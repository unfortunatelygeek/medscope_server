# imaging/views/base.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from ..utils.pdf_utils import generate_pdf_report
from ..utils.inference_utils import get_roboflow_prediction, get_gemini_report
import cv2
from ..utils.colour_utils import colour_transforms
from ..models import PharyngoImage, DermatoImage, OtoImage
import base64

from drf_spectacular.utils import extend_schema, OpenApiRequest
from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

class PredictionResponseSerializer(serializers.Serializer):
    image = serializers.CharField()
    transformed_image = serializers.CharField()
    prediction = serializers.JSONField()
    confidence = serializers.FloatField(required=False)
    recommendation = serializers.CharField(required=False)


@extend_schema(
    request={
        'multipart/form-data': ImageUploadSerializer,

    },
    responses={201: PredictionResponseSerializer(many=True)},
)
class BaseImageUploadView(APIView):
    """
    Generic upload view for any scan category.
    Subclasses must define: model_class, roboflow_model_id
    """
    serializer_class = ImageUploadSerializer
    # model_class = None
    # roboflow_model_id = None

    def post(self, request):
        if not self.model_class or not self.roboflow_model_id:
            return Response({"error": "model_class or roboflow_model_id not defined"}, status=500)

        images = request.FILES.getlist("images")
        if not images:
            image = request.FILES.get("image")
            if image:
                images = [image]
            else:
                return Response({"error": "No images provided"}, status=400)

        response_data = []
        for img in images:
            obj = self.model_class.objects.create(image=img)
            image_path = obj.image.path

            image_for_txform = cv2.imread(image_path)
            transformed_image = colour_transforms(image_for_txform)
            transformed_image_path = image_path.replace("scans/", "transformed/")
            cv2.imwrite(transformed_image_path, transformed_image)

            with open(transformed_image_path, "rb") as f:
                transformed_image_base64 = base64.b64encode(f.read()).decode("utf-8")

            prediction = get_roboflow_prediction(image_path, self.roboflow_model_id)

            confidence = prediction.get("confidence")
            recommendation = prediction.get("recommendation")

            response_data.append({
                "image": image_path,
                "transformed_image": transformed_image_path,
                "transformed_image_base64": transformed_image_base64,
                "prediction": prediction,
                "confidence": confidence,
                "recommendation": recommendation,
            })

        return Response(response_data, status=201)



class BaseReportView(APIView):
    """
    Generic report view for any scan category.
    Subclasses must define: model_class, report_type, roboflow_model_id
    """
    model_class = None
    report_type = None
    roboflow_model_id = None

    def get(self, request):
        if not self.model_class:
            return Response({"error": "No model_class defined"}, status=500)

        images = self.model_class.objects.all().order_by("uploaded_at")
        if not images:
            return Response({"error": "No images found"}, status=404)

        predictions = []
        transformed_images = []
        for img in images:
            image_path = img.image.path
            image_for_txform = cv2.imread(image_path)
            transformed_image = colour_transforms(image_for_txform)
            transformed_image_path = image_path.replace("scans/", "transformed/")
            transformed_images.append(transformed_image_path)
            prediction = get_roboflow_prediction(image_path, self.roboflow_model_id)
            gemini_report = get_gemini_report(image_path, prediction)
            predictions.append({
                "image": image_path,
                "transformed_image": transformed_image,
                "prediction": prediction,
                "gemini_report": gemini_report,
            })

        report_path = f"media/{self.report_type}_report.pdf"
        generate_pdf_report(transformed_images, report_type=self.report_type, file_path=report_path, extra_info=predictions)

        return FileResponse(open(report_path, "rb"), as_attachment=True, filename=f"{self.report_type}_report.pdf")
