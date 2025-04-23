def dummy_predict(image_path):
    return {"prediction": "benign", "confidence": 0.95}

def dummy_explanations(image_path):
    return {"gradcam": "gradcam_image.jpg", "lime": "lime_image.jpg"}
