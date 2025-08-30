from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PIL import Image
import os


def generate_pdf_report(images, report_type, file_path="report.pdf", extra_info=None):
    """
    Generate a PDF report with uploaded images and contextual info.
    Handles long Gemini text gracefully with word wrapping.
    """
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    body_style = styles["Normal"]
    body_style.fontSize = 10
    body_style.leading = 14

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=14,
        leading=18,
        spaceAfter=10
    )

    elements = []

    for i, img_obj in enumerate(images):
        img_path = img_obj.image.path
        img_name = os.path.basename(img_path)

        # Header per image
        if report_type == "pharyngoscopy":
            label = f"Image: {img_name} | Region: {getattr(img_obj, 'region', 'N/A')}"
        elif report_type == "otoscopy":
            label = f"Image: {img_name} | Ear Side: {getattr(img_obj, 'ear_side', 'N/A')}"
        elif report_type == "dermatoscopy":
            label = f"Image: {img_name} | Category: {getattr(img_obj, 'category', 'N/A')}"
        else:
            label = f"Image: {img_name}"

        elements.append(Paragraph(label, title_style))
        elements.append(Spacer(1, 6))

        # Prediction + Gemini report
        if extra_info and i < len(extra_info):
            prediction = extra_info[i]

            pred_text = (
                f"<b>Model Prediction:</b> {prediction.get('prediction', {}).get('class', 'N/A')} "
                f"(Confidence: {prediction.get('prediction', {}).get('confidence', 0):.2f})"
            )
            elements.append(Paragraph(pred_text, body_style))
            elements.append(Spacer(1, 4))

            gemini_text = prediction.get("gemini_report", "No Gemini report available.")
            elements.append(Paragraph(f"<b>Gemini Report:</b> {gemini_text}", body_style))
            elements.append(Spacer(1, 12))

        # Image thumbnail
        try:
            pil_img = Image.open(img_path)
            pil_img.thumbnail((200, 200))
            pil_img.save("temp_thumb.jpg")  # save temp thumbnail for reportlab

            elements.append(RLImage("temp_thumb.jpg", width=2*inch, height=2*inch))
            elements.append(Spacer(1, 24))
        except Exception as e:
            elements.append(Paragraph(f"[Error loading image: {e}]", body_style))
            elements.append(Spacer(1, 12))

    # Build final PDF
    doc.build(elements)
