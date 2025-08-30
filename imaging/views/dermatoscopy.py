# imaging/views/dermatoscopy.py
from .base import BaseImageUploadView, BaseReportView
from ..models import DermatoImage

class DermatoImageUploadView(BaseImageUploadView):
    model_class = DermatoImage

class DermatoReportView(BaseReportView):
    model_class = DermatoImage
    report_type = "dermatoscopy"
    roboflow_model_id = "dermatology-dataset-xyz/1"
