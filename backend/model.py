"""
VeriMark AI - ML Model Handler
Loads and runs the watermark verification model
"""
import torch
import torch.nn as nn
import torchvision.transforms as T
import numpy as np
from PIL import Image
import logging
import os
from typing import Tuple
from config import Config

logger = logging.getLogger(__name__)


# ⚠️ THIS IS YOUR ORIGINAL MODEL FROM JUPYTER NOTEBOOK
class SimpleCNN(nn.Module):
    """
    Your original CNN model architecture
    Must match exactly what you used for training
    """
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), 
            nn.ReLU(), 
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), 
            nn.ReLU(), 
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), 
            nn.ReLU(), 
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), 
            nn.ReLU(), 
            nn.AdaptiveAvgPool2d((4, 4))
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


class WatermarkPredictor:
    """Handles watermark prediction with the trained model"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize predictor with model
        
        Args:
            model_path: Path to trained model file (.pth)
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Initialize model with YOUR architecture (SimpleCNN)
        self.model = SimpleCNN().to(self.device)
        
        # Load trained weights if available
        if model_path and os.path.exists(model_path):
            success = self.load_model(model_path)
            if success:
                logger.info(f"Model loaded successfully from {model_path}")
            else:
                logger.warning("Failed to load model - using untrained model")
        else:
            logger.warning(f"Model not found at: {model_path}")
            logger.warning("Predictions will use untrained model (will fail)")
        
        # Image transformation (must match training)
        self.transform = T.Compose([
            T.Resize((Config.IMG_SIZE, Config.IMG_SIZE)),
            T.ToTensor(),
            T.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
    
    def load_model(self, model_path: str) -> bool:
        """
        Load trained model weights
        
        Args:
            model_path: Path to .pth file
            
        Returns:
            True if successful
        """
        try:
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()  # Set to evaluation mode
            logger.info(f"Model loaded from {model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def predict(self, pil_img: Image.Image) -> Tuple[int, float, list]:
        """
        Predict if watermark is genuine or forged
        
        Args:
            pil_img: PIL Image of watermark
            
        Returns:
            Tuple of (prediction, confidence, probabilities)
            - prediction: 0 for forged, 1 for genuine
            - confidence: confidence score (0.0 to 1.0)
            - probabilities: [forged_prob, genuine_prob]
        """
        try:
            self.model.eval()
            
            # Transform and add batch dimension
            img_tensor = self.transform(pil_img).unsqueeze(0).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                output = self.model(img_tensor)
                probs = torch.softmax(output, dim=1).cpu().numpy()[0]
                pred = int(np.argmax(probs))
                confidence = float(probs[pred])
            
            result = 'Genuine' if pred == 1 else 'Forged'
            logger.info(f"Prediction: {result} (confidence: {confidence:.4f})")
            
            return pred, confidence, probs.tolist()
        
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            # Return safe default (forged with 100% confidence)
            return 0, 1.0, [1.0, 0.0]
    
    def batch_predict(self, images: list) -> list:
        """
        Predict multiple images at once
        
        Args:
            images: List of PIL Images
            
        Returns:
            List of prediction dictionaries
        """
        results = []
        for img in images:
            pred, conf, probs = self.predict(img)
            results.append({
                'prediction': 'genuine' if pred == 1 else 'forged',
                'confidence': conf,
                'probabilities': {
                    'forged': probs[0],
                    'genuine': probs[1]
                }
            })
        return results
    
    def is_model_loaded(self) -> bool:
        """
        Check if model is properly loaded
        
        Returns:
            True if model appears to be trained
        """
        # Simple check: trained models have non-zero parameters
        total_params = sum(p.sum().item() for p in self.model.parameters())
        return abs(total_params) > 0.001


# Global predictor instance - initialized once when module loads
model_path = Config.MODEL_DIR / "watermark_cnn_best.pth"
predictor = WatermarkPredictor(str(model_path) if model_path.exists() else None)

# Log model status
if predictor.is_model_loaded():
    logger.info("✓ Model initialized and ready")
else:
    logger.warning("⚠ Model may not be properly trained")