import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './FileUpload.css';

const FileUpload = ({ label, accept, onChange, file, preview, icon = '📁' }) => {
    const [dragOver, setDragOver] = useState(false);

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setDragOver(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onChange({ target: { files: e.dataTransfer.files } });
        }
    };

    const handleFileChange = (e) => {
        onChange(e);
    };

    const inputId = `file-upload-${label.replace(/\s+/g, '-').toLowerCase()}`;

    return (
        <div className="file-upload-wrapper">
            <label className="file-upload-label">{label}</label>

            <motion.div
                className={`file-upload-box ${dragOver ? 'drag-over' : ''} ${file ? 'has-file' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
            >
                <input
                    type="file"
                    id={inputId}
                    accept={accept}
                    onChange={handleFileChange}
                    className="file-input"
                />

                <label htmlFor={inputId} className="file-upload-content">
                    <AnimatePresence mode="wait">
                        {preview ? (
                            <motion.div
                                key="preview"
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.8 }}
                                className="file-preview"
                            >
                                <img src={preview} alt="Preview" className="preview-image" />
                                <p className="preview-text">Click to change</p>
                            </motion.div>
                        ) : file ? (
                            <motion.div
                                key="file"
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.8 }}
                                className="file-info"
                            >
                                <div className="file-icon">📄</div>
                                <p className="file-name">{file.name}</p>
                                <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
                                <p className="file-change-text">Click to change</p>
                            </motion.div>
                        ) : (
                            <motion.div
                                key="empty"
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.8 }}
                                className="file-empty"
                            >
                                <motion.div
                                    className="upload-icon"
                                    animate={{ y: [0, -10, 0] }}
                                    transition={{ duration: 2, repeat: Infinity }}
                                >
                                    {icon}
                                </motion.div>
                                <p className="upload-text">Click or drag to upload</p>
                                <p className="upload-subtext">{label}</p>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </label>
            </motion.div>
        </div>
    );
};

export default FileUpload;
