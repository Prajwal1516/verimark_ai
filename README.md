# VeriMark AI 

**VeriMark AI** is a cutting-edge biometric file encryption system that combines military-grade encryption with AI-powered biometric authentication. It uses iris and fingerprint data to generate unique watermarks and encryption keys, ensuring that your sensitive files are accessible only by you.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-20232A?logo=react&logoColor=61DAFB)
![HTML](https://img.shields.io/badge/Markup-HTML5-E34F26?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/Style-CSS3-1572B6?logo=css3&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
![AI/ML](https://img.shields.io/badge/Domain-AI%2FML-FF6F00)
![ACS Algorithm](https://img.shields.io/badge/Optimization-ACS-blueviolet)

<img width="1920" height="870" alt="{31B5CED8-A39F-475D-B9DF-E0D8C8C0636F}" src="https://github.com/user-attachments/assets/201ed54b-11ae-4f3c-bc98-f6fff6703154" />
Screenshot of the application in dark mode.


##  Features

-   **Biometric Authentication:** Secure registration and access using Iris and Fingerprint scanning (simulated via image upload).
-   **AI-Powered Validation:** Deep learning models validate the authenticity of biometric data.
-   **Military-Grade Encryption:** Files are encrypted using AES (Fernet) with keys derived from unique biometric hashes.
-   **Secure Watermarking:** Generates a visual watermark combining your biometric traits.
-   **Modern UI:** A sleek, responsive, and "Cyber-Security" themed interface built with React and Tailwind CSS.
-   **Rate Limiting:** Protects against brute-force attacks.

##  Tech Stack

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

##  Prerequisites

Before you begin, ensure you have the following installed:
-   **Node.js** (v16 or higher)
-   **Python** (v3.8 or higher)
-   **Git**

##  Installation

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

##  Running the Application

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

##  Usage

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

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
