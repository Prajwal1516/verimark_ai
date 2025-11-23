import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Lock, Upload, Eye, Fingerprint, ShieldCheck, AlertTriangle, FileText, CheckCircle, XCircle } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import LoadingSpinner from '../components/LoadingSpinner';
import { registerFile } from '../services/api';
import './Register.css';

const Register = () => {
    const [file, setFile] = useState(null);
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

    const handleRegister = async () => {
        if (!file || !iris || !fingerprint) {
            setResult({
                success: false,
                error: 'Please upload all required files',
            });
            return;
        }

        setLoading(true);
        setResult(null);

        const response = await registerFile(file, iris, fingerprint);

        setLoading(false);
        setResult(response);

        // Clear form on success
        if (response.success) {
            setTimeout(() => {
                setFile(null);
                setIris(null);
                setFingerprint(null);
                setIrisPreview(null);
                setFpPreview(null);
            }, 3000);
        }
    };

    const handleClear = () => {
        setFile(null);
        setIris(null);
        setFingerprint(null);
        setIrisPreview(null);
        setFpPreview(null);
        setResult(null);
    };

    return (
        <div className="register-page container">
            <motion.div
                className="page-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h1 className="page-title">
                    <Lock className="title-icon" size={40} />
                    Register & Encrypt File
                </h1>
                <p className="page-description">
                    Secure your file with biometric authentication. Upload your file along with
                    your iris and fingerprint images to create an encrypted version.
                </p>
            </motion.div>

            <motion.div
                className="register-form card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
            >
                <div className="upload-grid">
                    <FileUpload
                        label="File to Protect"
                        accept="*"
                        onChange={(e) => handleFileChange(e, setFile, null)}
                        file={file}
                        icon={<FileText size={40} />}
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
                        onClick={handleClear}
                        disabled={loading || (!file && !iris && !fingerprint)}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        <XCircle size={20} />
                        <span>Clear Feed</span>
                    </motion.button>

                    <motion.button
                        className="btn btn-primary w-full"
                        onClick={handleRegister}
                        disabled={loading || !file || !iris || !fingerprint}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                    >
                        {loading ? (
                            <LoadingSpinner size="sm" text="" />
                        ) : (
                            <>
                                <ShieldCheck size={20} />
                                <span>Register & Encrypt</span>
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
                                {result.success ? 'Success!' : 'Error'}
                            </h3>
                            <p className="result-message">
                                {result.success ? result.data.message : result.error}
                            </p>
                            {result.success && result.data.encrypted_file && (
                                <div className="result-details">
                                    <div className="detail-item">
                                        <span className="detail-icon"><Lock size={16} /></span>
                                        <span className="detail-text">
                                            Encrypted file: <strong>{result.data.encrypted_file}</strong>
                                        </span>
                                    </div>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Info Section */}
            <motion.div
                className="info-section card"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
            >
                <h3 className="info-title">
                    <AlertTriangle size={20} className="info-icon" />
                    Important Information
                </h3>
                <ul className="info-list">
                    <li>Your biometric images must be clear and well-lit</li>
                    <li>The encrypted file will be saved with a .enc extension</li>
                    <li>Keep your biometric images safe - they are your only keys</li>
                    <li>Maximum file size: 100MB</li>
                    <li>The AI model validates biometric authenticity before encryption</li>
                </ul>
            </motion.div>
        </div>
    );
};

export default Register;
