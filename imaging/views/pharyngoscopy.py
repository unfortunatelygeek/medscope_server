from .base import BaseImageUploadView, BaseReportView
from ..models import PharyngoImage
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response

class PharyngoImageUploadView(BaseImageUploadView):
    model_class = PharyngoImage
    roboflow_model_id = "pharyngitis-dataset-wifsx/3"


class PharyngoReportView(BaseReportView):
    model_class = PharyngoImage
    report_type = "pharyngoscopy"
    roboflow_model_id = "pharyngitis-dataset-wifsx/3"

    @extend_schema(
        description="Generate a diagnostic PDF report for all uploaded pharyngoscopy images.",
        responses={200: {"content": {"application/pdf": {}}}},
    )
    def get(self, request):
        return super().get(request)

