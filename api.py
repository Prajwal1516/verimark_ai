"""
VeriMark AI - FastAPI Backend Server
REST API for biometric file encryption/decryption
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import sys
import tempfile
import shutil
from PIL import Image
from cryptography.fernet import Fernet
import logging

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from config import Config
from utils import (
    resize_square, rubik_permute, blend_watermark, 
    compute_image_hash, BiometricValidator, open_rgb,
    validate_file_size
)
from security import key_manager, FileEncryption, access_control
from model import predictor

# Setup
Config.setup_directories()
logger = logging.getLogger(__name__)

# Validate configuration
Config.validate_config()

# Create FastAPI app
app = FastAPI(
    title="VeriMark AI API", 
    version="1.0.0",
    description="Biometric-based file encryption system"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class RegistrationResponse(BaseModel):
    success: bool
    message: str
    watermark_preview: Optional[str] = None
    encrypted_file: Optional[str] = None


class AccessResponse(BaseModel):
    success: bool
    message: str
    watermark_preview: Optional[str] = None
    decrypted_file: Optional[str] = None
    file_content: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    secure_storage: bool


# Helper functions
def save_upload_file(upload_file: UploadFile) -> str:
    """Save uploaded file to temp directory"""
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        with temp_file as f:
            shutil.copyfileobj(upload_file.file, f)
        return temp_file.name
    except Exception as e:
        logger.error(f"Failed to save upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")


def generate_watermark(iris_path: str, fp_path: str) -> tuple:
    """Generate watermark from biometric images"""
    try:
        # Validate images
        valid, msg = BiometricValidator.validate_iris(iris_path)
        if not valid:
            raise ValueError(msg)
        
        valid, msg = BiometricValidator.validate_fingerprint(fp_path)
        if not valid:
            raise ValueError(msg)
        
        # Process images
        iris_img = resize_square(open_rgb(iris_path))
        fp_img = resize_square(open_rgb(fp_path))
        fp_img = rubik_permute(fp_img)
        
        # Create watermark
        watermark = blend_watermark(iris_img, fp_img, alpha=Config.BLEND_ALPHA)
        
        # Predict authenticity (logging only, no enforcement)
        pred, confidence, probs = predictor.predict(watermark)
        logger.info(f"Prediction: {pred}, Confidence: {confidence}")
        
        # Compute hash
        wm_hash = compute_image_hash(watermark)
        
        return wm_hash, watermark, "Success"
    
    except Exception as e:
        logger.error(f"Watermark generation failed: {e}")
        return None, None, str(e)


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "VeriMark AI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": predictor.is_model_loaded(),
        "secure_storage": os.path.exists(Config.SECURE_FOLDER)
    }


@app.post("/register", response_model=RegistrationResponse)
async def register_file(
    file: UploadFile = File(..., description="File to encrypt"),
    iris: UploadFile = File(..., description="Iris image"),
    fingerprint: UploadFile = File(..., description="Fingerprint image")
):
    """
    Register and encrypt a file with biometric authentication
    
    - **file**: Any file you want to protect
    - **iris**: Clear iris image
    - **fingerprint**: Clear fingerprint image
    
    Returns encrypted file name and watermark preview
    """
    
    temp_files = []
    
    try:
        logger.info(f"Registration attempt for file: {file.filename}")
        
        # Save uploaded files
        file_path = save_upload_file(file)
        iris_path = save_upload_file(iris)
        fp_path = save_upload_file(fingerprint)
        temp_files = [file_path, iris_path, fp_path]
        
        # Validate file size
        if not validate_file_size(file_path):
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {Config.MAX_FILE_SIZE / (1024*1024):.0f}MB"
            )
        
        # Generate watermark
        wm_hash, watermark, message = generate_watermark(iris_path, fp_path)
        
        if wm_hash is None:
            logger.warning(f"Registration failed: {message}")
            raise HTTPException(status_code=400, detail=message)
        
        # Generate encryption key
        encryption_key = Fernet.generate_key()
        
        # Encrypt file
        encrypted_path = FileEncryption.encrypt_file(file_path, encryption_key)
        
        if not encrypted_path:
            raise HTTPException(status_code=500, detail="File encryption failed")
        
        # Store key mapping
        if not key_manager.add_key(wm_hash, encryption_key):
            raise HTTPException(status_code=500, detail="Failed to store encryption key")
        
        # Save watermark preview
        wm_preview_path = os.path.join(Config.SECURE_FOLDER, f"{wm_hash[:8]}_wm.png")
        watermark.save(wm_preview_path)
        
        logger.info(f"File registered successfully: {file.filename} -> {os.path.basename(encrypted_path)}")
        
        return {
            "success": True,
            "message": f"File secured successfully: {os.path.basename(encrypted_path)}",
            "watermark_preview": wm_preview_path,
            "encrypted_file": os.path.basename(encrypted_path)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp files
        for f in temp_files:
            try:
                if os.path.exists(f):
                    os.unlink(f)
            except:
                pass


@app.post("/access", response_model=AccessResponse)
async def access_file(
    encrypted_file: UploadFile = File(..., description="Encrypted .enc file"),
    iris: UploadFile = File(..., description="Iris image"),
    fingerprint: UploadFile = File(..., description="Fingerprint image")
):
    """
    Access and decrypt a file with biometric authentication
    
    - **encrypted_file**: The .enc file to decrypt
    - **iris**: Same iris image used during registration
    - **fingerprint**: Same fingerprint image used during registration
    
    Returns decrypted file for download
    """
    
    temp_files = []
    
    try:
        logger.info(f"Access attempt for file: {encrypted_file.filename}")
        
        # Save uploaded files
        enc_path = save_upload_file(encrypted_file)
        iris_path = save_upload_file(iris)
        fp_path = save_upload_file(fingerprint)
        temp_files = [enc_path, iris_path, fp_path]
        
        # Generate watermark
        wm_hash, watermark, message = generate_watermark(iris_path, fp_path)
        
        if wm_hash is None:
            logger.warning(f"Access denied: {message}")
            raise HTTPException(status_code=401, detail=f"Access Denied: {message}")
        
        # Check rate limiting
        allowed, rate_msg = access_control.check_rate_limit(wm_hash)
        if not allowed:
            logger.warning(f"Rate limit exceeded: {wm_hash[:8]}")
            raise HTTPException(status_code=429, detail=rate_msg)
        
        # Retrieve encryption key
        encryption_key = key_manager.get_key(wm_hash)
        
        if encryption_key is None:
            logger.warning(f"Unauthorized access attempt: {wm_hash[:8]}")
            raise HTTPException(status_code=401, detail="Access Denied: Unauthorized user")
        
        # Decrypt file
        decrypted_path = FileEncryption.decrypt_file(enc_path, encryption_key)
        
        if not decrypted_path:
            raise HTTPException(status_code=500, detail="File decryption failed")
        
        # Clear rate limit attempts on success
        access_control.clear_attempts(wm_hash)
        
        # Try to read file content for preview
        file_content = None
        file_ext = os.path.splitext(decrypted_path)[1].lower()
        
        try:
            if file_ext in ['.txt', '.csv', '.json', '.log', '.md']:
                with open(decrypted_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read(5000)  # First 5KB
        except:
            pass
        
        # Save watermark preview
        wm_preview_path = os.path.join(Config.SECURE_FOLDER, f"access_{wm_hash[:8]}_wm.png")
        watermark.save(wm_preview_path)
        
        logger.info(f"File accessed successfully: {encrypted_file.filename}")
        
        return {
            "success": True,
            "message": f"Access granted: {os.path.basename(decrypted_path)}",
            "watermark_preview": wm_preview_path,
            "decrypted_file": os.path.basename(decrypted_path),
            "file_content": file_content
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Access failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp files
        for f in temp_files:
            try:
                if os.path.exists(f):
                    os.unlink(f)
            except:
                pass


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download decrypted file"""
    file_path = os.path.join(Config.SECURE_FOLDER, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        total_keys = len(key_manager.list_all_hashes())
        secure_files = len([f for f in os.listdir(Config.SECURE_FOLDER) if f.endswith('.enc')])
        
        return {
            "total_registrations": total_keys,
            "encrypted_files": secure_files,
            "model_loaded": predictor.is_model_loaded()
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    print(f"""
    ===============================================================
               VeriMark AI - Backend Server                    
                                                               
      API Documentation: http://localhost:{Config.API_PORT}/docs        
      Health Check:      http://localhost:{Config.API_PORT}/health      
                                                               
      Press CTRL+C to stop                                    
    ===============================================================
    """)
    
    uvicorn.run(
        app, 
        host=Config.API_HOST, 
        port=Config.API_PORT,
        log_level="info"
    )