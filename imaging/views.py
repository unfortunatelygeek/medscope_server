from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError
from .models import DermatoImage
from .serializers import DermatoImageSerializer
import cv2
import numpy as np
import io
from .pdf_utils import generate_pdf_report
from django.http import FileResponse
import os
import traceback

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        files = request.FILES.getlist("images")
        category = request.POST.get("category", "total_body")

        print("=" * 60)
        print("📥 Image Upload Request Received")
        print("📁 FILES:", [f.name for f in files])
        print("🏷️ CATEGORY:", category)

        if not files:
            print("❌ No images uploaded")
            return Response({"error": "No images uploaded"}, status=400)

        responses = []

        for f in files:
            print("-" * 60)
            print(f"🔍 Processing file: {f.name}")
            print(f"   - Size: {f.size}")
            print(f"   - Content type: {f.content_type}")

            try:
                f.seek(0)  # Ensure reading from beginning
                img = Image.open(f)
                print(f"   ✅ Opened image: format={img.format}, size={img.size}, mode={img.mode}")
                
                img = img.convert("RGB")
                img_resized = img.resize((224, 224))
                print("   🔧 Resized to 224x224")

                buffer = io.BytesIO()
                img_resized.save(buffer, format="JPEG")
                buffer.seek(0)

                image_model = DermatoImage(category=category)
                image_model.image.save(f.name, ContentFile(buffer.getvalue()))
                image_model.save()

                responses.append({
                    "id": image_model.id,
                    "category": image_model.category,
                    "name": f.name
                })
                print(f"   ✅ Successfully saved image record with ID {image_model.id}")

            except UnidentifiedImageError:
                print(f"❌ PIL couldn't identify image format: {f.name}")
                return Response({"error": f"Unidentified image format: {f.name}"}, status=400)
            except Exception as e:
                print(f"❌ Error processing {f.name}: {str(e)}")
                traceback.print_exc()
                return Response({"error": f"Failed to process {f.name}: {str(e)}"}, status=400)

        print("✅ All images processed successfully")
        return Response(responses, status=status.HTTP_201_CREATED)


class GenerateReportView(APIView):
    def get(self, request):
        images = DermatoImage.objects.all().order_by('uploaded_at')
        if not images:
            return Response({"error": "No images found"}, status=404)

        report_path = "media/dermato_report.pdf"
        generate_pdf_report(images, file_path=report_path)
        return FileResponse(open(report_path, 'rb'), as_attachment=True, filename='dermato_report.pdf')
