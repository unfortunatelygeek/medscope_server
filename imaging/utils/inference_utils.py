import requests
import os
import base64

if os.environ.get("RENDER") is None:  # Render sets its own env vars
    from dotenv import load_dotenv
    load_dotenv()

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import base64
import requests

def get_roboflow_prediction(image_bytes, model_id):
    url = f"https://detect.roboflow.com/{model_id}?api_key={ROBOFLOW_API_KEY}"
    response = requests.post(url, files={"file": ("image.jpg", image_bytes, "image/jpeg")})
    response.raise_for_status()
    data = response.json()
    return data["predictions"][0] if data.get("predictions") else {"class": "unknown", "confidence": 0}


def get_gemini_report(image_path, prediction):
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    prompt = (
        f"This is a diagnostic image.\n"
        f"Prediction: {prediction['class']}\n"
        f"Confidence: {prediction['confidence']:.2f}\n"
        f"Please provide a medical analysis and recommendation. Return in HTML format compatible with Python reportlab."
    )

    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}},
                ]
            }
        ]
    }

    response = requests.post(gemini_url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()
    return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No report generated.")