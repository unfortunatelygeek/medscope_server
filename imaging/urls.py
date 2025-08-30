from django.urls import path
from imaging.views.pharyngoscopy import PharyngoImageUploadView, PharyngoReportView
from imaging.views.dermatoscopy import DermatoImageUploadView, DermatoReportView
from imaging.views.otoscopy import OtoImageUploadView, OtoReportView

urlpatterns = [
    path("upload/pharyngo/", PharyngoImageUploadView.as_view(), name="upload-pharyngo"),
    path("report/pharyngo/", PharyngoReportView.as_view(), name="report-pharyngo"),

    path("upload/dermato/", DermatoImageUploadView.as_view(), name="upload-dermato"),
    path("report/dermato/", DermatoReportView.as_view(), name="report-dermato"),

    path("upload/otoscopy/", OtoImageUploadView.as_view(), name="upload-otoscopy"),
    path("report/otoscopy/", OtoReportView.as_view(), name="report-otoscopy"),
]
