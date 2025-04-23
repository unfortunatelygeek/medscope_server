from django.urls import path
from .views import (
    DermatoImageUploadView, DermatoReportView,
    OtoImageUploadView, OtoReportView,
    PharyngoImageUploadView, PharyngoReportView
)

urlpatterns = [
    path('upload/dermato/', DermatoImageUploadView.as_view(), name='dermato-upload'),
    path('report/dermato/', DermatoReportView.as_view(), name='dermato-report'),
    
    path('upload/oto/', OtoImageUploadView.as_view(), name='oto-upload'),
    path('report/oto/', OtoReportView.as_view(), name='oto-report'),
    
    path('upload/pharyngo/', PharyngoImageUploadView.as_view(), name='pharyngo-upload'),
    path('report/pharyngo/', PharyngoReportView.as_view(), name='pharyngo-report'),
]