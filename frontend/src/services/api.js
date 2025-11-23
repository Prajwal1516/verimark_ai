import axios from 'axios';

// API base URL - uses Vite proxy in development
const API_BASE_URL = import.meta.env.PROD
    ? 'http://localhost:8000'
    : '/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'multipart/form-data',
    },
});

/**
 * Register and encrypt a file with biometric authentication
 * @param {File} file - File to encrypt
 * @param {File} iris - Iris image
 * @param {File} fingerprint - Fingerprint image
 * @returns {Promise} Response with encrypted file info
 */
export const registerFile = async (file, iris, fingerprint) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('iris', iris);
    formData.append('fingerprint', fingerprint);

    try {
        const response = await api.post('/register', formData);
        return { success: true, data: response.data };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.detail || error.message || 'Registration failed',
        };
    }
};

/**
 * Access and decrypt a file with biometric authentication
 * @param {File} encryptedFile - Encrypted .enc file
 * @param {File} iris - Iris image
 * @param {File} fingerprint - Fingerprint image
 * @returns {Promise} Response with decrypted file info
 */
export const accessFile = async (encryptedFile, iris, fingerprint) => {
    const formData = new FormData();
    formData.append('encrypted_file', encryptedFile);
    formData.append('iris', iris);
    formData.append('fingerprint', fingerprint);

    try {
        const response = await api.post('/access', formData);
        return { success: true, data: response.data };
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.detail || error.message || 'Access denied',
        };
    }
};

/**
 * Get download URL for a decrypted file
 * @param {string} filename - Name of the file to download
 * @returns {string} Download URL
 */
export const getDownloadUrl = (filename) => {
    return `${API_BASE_URL}/download/${filename}`;
};

/**
 * Check backend health status
 * @returns {Promise} Health status
 */
export const checkHealth = async () => {
    try {
        const response = await api.get('/health');
        return { success: true, data: response.data };
    } catch (error) {
        return {
            success: false,
            error: 'Backend is offline',
        };
    }
};

/**
 * Get system statistics
 * @returns {Promise} System stats
 */
export const getStats = async () => {
    try {
        const response = await api.get('/stats');
        return { success: true, data: response.data };
    } catch (error) {
        return {
            success: false,
            error: error.message,
        };
    }
};

export default api;
