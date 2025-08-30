# imaging/ml/dermato/model.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from ..base import BaseModel

class DermatoModel(BaseModel):
    """Dermatoscopy analysis model"""
    
    CLASSES = [
        'benign',
        'malignant',
        'suspicious'
    ]
    
    def __init__(self):
        super().__init__()
        self.model = None
    
    def _create_default_model(self):
        """Create a default model for testing"""
        self.model = RandomForestClassifier(
            n_estimators=100, 
            max_depth=10,
            random_state=42
        )
        # Fit with dummy data so it can make predictions
        X_dummy = np.random.random((10, 224*224*3))
        y_dummy = np.random.choice(len(self.CLASSES), 10)
        self.model.fit(X_dummy, y_dummy)
    
    def preprocess_for_model(self, image):
        """Prepare normalized image for model input"""
        # Flatten the image for the RandomForest model
        return image.reshape(1, -1)
    
    def predict(self, input_data):
        """Make prediction from preprocessed image data"""
        if self.model is None:
            self._create_default_model()
            
        # Make sure input is properly shaped for sklearn
        if len(input_data.shape) == 4:  # Batch of images [B, H, W, C]
            input_data = input_data.reshape(input_data.shape[0], -1)
        elif len(input_data.shape) == 3:  # Single image [H, W, C]
            input_data = input_data.reshape(1, -1)
            
        # Get class probabilities
        probs = self.model.predict_proba(input_data)
        
        # Get predicted class indices
        class_indices = np.argmax(probs, axis=1)
        
        # Get class names
        predictions = [self.CLASSES[idx] for idx in class_indices]
        
        # Get confidence scores
        confidence = np.max(probs, axis=1)
        
        return {
            'predictions': predictions,
            'confidence': confidence.tolist(),
            'probabilities': {
                class_name: probs[:, i].tolist() for i, class_name in enumerate(self.CLASSES)
            }
        }
    
    def train(self, X_train, y_train, **kwargs):
        """Train the model with new data"""
        # If model doesn't exist, create it
        if self.model is None:
            n_estimators = kwargs.get('n_estimators', 100)
            max_depth = kwargs.get('max_depth', 10)
            
            self.model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                n_jobs=-1,
                random_state=42
            )
        
        # Reshape data if needed (from images to feature vectors)
        if len(X_train.shape) == 4:  # [B, H, W, C]
            X_train = X_train.reshape(X_train.shape[0], -1)
        elif len(X_train.shape) == 3:  # [H, W, C]
            X_train = X_train.reshape(1, -1)
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Return model for chaining
        return self
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Reshape data if needed
        if len(X_test.shape) == 4:  # [B, H, W, C]
            X_test = X_test.reshape(X_test.shape[0], -1)
        elif len(X_test.shape) == 3:  # [H, W, C]
            X_test = X_test.reshape(1, -1)
            
        # Get predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = np.mean(y_pred == y_test)
        
        # For simplicity, just return accuracy
        # In a real system, you'd want precision, recall, F1, etc.
        return {'accuracy': float(accuracy)}