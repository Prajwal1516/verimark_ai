"""
VeriMark AI - Enhanced Security Module
Encryption, key management, and access control
"""
import json
import os
import time
from typing import Optional, Dict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)


class SecureKeyManager:
    """Secure key management with encryption"""
    
    def __init__(self, master_password: str = None):
        """
        Initialize with optional master password
        
        Args:
            master_password: Password for key encryption (uses default if None)
        """
        self.key_file = Config.KEY_FILE
        self.master_key = self._derive_master_key(master_password or "verimark_default_master_key_2024")
        self.fernet = Fernet(self.master_key)
    
    def _derive_master_key(self, password: str) -> bytes:
        """
        Derive encryption key from master password using PBKDF2
        
        Args:
            password: Master password
            
        Returns:
            Derived encryption key
        """
        # In production, use random salt stored securely
        salt = b'verimark_salt_v1_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def load_keys(self) -> Dict[str, str]:
        """
        Load and decrypt keys from file
        
        Returns:
            Dictionary of watermark_hash -> encryption_key mappings
        """
        if not os.path.exists(self.key_file):
            logger.info("Key file not found, creating new one")
            return {}
        
        try:
            with open(self.key_file, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            keys = json.loads(decrypted_data.decode())
            logger.info(f"Loaded {len(keys)} keys from storage")
            return keys
        except Exception as e:
            logger.error(f"Failed to load keys: {e}")
            return {}
    
    def save_keys(self, keys: Dict[str, str]) -> bool:
        """
        Encrypt and save keys to file
        
        Args:
            keys: Dictionary of watermark_hash -> encryption_key mappings
            
        Returns:
            True if successful
        """
        try:
            json_data = json.dumps(keys, indent=2).encode()
            encrypted_data = self.fernet.encrypt(json_data)
            
            # Ensure directory exists
            self.key_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.key_file, "wb") as f:
                f.write(encrypted_data)
            
            logger.info(f"Saved {len(keys)} keys to storage")
            return True
        except Exception as e:
            logger.error(f"Failed to save keys: {e}")
            return False
    
    def add_key(self, watermark_hash: str, encryption_key: bytes) -> bool:
        """
        Add a new biometric key mapping
        
        Args:
            watermark_hash: Hash of the watermark
            encryption_key: Fernet encryption key
            
        Returns:
            True if successful
        """
        keys = self.load_keys()
        keys[watermark_hash] = encryption_key.decode()
        return self.save_keys(keys)
    
    def get_key(self, watermark_hash: str) -> Optional[bytes]:
        """
        Retrieve encryption key for watermark hash
        
        Args:
            watermark_hash: Hash of the watermark
            
        Returns:
            Encryption key if found, None otherwise
        """
        keys = self.load_keys()
        key_str = keys.get(watermark_hash)
        return key_str.encode() if key_str else None
    
    def remove_key(self, watermark_hash: str) -> bool:
        """
        Remove a biometric key mapping
        
        Args:
            watermark_hash: Hash of the watermark
            
        Returns:
            True if successful
        """
        keys = self.load_keys()
        if watermark_hash in keys:
            del keys[watermark_hash]
            return self.save_keys(keys)
        return False
    
    def list_all_hashes(self) -> list:
        """
        Get list of all stored watermark hashes
        
        Returns:
            List of watermark hashes
        """
        keys = self.load_keys()
        return list(keys.keys())


class FileEncryption:
    """Handle file encryption and decryption"""
    
    @staticmethod
    def encrypt_file(file_path: str, key: bytes) -> Optional[str]:
        """
        Encrypt a file and return encrypted file path
        
        Args:
            file_path: Path to file to encrypt
            key: Fernet encryption key
            
        Returns:
            Path to encrypted file, or None if failed
        """
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            
            # Save to secure folder
            Config.SECURE_FOLDER.mkdir(parents=True, exist_ok=True)
            filename = os.path.basename(file_path)
            enc_path = os.path.join(Config.SECURE_FOLDER, f"{filename}.enc")
            
            with open(enc_path, "wb") as ef:
                ef.write(encrypted)
            
            logger.info(f"Encrypted file: {filename}")
            return enc_path
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return None
    
    @staticmethod
    def decrypt_file(enc_path: str, key: bytes) -> Optional[str]:
        """
        Decrypt a file and return decrypted file path
        
        Args:
            enc_path: Path to encrypted file
            key: Fernet encryption key
            
        Returns:
            Path to decrypted file, or None if failed
        """
        try:
            with open(enc_path, "rb") as ef:
                encrypted = ef.read()
            
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted)
            
            # Remove .enc extension
            base = os.path.basename(enc_path)
            if base.endswith(".enc"):
                base = base[:-4]
            
            dec_path = os.path.join(Config.SECURE_FOLDER, f"decrypted_{base}")
            
            with open(dec_path, "wb") as df:
                df.write(decrypted)
            
            logger.info(f"Decrypted file: {base}")
            return dec_path
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return None


class AccessControl:
    """Rate limiting and access control"""
    
    def __init__(self):
        self.attempts: Dict[str, list] = {}
        self.locked_hashes: Dict[str, float] = {}
    
    def check_rate_limit(self, watermark_hash: str) -> tuple:
        """
        Check if access attempts are within rate limit
        
        Args:
            watermark_hash: Hash to check
            
        Returns:
            Tuple of (allowed, message)
        """
        current_time = time.time()
        
        # Check if locked out
        if watermark_hash in self.locked_hashes:
            lockout_end = self.locked_hashes[watermark_hash]
            if current_time < lockout_end:
                remaining = int(lockout_end - current_time)
                return False, f"Account locked. Try again in {remaining} seconds"
            else:
                # Lockout expired
                del self.locked_hashes[watermark_hash]
                self.attempts[watermark_hash] = []
        
        # Clean old attempts (older than 1 hour)
        if watermark_hash in self.attempts:
            self.attempts[watermark_hash] = [
                t for t in self.attempts[watermark_hash] 
                if current_time - t < 3600
            ]
        else:
            self.attempts[watermark_hash] = []
        
        # Check attempt count
        if len(self.attempts[watermark_hash]) >= Config.MAX_LOGIN_ATTEMPTS:
            # Lock account
            self.locked_hashes[watermark_hash] = current_time + Config.LOCKOUT_DURATION
            logger.warning(f"Account locked due to excessive attempts: {watermark_hash[:8]}...")
            return False, f"Too many attempts. Account locked for {Config.LOCKOUT_DURATION} seconds"
        
        # Record attempt
        self.attempts[watermark_hash].append(current_time)
        return True, "OK"
    
    def clear_attempts(self, watermark_hash: str):
        """
        Clear attempts for successful authentication
        
        Args:
            watermark_hash: Hash to clear
        """
        if watermark_hash in self.attempts:
            self.attempts[watermark_hash] = []
        if watermark_hash in self.locked_hashes:
            del self.locked_hashes[watermark_hash]


# Global instances (singleton pattern)
key_manager = SecureKeyManager()
access_control = AccessControl()