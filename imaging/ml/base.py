# imaging/ml/base.py
from abc import ABC, abstractmethod
import os
import numpy as np
import pickle

class BaseModel(ABC):
    """Abstract base class for all ML models in the system"""
    
    MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'saved_models')
    
    def __init__(self):
        """Initialize the model"""
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        self.model = None
    
    @abstractmethod
    def predict(self, input_data):
        """Make predictions with the model"""
        pass
    
    @abstractmethod
    def train(self, X_train, y_train, **kwargs):
        """Train the model"""
        pass
    
    @abstractmethod
    def evaluate(self, X_test, y_test):
        """Evaluate the model"""
        pass
    
    def save(self, filename):
        """Save the model to disk"""
        filepath = os.path.join(self.MODEL_DIR, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        return filepath
    
    def load(self, filename):
        """Load the model from disk"""
        filepath = os.path.join(self.MODEL_DIR, filename)
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        return self
    
    @classmethod
    def get_current_model(cls):
        """Get the current production model"""
        instance = cls()
        try:
            # Try to load the latest model
            instance.load(f"{cls.__name__}_latest.pkl")
        except FileNotFoundError:
            # If no model exists, create a default one
            instance._create_default_model()
            instance.save(f"{cls.__name__}_latest.pkl")
        return instance
    
    @abstractmethod
    def _create_default_model(self):
        """Create a default model when no trained model is available"""
        pass