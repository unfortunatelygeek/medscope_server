# imaging/views/dermatoscopy.py
from .base import BaseImageUploadView, BaseReportView
from ..models import DermatoImage

class DermatoImageUploadView(BaseImageUploadView):
    model_class = DermatoImage
    roboflow_model_id = "pharyngitis-dataset-wifsx/3"

class DermatoReportView(BaseReportView):
    model_class = DermatoImage
    report_type = "dermatoscopy"
    roboflow_model_id = "dermatology-dataset-xyz/1"
