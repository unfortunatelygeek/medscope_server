from .base_processor import ImageProcessor
from ..ml.dermato.model import DermatoModel

import cv2
import numpy as np
from PIL import Image
import albumentations as A

class DermatoProcessor(ImageProcessor):
    def __init__(self):
        self.model = DermatoModel.get_current_model()
        
        # Define augmentation pipeline for training/data augmentation
        self.augmentation = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.Rotate(limit=15, p=0.7),
            A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.7),
        ])
    
    def preprocess(self, image, augment=False):
        """
        Preprocess dermato images:
        - Convert to RGB
        - Resize to 224x224
        - Apply DullRazor hair removal
        - Min-Max normalization
        - Optional data augmentation
        """
        # Convert to numpy array if needed
        if not isinstance(image, np.ndarray):
            if isinstance(image, Image.Image):
                image = np.array(image)
            else:
                # Assume it's a file path or similar
                image = np.array(Image.open(image))
        
        # Ensure RGB format
        if len(image.shape) == 2:  # Grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        # Resize to 224x224
        image = cv2.resize(image, (224, 224))
        
        # Apply DullRazor for hair removal
        image = self._apply_dull_razor(image)
        
        # Apply data augmentation if requested (for training)
        if augment:
            augmented = self.augmentation(image=image)
            image = augmented["image"]
        
        # Apply Min-Max normalization
        # First convert to float
        image = image.astype(np.float32)
        
        # Min-max normalization to [0, 1] range
        image = (image - image.min()) / (image.max() - image.min() + 1e-8)
        
        return image
    
    def _apply_dull_razor(self, image):
        """
        Apply DullRazor algorithm for hair removal
        Ref: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5373870/
        """
        # Convert to grayscale
        grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply blackhat morphological operation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        blackhat = cv2.morphologyEx(grayscale, cv2.MORPH_BLACKHAT, kernel)
        
        # Threshold to identify hair regions
        _, thresh = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
        
        # Dilate the hair mask
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        # Inpaint to remove hair
        result = cv2.inpaint(image, dilated, 7, cv2.INPAINT_TELEA)
        
        return result
    
    def run_inference(self, preprocessed_image):
        """Run ML model on preprocessed image"""
        # Add batch dimension if needed
        if len(preprocessed_image.shape) == 3:  # [H, W, C]
            preprocessed_image = np.expand_dims(preprocessed_image, axis=0)  # [1, H, W, C]
            
        return self.model.predict(preprocessed_image)
    
    def postprocess(self, inference_results):
        """Process and format results"""
        # Format results, extract key findings, etc.
        return {
            'findings': inference_results.get('predictions', []),
            'confidence_scores': inference_results.get('confidence', []),
            'recommendation': self._generate_recommendation(inference_results)
        }
    
    def _generate_recommendation(self, results):
        """Generate clinical recommendations based on findings"""
        # Logic to convert model output to clinical recommendations
        return "Based on the analysis, recommend further examination."
    
    def process_for_training(self, image_path):
        """Process image specifically for training with augmentation"""
        image = self.preprocess(image_path, augment=True)
        return image