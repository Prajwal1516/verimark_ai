import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Navbar.css';

const Navbar = () => {
    const location = useLocation();

    const isActive = (path) => location.pathname === path;

    return (
        <motion.nav
            className="navbar glass"
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <div className="navbar-container container">
                <Link to="/" className="navbar-brand">
                    <motion.div
                        className="brand-icon"
                        whileHover={{ rotate: 360, scale: 1.1 }}
                        transition={{ duration: 0.5 }}
                    >
                        🔐
                    </motion.div>
                    <div className="brand-text">
                        <h1 className="brand-title">VeriMark AI</h1>
                        <p className="brand-subtitle">Biometric Security</p>
                    </div>
                </Link>

                <div className="navbar-links">
                    <Link
                        to="/"
                        className={`nav-link ${isActive('/') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">🏠</span>
                        <span>Home</span>
                    </Link>
                    <Link
                        to="/register"
                        className={`nav-link ${isActive('/register') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">🔒</span>
                        <span>Register</span>
                    </Link>
                    <Link
                        to="/decrypt"
                        className={`nav-link ${isActive('/decrypt') ? 'active' : ''}`}
                    >
                        <span className="nav-icon">🔓</span>
                        <span>Decrypt</span>
                    </Link>
                </div>
            </div>
        </motion.nav>
    );
};

export default Navbar;
