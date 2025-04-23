from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .ml_model import dummy_predict, dummy_explanations

def generate_pdf_report(images, file_path="report.pdf"):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50

    for image_obj in images:
        prediction = dummy_predict(image_obj.image.path)
        explanations = dummy_explanations(image_obj.image.path)

        c.drawString(30, y, f"Image: {image_obj.image.name} | Category: {image_obj.category}")
        y -= 20
        c.drawString(30, y, f"Prediction: {prediction['prediction']} | Confidence: {prediction['confidence']}")
        y -= 40

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
