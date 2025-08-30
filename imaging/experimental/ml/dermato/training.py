# imaging/ml/dermato/training.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from .model import DermatoModel

class DermatoTrainer:
    """Training manager for dermatoscopy models"""
    
    def __init__(self):
        self.model = DermatoModel()
    
    def prepare_dataset_from_images(self, images, labels):
        """Prepare dataset from processed images"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            images, labels, test_size=0.2, random_state=42, stratify=labels
        )
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train, y_train, hyperparams=None):
        """Train the model"""
        # Default hyperparameters
        if hyperparams is None:
            hyperparams = {
                'n_estimators': 100,
                'max_depth': 10
            }
        
        # Train the model
        self.model.train(X_train, y_train, **hyperparams)
        
        # Save the model
        self.model.save('DermatoModel_latest.pkl')
        
        return self.model
    
    def run_training_job(self, images, labels):
        """Run a complete training job"""
        # Prepare dataset
        X_train, X_test, y_train, y_test = self.prepare_dataset_from_images(images, labels)
        
        # Train model
        self.train(X_train, y_train)
        
        # Evaluate model
        metrics = self.model.evaluate(X_test, y_test)
        
        return metrics