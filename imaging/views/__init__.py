from .dermatoscopy import DermatoImageUploadView, DermatoReportView
from .otoscopy import OtoImageUploadView, OtoReportView
from .pharyngoscopy import PharyngoImageUploadView, PharyngoReportView

# Export all views
__all__ = [
    'DermatoImageUploadView',
    'DermatoReportView',
    'OtoImageUploadView',
    'OtoReportView',
    'PharyngoImageUploadView',
    'PharyngoReportView',
]