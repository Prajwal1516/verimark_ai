import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ParticleBackground from './components/ParticleBackground';
import Home from './pages/Home';
import Register from './pages/Register';
import Decrypt from './pages/Decrypt';
import './App.css';

import { ThemeProvider } from './context/ThemeContext';
import ThemeToggle from './components/ThemeToggle';

function App() {
    return (
        <ThemeProvider>
            <Router>
                <div className="app">
                    {/* Animated Background */}
                    <div className="gradient-bg"></div>
                    <ParticleBackground />

                    <ThemeToggle />

                    {/* Main Content */}
                    <div className="app-content">
                        <Navbar />
                        <main className="main-content">
                            <Routes>
                                <Route path="/" element={<Home />} />
                                <Route path="/register" element={<Register />} />
                                <Route path="/decrypt" element={<Decrypt />} />
                            </Routes>
                        </main>

                        {/* Footer */}
                        <footer className="app-footer">
                            <div className="container">
                                <p className="footer-text">
                                    🏛️ SJB Institute of Technology
                                </p>
                                <p className="footer-subtext">
                                    VeriMark AI - Secure Your Files with Biometric Authentication
                                </p>
                            </div>
                        </footer>
                    </div>
                </div>
            </Router>
        </ThemeProvider>
    );
}

export default App;
