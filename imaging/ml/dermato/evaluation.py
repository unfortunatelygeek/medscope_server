# imaging/ml/dermato/evaluation.py
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from .model import DermatoModel

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance with multiple metrics"""
    # If X is in image format, reshape for sklearn
    if len(X_test.shape) > 2:  # [B, H, W, C] or [H, W, C]
        if len(X_test.shape) == 3:  # Single image [H, W, C]
            X_test = X_test.reshape(1, -1)
        else:  # Batch of images [B, H, W, C] 
            X_test = X_test.reshape(X_test.shape[0], -1)
    
    # Get predictions
    y_pred = model.model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average='weighted'
    )
    
    return {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1)
    }

def get_confusion_matrix(model, X_test, y_test):
    """Generate confusion matrix for model evaluation"""
    from sklearn.metrics import confusion_matrix
    
    # If X is in image format, reshape for sklearn
    if len(X_test.shape) > 2:
        if len(X_test.shape) == 3:  # Single image [H, W, C]
            X_test = X_test.reshape(1, -1)
        else:  # Batch of images [B, H, W, C]
            X_test = X_test.reshape(X_test.shape[0], -1)
    
    # Get predictions
    y_pred = model.model.predict(X_test)
    
    # Get confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    return {
        'confusion_matrix': cm.tolist(),
        'classes': model.CLASSES
    }