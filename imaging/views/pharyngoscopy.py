from .base import BaseImageUploadView  
from ..models import PharyngoImage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from ..pdf_utils import generate_pdf_report

class PharyngoImageUploadView(BaseImageUploadView):
    model_class = PharyngoImage

class PharyngoReportView(APIView):
    def get(self, request):
        images = PharyngoImage.objects.all().order_by('uploaded_at')
        if not images:
            return Response({"error": "No images found"}, status=404)

        report_path = "media/pharyngo_report.pdf"
        generate_pdf_report(images, file_path=report_path, report_type="pharyngoscopy")
        return FileResponse(open(report_path, 'rb'), as_attachment=True, filename='pharyngo_report.pdf')