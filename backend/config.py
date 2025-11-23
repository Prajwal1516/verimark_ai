"""
VeriMark AI - Configuration Management
"""
import os
from pathlib import Path

class Config:
    """Central configuration for VeriMark AI"""
    
    # ⚠️ IMPORTANT: Update DATA_ROOT to YOUR actual dataset location
    BASE_DIR = Path(__file__).parent.parent  # Points to verimark_ai_production/
    DATA_ROOT = BASE_DIR / "biometric_data"  # Change this to your path if different
    MODEL_DIR = BASE_DIR / "backend" / "models"
    SECURE_FOLDER = BASE_DIR / "secure_files"
    KEY_FILE = BASE_DIR / "backend" / "biometric_keys.enc"
    LOG_FILE = BASE_DIR / "logs" / "access.log"
    
    # Model parameters (should match your training)
    IMG_SIZE = 128
    BATCH_SIZE = 16
    NUM_EPOCHS = 15
    SEED = 42
    
    # Security settings
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 300  # seconds (5 minutes)
    KEY_ROTATION_DAYS = 90
    
    # Watermark parameters (must match your notebook settings)
    RUBIK_TILES = 8
    BLEND_ALPHA = 0.5
    CONFIDENCE_THRESHOLD = 0.0  # Allow all inputs
    
    # File upload limits
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {
        '.txt', '.pdf', '.png', '.jpg', '.jpeg', 
        '.csv', '.json', '.docx', '.doc', '.xlsx', 
        '.xls', '.pptx', '.zip'
    }
    
    # API Configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5500",  # VS Code Live Server
        "http://127.0.0.1:5500",
        "null"  # For file:// protocol
    ]
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist"""
        for path in [cls.MODEL_DIR, cls.SECURE_FOLDER, cls.LOG_FILE.parent]:
            path.mkdir(parents=True, exist_ok=True)
            
    @classmethod
    def validate_config(cls):
        """Validate configuration on startup"""
        errors = []
        
        if not cls.DATA_ROOT.exists():
            errors.append(f"Dataset not found at: {cls.DATA_ROOT}")
        
        model_path = cls.MODEL_DIR / "watermark_cnn_best.pth"
        if not model_path.exists():
            errors.append(f"Model not found at: {model_path}")
        
        if errors:
            print("⚠️  Configuration Warnings:")
            for error in errors:
                print(f"   - {error}")
        
        return len(errors) == 0