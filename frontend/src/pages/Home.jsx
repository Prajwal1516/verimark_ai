import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { checkHealth } from '../services/api';
import { Shield, Lock, Cpu, Zap } from 'lucide-react';
import './Home.css';

const Home = () => {
    const [backendStatus, setBackendStatus] = useState(null);

    useEffect(() => {
        // Check backend health
        checkHealth().then((result) => {
            setBackendStatus(result.success ? result.data : null);
        });
    }, []);

    const features = [
        {
            icon: <Shield size={32} />,
            title: 'Biometric Security',
            description: 'Advanced iris and fingerprint authentication for maximum security',
            color: '#f97316'
        },
        {
            icon: <Lock size={32} />,
            title: 'File Encryption',
            description: 'Military-grade encryption to protect your sensitive files',
            color: '#3b82f6'
        },
        {
            icon: <Cpu size={32} />,
            title: 'AI-Powered',
            description: 'Deep learning model validates biometric authenticity',
            color: '#10b981'
        },
        {
            icon: <Zap size={32} />,
            title: 'Fast & Secure',
            description: 'Quick processing with enterprise-level security standards',
            color: '#8b5cf6'
        },
    ];

    return (
        <div className="home-page">
            {/* Hero Section */}
            <motion.section
                className="hero-section"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
            >
                <div className="hero-content">
                    <motion.div
                        className="hero-icon"
                        animate={{ rotate: [0, 10, -10, 0] }}
                        transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
                    >
                        🛡️
                    </motion.div>

                    <h1 className="hero-title">
                        Secure Your Files with
                        <span className="gradient-text"> Biometric Authentication</span>
                    </h1>

                    <p className="hero-description">
                        VeriMark AI combines cutting-edge biometric technology with military-grade encryption
                        to provide unparalleled file security. Your iris and fingerprint are the only keys.
                    </p>

                    <div className="hero-actions">
                        <Link to="/register" className="btn btn-primary btn-lg">
                            <span>🔒</span>
                            <span>Encrypt File</span>
                        </Link>
                        <Link to="/decrypt" className="btn btn-success btn-lg">
                            <span>🔓</span>
                            <span>Decrypt File</span>
                        </Link>
                    </div>

                    {/* Backend Status */}
                    {backendStatus && (
                        <motion.div
                            className="status-badge"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.5 }}
                        >
                            <span className="status-indicator active"></span>
                            <span>Backend Online</span>
                        </motion.div>
                    )}
                </div>
            </motion.section>

            {/* Features Section */}
            <section className="features-section container">
                <motion.h2
                    className="section-title"
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                >
                    Why Choose VeriMark AI?
                </motion.h2>

                <div className="features-grid">
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            className="feature-card"
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ y: -5 }}
                            style={{ '--accent-color': feature.color }}
                        >
                            <div className="feature-content">
                                <div className="feature-icon-box">
                                    {feature.icon}
                                </div>
                                <h3 className="feature-title">{feature.title}</h3>
                                <p className="feature-description">{feature.description}</p>
                            </div>
                            <div className="feature-glow"></div>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* How It Works Section */}
            <section className="how-it-works-section">
                <motion.h2
                    className="section-title"
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                >
                    How It Works
                </motion.h2>

                <div className="steps-container">
                    <motion.div
                        className="step-card card"
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                    >
                        <div className="step-number">1</div>
                        <h3>Upload Biometrics</h3>
                        <p>Provide your iris and fingerprint images for authentication</p>
                    </motion.div>

                    <motion.div
                        className="step-arrow"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                    >
                        →
                    </motion.div>

                    <motion.div
                        className="step-card card"
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                    >
                        <div className="step-number">2</div>
                        <h3>AI Verification</h3>
                        <p>Our deep learning model validates your biometric data</p>
                    </motion.div>

                    <motion.div
                        className="step-arrow"
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                    >
                        →
                    </motion.div>

                    <motion.div
                        className="step-card card"
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.4 }}
                    >
                        <div className="step-number">3</div>
                        <h3>Secure Encryption</h3>
                        <p>Your file is encrypted with a unique biometric key</p>
                    </motion.div>
                </div>
            </section>
        </div>
    );
};

export default Home;
