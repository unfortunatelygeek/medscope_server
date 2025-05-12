import requests
from .base import BaseImageUploadView
from ..models import PharyngoImage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from django.conf import settings
from ..pdf_utils import generate_pdf_report
from dotenv import load_dotenv
import os

load_dotenv()

ROBOFLOW_MODEL_ID = "pharyngitis-dataset-wifsx/3"
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class PharyngoImageUploadView(BaseImageUploadView):
    model_class = PharyngoImage


class PharyngoReportView(APIView):
    def get(self, request):
        images = PharyngoImage.objects.all().order_by('uploaded_at')
        if not images:
            return Response({"error": "No images found"}, status=404)

        predictions = []
        for img in images:
            image_path = img.image.path
            prediction = get_roboflow_prediction(image_path)
            gemini_report = get_gemini_report(image_path, prediction)
            predictions.append({
                "image": image_path,
                "prediction": prediction,
                "gemini_report": gemini_report
            })

        report_path = "media/pharyngo_report.pdf"
        generate_pdf_report(images, report_type="pharyngoscopy", file_path=report_path, extra_info=predictions)
        return FileResponse(open(report_path, 'rb'), as_attachment=True, filename='pharyngo_report.pdf')


def get_roboflow_prediction(image_path):
    url = f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}?api_key={ROBOFLOW_API_KEY}"
    with open(image_path, "rb") as img_file:
        response = requests.post(url, files={"file": img_file})
    response.raise_for_status()
    data = response.json()
    return data["predictions"][0] if data["predictions"] else {"class": "unknown", "confidence": 0}


def get_gemini_report(image_path, prediction):
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }

    prompt = (
        f"This is a pharyngoscopy image. Based on the Roboflow model prediction:\n"
        f"Diagnosis: {prediction['class']}\n"
        f"Confidence: {prediction['confidence']:.2f}\n"
        f"Please provide a medical analysis and recommendation."
    )

    with open(image_path, "rb") as img_file:
        import base64
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": encoded_image
                        }
                    }
                ]
            }
        ]
    }


    response = requests.post(gemini_url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()
    return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No report generated.")
