# imaging/reports/pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

def generate_pdf_report(images, report_type, file_path="report.pdf", extra_info=None):
    """
    Generate a PDF report with uploaded images and contextual info.
    
    :param images: A list of model instances.
    :param file_path: Output path for the generated PDF.
    :param report_type: 'pharyngoscopy', 'otoscopy', or 'dermatoscopy'
    :param extra_info: Optional list of dicts with predictions or extra annotations.
    """
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin = 50
    image_max_width = 200
    image_max_height = 200
    y = height - margin

    for i, img_obj in enumerate(images):
        img_path = img_obj.image.path
        img_name = os.path.basename(img_path)

        # Header info per report type
        if report_type == "pharyngoscopy":
            label = f"Image: {img_name} | Region: {getattr(img_obj, 'region', 'N/A')}"
        elif report_type == "otoscopy":
            label = f"Image: {img_name} | Ear Side: {getattr(img_obj, 'ear_side', 'N/A')}"
        elif report_type == "dermatoscopy":
            label = f"Image: {img_name} | Category: {getattr(img_obj, 'category', 'N/A')}"
        else:
            label = f"Image: {img_name}"

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, label)
        y -= 20

        # Optional: show AI prediction or Gemini report
        if extra_info and i < len(extra_info):
            prediction = extra_info[i]
            c.setFont("Helvetica", 10)
            c.drawString(margin, y, f"Model Prediction: {prediction.get('prediction', {}).get('class', 'N/A')} (Confidence: {prediction.get('prediction', {}).get('confidence', 0):.2f})")
            y -= 15
            c.drawString(margin, y, f"Gemini Report: {prediction.get('gemini_report', '')[:200]}...")  # trim long text
            y -= 40

        # Draw image
        try:
            img = Image.open(img_path)
            img.thumbnail((image_max_width, image_max_height))
            img_reader = ImageReader(img)
            c.drawImage(img_reader, margin, y - image_max_height, width=image_max_width, height=image_max_height)
            y -= image_max_height + 40
        except Exception as e:
            c.setFont("Helvetica", 10)
            c.drawString(margin, y, f"[Error loading image: {e}]")
            y -= 40

        # Page break if needed
        if y < margin + image_max_height:
            c.showPage()
            y = height - margin

    c.save()
