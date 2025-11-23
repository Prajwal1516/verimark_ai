import { Sun, Moon } from 'lucide-react';
import { motion } from 'framer-motion';
import { useTheme } from '../context/ThemeContext';
import './ThemeToggle.css';

const ThemeToggle = () => {
    const { theme, toggleTheme } = useTheme();

    return (
        <motion.button
            className="theme-toggle-btn"
            onClick={toggleTheme}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
            <motion.div
                initial={false}
                animate={{
                    rotate: theme === 'light' ? 0 : 180,
                    scale: theme === 'light' ? 1 : 0
                }}
                transition={{ duration: 0.3 }}
                style={{ position: 'absolute' }}
            >
                <Sun className="theme-icon sun" size={24} />
            </motion.div>

            <motion.div
                initial={false}
                animate={{
                    rotate: theme === 'dark' ? 0 : -180,
                    scale: theme === 'dark' ? 1 : 0
                }}
                transition={{ duration: 0.3 }}
                style={{ position: 'absolute' }}
            >
                <Moon className="theme-icon moon" size={24} />
            </motion.div>
        </motion.button>
    );
};

export default ThemeToggle;
