# imaging/views/otoscopy.py
from .base import BaseImageUploadView, BaseReportView
from ..models import OtoImage

class OtoImageUploadView(BaseImageUploadView):
    model_class = OtoImage
    roboflow_model_id = "otoscopy-dataset-abc/2"

class OtoReportView(BaseReportView):
    model_class = OtoImage
    report_type = "otoscopy"
    roboflow_model_id = "otoscopy-dataset-abc/2"
