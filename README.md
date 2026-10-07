SafeSite AI: Autonomous Construction PPE Compliance System

An end-to-end computer vision and web-based dashboard solution designed for real-time Personal Protective Equipment (PPE) compliance monitoring in construction zones.

🌟 Overview

SafeSite AI is a portfolio-grade computer vision project developed to automate safety compliance enforcement on active construction sites. Built using a custom-trained YOLO model, the system processes video streams (webcam or prerecorded footage) to detect construction workers and verify whether they are properly equipped with mandatory safety gear (such as hardhats and high-visibility vests).

The system features an industrial-grade, dark-themed Streamlit control dashboard that provides real-time telemetry, automated violation alerts, and safety status metrics without cluttering the interface with unnecessary parameters.

🚀 Key Features

Real-Time Object Detection: Powered by a fine-tuned Ultralytics YOLO model optimized for high-speed edge and local processing.

Automated Safety Telemetry: Instantly counts active personnel, logs safety violations (e.g., missing helmets or vests), and triggers dynamic alert cards.

Industrial UI/UX Dashboard: Built with custom CSS and modern HTML styling, offering a clean, professional "control room" aesthetic tailored for portfolio demonstration.

Zero-Latency Optimization: Configured for smooth, uninterrupted video frame rendering.

Visual Case Reference: Includes built-in reference cards demonstrating model capabilities under compliant vs. non-compliant conditions.

🛠️ Tech Stack

Core Language: Python

Computer Vision & AI: Ultralytics YOLOv8/v11, OpenCV, PyTorch

Web Framework & UI: Streamlit, Custom HTML/CSS (Industrial Dark Theme)

Version Control: Git & GitHub

📂 Project Structure

apd_constructions/
│
├── app.py                  # Main Streamlit dashboard application
├── best.pt                 # Custom-trained YOLO model weights
├── requirements.txt        # Required Python packages
└── README.md               # Project documentation


⚙️ Installation & Setup

Follow these steps to run the project locally on your machine:

Clone the repository:

git clone https://github.com/YOUR-USERNAME/construction-ppe-detection.git
cd construction-ppe-detection


Install dependencies:

pip install -r requirements.txt


Ensure model weights are in place:

Place your trained best.pt file directly into the root project directory (same folder as app.py).

Run the Streamlit application:

streamlit run app.py


Access the dashboard:

Open your web browser and navigate to http://localhost:8501.

📊 Dashboard Preview & Workflow

Open the sidebar and select your input video source (Webcam or Field Footage).

Click "🟢 Mulai Pengawasan K3" to activate the real-time AI monitoring loop.

Observe live metrics, bounding box annotations on the video feed, and instant safety alerts if a violation is detected.

Click "🔴 Hentikan Sesi" to safely terminate the monitoring session.

👤 Author

Your Name

GitHub: @atsalhfdz5
LinkedIn: atsalhafidz

📄 License

This project is open-source and available under the MIT License.