from .dermatoscopy import DermatoImageUploadView, DermatoReportView
from .otoscopy import OtoImageUploadView, OtoReportView
from .pharyngoscopy import PharyngoImageUploadView, PharyngoReportView

#export
__all__ = [
    'DermatoImageUploadView',
    'DermatoReportView',
    'OtoImageUploadView',
    'OtoReportView',
    'PharyngoImageUploadView',
    'PharyngoReportView',
]