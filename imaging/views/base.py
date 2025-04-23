from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError
import io
import traceback

class BaseImageUploadView(APIView):
    parser_classes = [MultiPartParser]
    model_class = None  #to be set by subclasses
    
    def process_image(self, file, category):
        try:
            file.seek(0)  # Ensure reading from beginning
            img = Image.open(file)
            img = img.convert("RGB")
            img_resized = img.resize((224, 224))
            
            buffer = io.BytesIO()
            img_resized.    save(buffer, format="JPEG")
            buffer.seek(0)
            
            image_model = self.model_class(category=category)
            image_model.image.save(file.name, ContentFile(buffer.getvalue()))
            image_model.save()

            self.post_process_hook(image_model)
            
            return {
                "id": image_model.id,
                "category": image_model.category,
                "name": file.name
            }
        except UnidentifiedImageError:
            raise ValueError(f"Unidentified image format: {file.name}")
        except Exception as e:
            traceback.print_exc()
            raise ValueError(f"Failed to process {file.name}: {str(e)}")
    
    def post_process_hook(self, image_model):
        """
        Hook for subclasses to implement post-processing of images
        Default implementation does nothing, base hi hai ye
        """
        pass

    def post(self, request, format=None):
        files = request.FILES.getlist("images")
        category = request.POST.get("category", "default")
        
        print("=" * 60)
        print(f"{self.__class__.__name__} Request Received")
        print("FILES:", [f.name for f in files])
        print("CATEGORY:", category)
        
        if not files:
            return Response({"error": "No images uploaded"}, status=400)
        
        responses = []
        
        for file in files:
            print("-" * 60)
            print(f"🔍 Processing file: {file.name}")
            print(f"   - Size: {file.size}")
            print(f"   - Content type: {file.content_type}")
            
            try:
                result = self.process_image(file, category)
                responses.append(result)
                print(f"Successfully saved image record with ID {result['id']}")
            except ValueError as e:
                return Response({"error": str(e)}, status=400)
        
        print("All images processed successfully")
        return Response(responses, status=status.HTTP_201_CREATED)