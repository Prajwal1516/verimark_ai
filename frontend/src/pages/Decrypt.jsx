import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Unlock, Upload, Eye, Fingerprint, ShieldAlert, FileText, CheckCircle, XCircle, Download, RefreshCw, Lock } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import { accessFile, getDownloadUrl } from '../services/api';
import './Decrypt.css';

const Decrypt = () => {
    const [encryptedFile, setEncryptedFile] = useState(null);
    const [iris, setIris] = useState(null);
    const [fingerprint, setFingerprint] = useState(null);
    const [irisPreview, setIrisPreview] = useState(null);
    const [fpPreview, setFpPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleFileChange = (e, setter, previewSetter) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setter(selectedFile);

            if (previewSetter && selectedFile.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => previewSetter(e.target.result);
                reader.readAsDataURL(selectedFile);
            }
        }
    };

    const handleDecrypt = async () => {
        if (!encryptedFile || !iris || !fingerprint) {
            setResult({
                success: false,
                error: 'Please upload all required files',
            });
            return;
        }

        setLoading(true);
        setResult(null);

        const response = await accessFile(encryptedFile, iris, fingerprint);

        setLoading(false);
        setResult(response);
    };

    const handleNewDecryption = () => {
        setEncryptedFile(null);
        setIris(null);
        setFingerprint(null);
        setIrisPreview(null);
        setFpPreview(null);
        setResult(null);
    };

    return (
        <div className="decrypt-page container">
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h1 className="page-title">
                    <Unlock className="title-icon" size={40} />
                    Decrypt & Access File
                </h1>
                <p className="page-description">
                    Access your encrypted file using biometric authentication. Upload your encrypted
                    file along with the same iris and fingerprint images used during registration.
                </p>
            </motion.div>

            <motion.div
                className="decrypt-form card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
            >
                <div className="upload-grid">
                    <FileUpload
                        label="Encrypted File (.enc)"
                        accept=".enc"
                        onChange={(e) => handleFileChange(e, setEncryptedFile, null)}
                        file={encryptedFile}
                        icon={<Lock size={40} />}
                    />
                    <FileUpload
                        label="Iris Image"
                        accept="image/*"
                        onChange={(e) => handleFileChange(e, setIris, setIrisPreview)}
                        file={iris}
                        preview={irisPreview}
                        icon={<Eye size={40} />}
                    />
                    <FileUpload
                        label="Fingerprint Image"
                        accept="image/*"
                        onChange={(e) => handleFileChange(e, setFingerprint, setFpPreview)}
                        file={fingerprint}
                        preview={fpPreview}
                        icon={<Fingerprint size={40} />}
                    />
                </div>

                <div className="button-group flex gap-md mt-md">
                    <motion.button
                        className="btn btn-secondary w-full"
                        onClick={handleNewDecryption}
                        disabled={loading || (!encryptedFile && !iris && !fingerprint)}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        <RefreshCw size={20} />
                        <span>Clear Feed</span>
                    </motion.button>

                    <motion.button
                        className="btn btn-success w-full"
                        onClick={handleDecrypt}
                        disabled={loading || !encryptedFile || !iris || !fingerprint}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        {loading ? (
                            <LoadingSpinner size="sm" text="" />
                        ) : (
                            <>
                                <Unlock size={20} />
                                <span>Authenticate & Decrypt</span>
                            </>
                        )}
                    </motion.button>
                </div>
            </motion.div>

            {/* Result Display */}
            <AnimatePresence>
                {result && (
                    <motion.div
                        className={`result-card card ${result.success ? 'success' : 'error'}`}
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: -20 }}
                    >
                        <div className="result-icon">
                            {result.success ? <CheckCircle size={32} /> : <XCircle size={32} />}
                        </div>
                        <div className="result-content">
                            <h3 className="result-title">
                                {result.success ? 'Access Granted!' : 'Access Denied'}
                            </h3>
                            <p className="result-message">
                                {result.success ? result.data.message : result.error}
                            </p>

                            {result.success && result.data.decrypted_file && (
                                <div className="result-actions">
                                    <motion.a
                                        href={getDownloadUrl(result.data.decrypted_file)}
                                        download
                                        className="btn btn-primary"
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                    >
                                        <Download size={20} />
                                        <span>Download File</span>
                                    </motion.a>
                                    <motion.button
                                        onClick={handleNewDecryption}
                                        className="btn btn-secondary"
                                        whileHover={{ scale: 1.05 }}
                                        whileTap={{ scale: 0.95 }}
                                    >
                                        <RefreshCw size={20} />
                                        <span>New Decryption</span>
                                    </motion.button>
                                </div>
                            )}

                            {result.success && result.data.file_content && (
                                <div className="file-preview">
                                    <h4 className="preview-title">
                                        <FileText size={16} /> File Preview
                                    </h4>
                                    <pre className="preview-content">{result.data.file_content}</pre>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Security Notice */}
            <motion.div
                className="security-notice card"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
            >
                <h3 className="notice-title">
                    <ShieldAlert size={20} className="notice-icon" />
                    Security Notice
                </h3>
                <ul className="notice-list">
                    <li>You must use the exact same biometric images used during registration</li>
                    <li>The AI model will verify the authenticity of your biometric data</li>
                    <li>Multiple failed attempts may result in temporary lockout</li>
                    <li>Your decrypted file will be available for download immediately</li>
                    <li>For security, the decrypted file is stored temporarily</li>
                </ul>
            </motion.div>
        </div>
    );
};

export default Decrypt;
