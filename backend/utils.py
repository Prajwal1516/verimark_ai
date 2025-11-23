"""
VeriMark AI - Utility Functions
Image processing and biometric validation
"""
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import hashlib
import logging
from typing import Tuple, Optional
from pathlib import Path
from config import Config

# Setup logging
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def open_rgb(path: str) -> Image.Image:
    """
    Open image and convert to RGB
    
    Args:
        path: Path to image file
        
    Returns:
        PIL Image in RGB format
    """
    try:
        img = Image.open(path).convert("RGB")
        return img
    except Exception as e:
        logger.error(f"Failed to open image {path}: {e}")
        raise ValueError(f"Cannot open image: {e}")


def resize_square(img: Image.Image, size: int = Config.IMG_SIZE) -> Image.Image:
    """
    Resize image to square maintaining aspect ratio
    
    Args:
        img: PIL Image
        size: Target size (will be size x size)
        
    Returns:
        Resized square PIL Image
    """
    return ImageOps.fit(img, (size, size), Image.Resampling.LANCZOS)


def rubik_permute(img: Image.Image, tiles: int = Config.RUBIK_TILES) -> Image.Image:
    """
    Apply deterministic Rubik-like tile permutation
    Splits image into tiles x tiles grid and shuffles with fixed permutation
    
    Args:
        img: PIL Image (must be square)
        tiles: Number of tiles per side (default: 8)
        
    Returns:
        Permuted PIL Image
    """
    w, h = img.size
    if w != h:
        raise ValueError("Image must be square for Rubik permutation")
    
    tile_w = w // tiles
    tile_h = h // tiles
    tiles_list = []
    
    # Extract tiles
    for i in range(tiles):
        for j in range(tiles):
            box = (j * tile_w, i * tile_h, (j + 1) * tile_w, (i + 1) * tile_h)
            tiles_list.append(img.crop(box))
    
    # Deterministic permutation using fixed seed (same as your notebook)
    rng = np.random.RandomState(12345)
    perm = rng.permutation(len(tiles_list))
    
    # Reconstruct image with permuted tiles
    new_img = Image.new('RGB', (w, h))
    idx = 0
    for i in range(tiles):
        for j in range(tiles):
            tile = tiles_list[perm[idx]]
            new_img.paste(tile, (j * tile_w, i * tile_h))
            idx += 1
    
    return new_img


def blend_watermark(
    iris_img: Image.Image, 
    fp_img: Image.Image, 
    alpha: float = Config.BLEND_ALPHA
) -> Image.Image:
    """
    Blend iris and fingerprint images to create watermark
    
    Args:
        iris_img: Iris PIL Image
        fp_img: Fingerprint PIL Image  
        alpha: Blend ratio (0.0 to 1.0)
        
    Returns:
        Blended watermark PIL Image
    """
    if iris_img.size != fp_img.size:
        raise ValueError("Images must have same dimensions for blending")
    return Image.blend(iris_img, fp_img, alpha=alpha)


def compute_image_hash(img: Image.Image) -> str:
    """
    Compute SHA-256 hash of image bytes
    
    Args:
        img: PIL Image
        
    Returns:
        Hex string of SHA-256 hash
    """
    img_bytes = img.tobytes()
    return hashlib.sha256(img_bytes).hexdigest()


def validate_file_extension(filename: str) -> bool:
    """
    Validate file extension against allowed list
    
    Args:
        filename: Name of file
        
    Returns:
        True if extension is allowed
    """
    ext = Path(filename).suffix.lower()
    return ext in Config.ALLOWED_EXTENSIONS


def validate_file_size(file_path: str) -> bool:
    """
    Validate file size against maximum limit
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file size is within limit
    """
    import os
    size = os.path.getsize(file_path)
    return size <= Config.MAX_FILE_SIZE


class BiometricValidator:
    """Validates biometric image quality"""
    
    @staticmethod
    def check_image_quality(img: Image.Image, min_size: int = 100) -> Tuple[bool, str]:
        """
        Check if image meets quality requirements
        
        Args:
            img: PIL Image to check
            min_size: Minimum dimension size (not enforced)
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Accept all images without restrictions
        return True, "Image quality acceptable"
    
    @staticmethod
    def validate_iris(img_path: str) -> Tuple[bool, str]:
        """
        Validate iris image
        
        Args:
            img_path: Path to iris image
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            img = open_rgb(img_path)
            return BiometricValidator.check_image_quality(img)
        except Exception as e:
            return False, f"Invalid iris image: {str(e)}"
    
    @staticmethod
    def validate_fingerprint(img_path: str) -> Tuple[bool, str]:
        """
        Validate fingerprint image
        
        Args:
            img_path: Path to fingerprint image
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            img = open_rgb(img_path)
            return BiometricValidator.check_image_quality(img)
        except Exception as e:
            return False, f"Invalid fingerprint image: {str(e)}"


# Helper function for dataset collection (used in training)
def collect_images(root_path):
    """
    Collect biometric images from dataset folder
    Used during training/testing
    
    Args:
        root_path: Path to biometric_data folder
        
    Returns:
        Dictionary with iris and fingerprint image paths
    """
    from glob import glob
    import os
    
    iris_root = os.path.join(root_path, "iris")
    fp_root = os.path.join(root_path, "fingerprint")
    
    iris_classes = sorted([d for d in os.listdir(iris_root) 
                          if os.path.isdir(os.path.join(iris_root, d))])
    fp_classes = sorted([d for d in os.listdir(fp_root) 
                        if os.path.isdir(os.path.join(fp_root, d))])
    
    data = {"iris": {}, "fingerprint": {}}
    
    for c in iris_classes:
        data["iris"][c] = sorted(glob(os.path.join(iris_root, c, "*")))
    
    for c in fp_classes:
        data["fingerprint"][c] = sorted(glob(os.path.join(fp_root, c, "*")))
    
    return data