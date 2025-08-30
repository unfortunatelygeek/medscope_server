from .base import BaseImageUploadView, BaseReportView
from ..models import PharyngoImage

class PharyngoImageUploadView(BaseImageUploadView):
    model_class = PharyngoImage

class PharyngoReportView(BaseReportView):
    model_class = PharyngoImage
    report_type = "pharyngoscopy"
    roboflow_model_id = "pharyngitis-dataset-wifsx/3"
