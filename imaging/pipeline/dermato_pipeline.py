import os
import logging
from PIL import Image
import cv2
import numpy as np
import tensorflow as tf
from io import BytesIO

# Configure logging
tf.get_logger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Constants for image size
IMAGE_SIZE = (224, 224)


def dull_razor_housekeeping(image: np.ndarray) -> np.ndarray:
    """
    Remove hair artifacts from dermatoscopic image using DullRazor.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Blackhat morphological operation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    # Threshold hair regions
    _, thresh = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
    # Dilate and inpaint
    mask = cv2.dilate(thresh, kernel, iterations=1)
    clean = cv2.inpaint(image, mask, 7, cv2.INPAINT_TELEA)
    return clean


def preprocess_for_embedding(image_path: str) -> tf.train.Example:
    """
    Load and preprocess image for embedding generation:
    - Load via PIL, convert to RGB
    - Resize to IMAGE_SIZE
    - Apply DullRazor hair removal
    - Min-max normalize to [0,1]
    - Serialize to tf.train.Example for model input

    Logs when processing is complete.
    """
    # Load image and ensure RGB
    img = Image.open(image_path).convert('RGB')
    img_np = np.array(img)

    # Resize to model input size
    img_resized = cv2.resize(img_np, IMAGE_SIZE)

    # Remove hair artifacts
    img_clean = dull_razor_housekeeping(img_resized)

    # Normalize pixel values to [0,1]
    img_float = img_clean.astype(np.float32)
    img_norm = (img_float - img_float.min()) / (img_float.max() - img_float.min() + 1e-8)

    # Serialize to TF Example
    buf = BytesIO()
    Image.fromarray((img_norm * 255).astype(np.uint8)).save(buf, format='PNG')
    example = tf.train.Example(
        features=tf.train.Features(
            feature={
                'image/encoded': tf.train.Feature(bytes_list=tf.train.BytesList(value=[buf.getvalue()]))
            }
        )
    )

    logger.info(f"Processed image for embedding: {os.path.basename(image_path)}")
    return example