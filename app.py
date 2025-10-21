import streamlit as st
import subprocess
import os
from pathlib import Path
from PIL import Image

# Judul halaman
st.set_page_config(page_title="YOLO Object Detection", layout="wide")
st.title("📦 YOLO Object Detection App")
st.markdown("Unggah gambar dan deteksi objek menggunakan model YOLO!")

# Path model
MODEL_PATH = "my_model.onnx"
if not os.path.exists(MODEL_PATH):
    st.error("❌ File model 'my_model.onnx' tidak ditemukan di folder aplikasi.")
    st.stop()

# Input gambar
uploaded_file = st.file_uploader("📤 Upload gambar untuk deteksi:", type=["jpg", "jpeg", "png"])

# Folder hasil
RUNS_DIR = Path("runs/streamlit")
RUNS_DIR.mkdir(parents=True, exist_ok=True)

if uploaded_file:
    # Simpan sementara gambar
    input_path = Path("input.jpg")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(uploaded_file, caption="Gambar Input", use_column_width=True)

    if st.button("🚀 Deteksi Sekarang"):
        with st.spinner("Sedang memproses deteksi..."):
            # Jalankan YOLO melalui yolo_detect.py
            cmd = [
                "python", "yolo_detect.py",
                "--model", str(MODEL_PATH),
                "--source", str(input_path),
                "--save_dir", str(RUNS_DIR)
            ]
            subprocess.run(cmd, check=False)

        # Cari hasil output
        result_files = sorted(RUNS_DIR.glob("result_*.jpg"))
        if result_files:
            st.success("✅ Deteksi selesai!")
            st.image(str(result_files[-1]), caption="Hasil Deteksi", use_column_width=True)
        else:
            st.warning("⚠️ Tidak ditemukan file hasil deteksi.")
