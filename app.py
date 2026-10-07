import time
import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO

# 1. Konfigurasi Halaman & Tema Profesional
st.set_page_config(
    page_title="SafeSite AI | PPE Construction Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Desain CSS Kustom Kelas Industri (Memperbaiki visibilitas teks agar jelas terbaca)
st.markdown(
    """
    <style>
        .main {
            background-color: #0b0f19;
            color: #f1f5f9;
            font-family: 'Inter', sans-serif;
        }
        [data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1f2937;
        }
        .header-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #334155;
            margin-bottom: 24px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }
        div.stMetric {
            background-color: #1e293b;
            padding: 16px;
            border-radius: 14px;
            border: 1px solid #334155;
            border-left: 6px solid #f97316;
        }
        div.stMetric label {
            color: #cbd5e1 !important;
            font-weight: 700;
            font-size: 14px;
        }
        div.stMetric [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 24px !important;
            font-weight: 800;
        }
        /* Memastikan seluruh heading terlihat jelas */
        h1, h2, h3, h4 {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        .section-title {
            color: #ffffff !important;
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 5px;
        }
        .section-desc {
            color: #cbd5e1 !important;
            font-size: 13px;
            margin-bottom: 15px;
        }
        .status-card-safe {
            padding: 14px 20px;
            background: linear-gradient(135deg, #065f46 0%, #047857 100%);
            color: #ffffff;
            border-radius: 12px;
            text-align: center;
            font-weight: 700;
            font-size: 14px;
            border: 1px solid #10b981;
        }
        .status-card-alert {
            padding: 14px 20px;
            background: linear-gradient(135deg, #991b1b 0%, #b91c1c 100%);
            color: #ffffff;
            border-radius: 12px;
            text-align: center;
            font-weight: 700;
            font-size: 14px;
            border: 1px solid #ef4444;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.01); opacity: 0.85; }
            100% { transform: scale(1.01); opacity: 1; }
        }
        .stButton button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1rem;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Header & Branding Personal Project
st.markdown(
    """
    <div class="header-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; font-size: 26px; color: #ffffff !important;">🛡️ SafeSite AI: Construction PPE Compliance</h1>
                <p style="margin: 6px 0 0 0; color: #cbd5e1; font-size: 14px; font-weight: 600;">Autonomous Computer Vision Monitoring System — Personal Portfolio</p>
            </div>
            <div>
                <span style="background-color: rgba(16, 185, 129, 0.2); color: #34d399; padding: 8px 16px; border-radius: 30px; font-size: 12px; font-weight: bold; border: 1px solid #059669;">● SYSTEM ONLINE</span>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# 4. Sidebar Kontrol Operasional
st.sidebar.markdown(
    "### 🎛️ Panel Kontrol Operasional", unsafe_allow_html=True
)
st.sidebar.divider()

source_option = st.sidebar.selectbox(
    "Pilih Sumber Input Video",
    [
        "Simulasi Kamera Proyek (Webcam Utama)",
        "Rekaman Video Uji Coba Lapangan",
    ],
)

st.sidebar.divider()
st.sidebar.markdown("### 🚀 Aksi Sistem")
run_monitoring = st.sidebar.button(
    "🟢 Mulai Pengawasan K3", use_container_width=True
)
stop_monitoring = st.sidebar.button(
    "🔴 Hentikan Sesi", use_container_width=True
)

st.sidebar.divider()
st.sidebar.markdown(
    "<p style='color: #94a3b8; font-size: 11px; text-align: center;'>Architecture: YOLOv8n (Fine-tuned)<br>Framework: PyTorch & Streamlit</p>",
    unsafe_allow_html=True,
)

# 5. Layout Utama Dasbor (Grid 2 Kolom: Video & Panel Analitik)
col_video, col_analytics = st.columns([1.6, 1], gap="large")

with col_analytics:
    st.markdown(
        '<p class="section-title">📊 Live Telemetry & Analytics</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="section-desc">Statistik deteksi keselamatan kerja secara langsung.</p>',
        unsafe_allow_html=True,
    )

    # Kartu Metrik Utama Berdampingan
    m1, m2 = st.columns(2)
    with m1:
        metric_placeholder_1 = st.empty()
    with m2:
        metric_placeholder_2 = st.empty()

    metric_placeholder_1.metric(label="Total Pekerja", value="0 Orang")
    metric_placeholder_2.metric(label="Pelanggaran", value="0 Kasus")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title">🚨 Status Kepatuhan K3</p>',
        unsafe_allow_html=True,
    )
    status_placeholder = st.empty()
    status_placeholder.markdown(
        '<div class="status-card-safe">✅ SISTEM SIAP - MENUNGGU AKTIVASI</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title">📝 Log Aktivitas Sistem</p>',
        unsafe_allow_html=True,
    )
    log_container = st.container(height=180)
    with log_container:
        st.caption(
            "🕒 [00:00:00] Model YOLOv8 lokal dimuat. Siap memantau area..."
        )

with col_video:
    st.markdown(
        '<p class="section-title">🎥 Live Feed CCTV - Zona Konstruksi Utama</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="section-desc">Tangkapan visual area kerja dengan bounding box otomatis.</p>',
        unsafe_allow_html=True,
    )

    video_frame_placeholder = st.empty()
    video_frame_placeholder.markdown(
        """
        <div style="background: linear-gradient(135deg, #111827 0%, #1f2937 100%); border: 2px dashed #4b5563; border-radius: 16px; height: 380px; display: flex; flex-direction: column; justify-content: center; align-items: center; color: #cbd5e1;">
            <p style="font-size: 48px; margin: 0;">📹</p>
            <p style="font-size: 16px; font-weight: 700; color: #ffffff; margin-top: 10px;">Aliran Kamera Belum Aktif</p>
            <p style="font-size: 13px; color: #cbd5e1;">Klik tombol <strong style='color: #38bdf8;'>'Mulai Pengawasan K3'</strong> di sidebar.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# 6. Bagian Tambahan: Galeri Referensi Kasus Lapangan (Full APD vs Pelanggaran)
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    '<p class="section-title" style="font-size: 22px;">🔍 Referensi Visual Model: Kepatuhan vs Pelanggaran APD</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="section-desc">Contoh hasil analisis model dalam mendeteksi pekerja sesuai standar keselamatan konstruksi.</p>',
    unsafe_allow_html=True,
)

col_ref1, col_ref2 = st.columns(2, gap="medium")

with col_ref1:
    st.markdown(
        """
        <div style="background-color: #1e293b; padding: 18px; border-radius: 12px; border: 1px solid #10b981;">
            <h4 style="color: #34d399 !important; margin-top: 0; font-weight: 800;">🟢 Kondisi 1: Pekerja Patuh (Full APD)</h4>
            <p style="color: #cbd5e1; font-size: 13px; margin-bottom: 10px; font-weight: 500;">Model mendeteksi penggunaan helm keselamatan (hardhat) dan rompi (vest) secara lengkap.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.info(
        "💡 Status: Terdeteksi Label [helmet] & [vest] dengan Confidence Tinggi."
    )

with col_ref2:
    st.markdown(
        """
        <div style="background-color: #1e293b; padding: 18px; border-radius: 12px; border: 1px solid #ef4444;">
            <h4 style="color: #f87171 !important; margin-top: 0; font-weight: 800;">🔴 Kondisi 2: Pelanggaran K3 (Tanpa APD)</h4>
            <p style="color: #cbd5e1; font-size: 13px; margin-bottom: 10px; font-weight: 500;">Model mendeteksi pekerja beraktivitas di zona konstruksi tanpa menggunakan pelindung kepala/rompi.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.error("⚠️ Status: Terdeteksi Label [no-helmet] / [no-vest] (Trigger Alarm)")

# 7. Logika Eksekusi Model & Video Stream (Menggunakan YOLOv8n)
if run_monitoring:
    try:
        model = YOLO("best.pt")
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")

    cap = cv2.VideoCapture(0)

    while cap.isOpened() and not stop_monitoring:
        ret, frame = cap.read()
        if not ret:
            st.error("Gagal terhubung ke perangkat kamera utama.")
            break

        results = model(frame, conf=0.5)
        annotated_frame = results[0].plot()

        boxes = results[0].boxes
        num_persons = 0
        num_violations = 0

        for box in boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id].lower()
            if "person" in cls_name:
                num_persons += 1
            if "no-helmet" in cls_name or "no-vest" in cls_name:
                num_violations += 1

        metric_placeholder_1.metric(label="Total Pekerja", value=f"{num_persons} Org")
        metric_placeholder_2.metric(
            label="Pelanggaran",
            value=f"{num_violations} Kasus",
            delta="Aman" if num_violations == 0 else "Bahaya",
            delta_color="normal" if num_violations == 0 else "inverse",
        )

        if num_violations > 0:
            status_placeholder.markdown(
                '<div class="status-card-alert">⚠️ PERINGATAN: PELANGGARAN K3 TERDETEKSI!</div>',
                unsafe_allow_html=True,
            )
        else:
            status_placeholder.markdown(
                '<div class="status-card-safe">✅ KONDISI LAPANGAN AMAN & PATUH K3</div>',
                unsafe_allow_html=True,
            )

        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        video_frame_placeholder.image(
            annotated_frame, channels="RGB", use_column_width=True
        )


    cap.release()