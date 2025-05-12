from .base import BaseImageUploadView
from ..models import DermatoImage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from ..pdf_utils import generate_pdf_report
from ..pipeline.dermato_pipeline import DermatoProcessor  
from PIL import Image  
import json  
import numpy as np

class DermatoImageUploadView(BaseImageUploadView):
    model_class = DermatoImage

    #ML Karte hai bhaiyo aur beheno
    def post_process_hook(self, image_model):
        """Process the image through ML pipeline after saving"""
        try:
            # Get the image
            img = Image.open(image_model.image.path)
            
            # Initialize processor
            processor = DermatoProcessor()
            
            # Process image
            preprocessed_img = processor.preprocess(img)
            
            # Run inference
            results = processor.run_inference(preprocessed_img)
            
            # Save results to model
            image_model.processed = True
            
            # Store inference results as JSON in the model
            image_model.results = json.dumps(results)
            
            # Save the processed image
            processed_img_path = image_model.image.path.replace('.jpg', '_processed.jpg')
            processed_img_path = processed_img_path.replace('.jpeg', '_processed.jpg')
            processed_img_path = processed_img_path.replace('.png', '_processed.jpg')
            
            # Convert the preprocessed image back to PIL format
            # Scale back to 0-255 range
            display_img = (preprocessed_img * 255).astype(np.uint8)
            if len(display_img.shape) == 3:  # Single image
                pil_img = Image.fromarray(display_img)
                pil_img.save(processed_img_path)
                image_model.processed_image = processed_img_path
            
            # Save changes
            image_model.save()
            
            print(f"Successfully processed image through ML pipeline. Results: {results}")
            
        except Exception as e:
            import traceback
            print(f"Error in post-processing hook: {str(e)}")
            traceback.print_exc()
            # Don't raise, so upload still succeeds but processing is marked as failed
            image_model.processed = False
            image_model.save()

class DermatoReportView(APIView):
    def get(self, request):
        images = DermatoImage.objects.all().order_by('uploaded_at')
        if not images:
            return Response({"error": "No images found"}, status=404)

        report_path = "media/dermato_report.pdf"
        generate_pdf_report(images, report_type='dermatoscopy', file_path=report_path)
        return FileResponse(open(report_path, 'rb'), as_attachment=True, filename='dermato_report.pdf')