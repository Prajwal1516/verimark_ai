# VeriMark AI 🛡️

**VeriMark AI** is a cutting-edge biometric file encryption system that combines military-grade encryption with AI-powered biometric authentication. It uses iris and fingerprint data to generate unique watermarks and encryption keys, ensuring that your sensitive files are accessible only by you.

## 🚀 Features

-   **Biometric Authentication:** Secure registration and access using Iris and Fingerprint scanning (simulated via image upload).
-   **AI-Powered Validation:** Deep learning models validate the authenticity of biometric data.
-   **Military-Grade Encryption:** Files are encrypted using AES (Fernet) with keys derived from unique biometric hashes.
-   **Secure Watermarking:** Generates a visual watermark combining your biometric traits.
-   **Modern UI:** A sleek, responsive, and "Cyber-Security" themed interface built with React and Tailwind CSS.
-   **Rate Limiting:** Protects against brute-force attacks.

## 🛠️ Tech Stack

### Frontend
-   **Framework:** React (Vite)
-   **Styling:** Tailwind CSS, CSS Modules
-   **Animations:** Framer Motion
-   **Icons:** Lucide React

### Backend
-   **Framework:** Python (FastAPI)
-   **Image Processing:** Pillow (PIL)
-   **Encryption:** Cryptography (Fernet)
-   **AI/ML:** PyTorch (for biometric model)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
-   **Node.js** (v16 or higher)
-   **Python** (v3.8 or higher)
-   **Git**

## ⚙️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Prajwal1516/verimark_ai.git
    cd verimark-ai
    ```

2.  **Backend Setup**
    Navigate to the root directory (where `api.py` is located).
    ```bash
    # Create a virtual environment (optional but recommended)
    python -m venv venv
    
    # Activate virtual environment
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate

    # Install dependencies
    pip install -r backend/requirements.txt
    ```

3.  **Frontend Setup**
    Navigate to the frontend directory.
    ```bash
    cd frontend
    npm install
    ```

## 🏃‍♂️ Running the Application

You need to run both the backend and frontend servers.

### 1. Start the Backend Server
From the root directory:
```bash
python api.py
```
The backend API will start at `http://localhost:8000`.
-   Docs: `http://localhost:8000/docs`
-   Health Check: `http://localhost:8000/health`

### 2. Start the Frontend Server
Open a new terminal, navigate to the `frontend` directory:
```bash
cd frontend
npm run dev
```
The frontend will start at `http://localhost:5173`.

## 📖 Usage

1.  **Register:**
    -   Go to the **Encrypt File** page.
    -   Upload the file you want to protect.
    -   Upload your Iris and Fingerprint images.
    -   Click "Secure File".
    -   The system will encrypt your file and provide a download link.

2.  **Access (Decrypt):**
    -   Go to the **Decrypt File** page.
    -   Upload the encrypted `.enc` file.
    -   Upload the **same** Iris and Fingerprint images used during registration.
    -   Click "Decrypt File".
    -   If the biometrics match, you can download the original file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
