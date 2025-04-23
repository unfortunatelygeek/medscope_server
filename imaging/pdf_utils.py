# imaging/reports/pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

def generate_pdf_report(images, file_path="report.pdf"):
    """
    Generate a PDF report with uploaded images and their categories.
    
    :param images: A list of model instances with 'image' and 'category' fields.
    :param file_path: Destination file path for the generated PDF.
    """
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin = 50
    image_max_width = 200
    image_max_height = 200
    y = height - margin

    for img_obj in images:
        img_path = img_obj.image.path
        img_name = os.path.basename(img_path)
        category = img_obj.category

        # Draw label
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, f"Image: {img_name} | Category: {category}")
        y -= 20

        # Load and resize image
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
