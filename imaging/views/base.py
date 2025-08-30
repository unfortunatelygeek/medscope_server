# imaging/views/base.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from ..utils.pdf_utils import generate_pdf_report
from ..utils.inference_utils import get_roboflow_prediction, get_gemini_report

class BaseImageUploadView(APIView):
    """
    Generic upload view for any scan category.
    Subclasses must define: model_class
    """
    model_class = None

    def post(self, request):
        if not self.model_class:
            return Response({"error": "No model_class defined"}, status=500)

        images = request.FILES.getlist("images")
        if not images:
            return Response({"error": "No images provided"}, status=400)

        objs = [self.model_class.objects.create(image=img) for img in images]
        return Response({"uploaded": len(objs)}, status=201)


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
        for img in images:
            image_path = img.image.path
            prediction = get_roboflow_prediction(image_path, self.roboflow_model_id)
            gemini_report = get_gemini_report(image_path, prediction)
            predictions.append({
                "image": image_path,
                "prediction": prediction,
                "gemini_report": gemini_report,
            })

        report_path = f"media/{self.report_type}_report.pdf"
        generate_pdf_report(images, report_type=self.report_type, file_path=report_path, extra_info=predictions)

        return FileResponse(open(report_path, "rb"), as_attachment=True, filename=f"{self.report_type}_report.pdf")
