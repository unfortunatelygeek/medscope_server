from .base import BaseImageUploadView
from ..models import OtoImage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from ..pdf_utils import generate_pdf_report

class OtoImageUploadView(BaseImageUploadView):
    model_class = OtoImage

class OtoReportView(APIView):
    def get(self, request):
        images = OtoImage.objects.all().order_by('uploaded_at')
        if not images:
            return Response({"error": "No images found"}, status=404)

        report_path = "media/oto_report.pdf"
        generate_pdf_report(images, report_type="otoscopy", file_path=report_path)
        return FileResponse(open(report_path, 'rb'), as_attachment=True, filename='oto_report.pdf')