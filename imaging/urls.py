from django.urls import path
from .views import ImageUploadView, GenerateReportView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload-image'),
    path('generate-report/', GenerateReportView.as_view(), name='generate-report'),
]
