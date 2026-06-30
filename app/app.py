import streamlit as st
import pandas as pd

# Konfigurasi Halaman (Wajib di baris paling atas)
st.set_page_config(page_title="SHIELD - Dashboard Prediksi Depresi", page_icon="🛡️", layout="wide")

# ==========================================
# HEADER & INFORMASI TIM
# ==========================================
st.title("🛡️ SHIELD: Sistem Prediksi Tingkat Depresi Siswa")
st.markdown("##### *Student Health Intelligence using Explainable Learning for Depression*")

st.markdown("""
**Tugas Besar Artificial Intelligence / Machine Learning**  
👨‍💻 **Oleh:** Aisyah Nurul Sholikhah & Calista Salsabila  
🎓 Program Studi Informatika, Fakultas Teknologi Informasi dan Sains Data, Universitas Sebelas Maret
""")

st.divider()

# ==========================================
# TENTANG PROYEK (GENERAL EXPLANATION)
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📌 Tentang Aplikasi")
    st.write("Aplikasi ini merupakan implementasi dari sistem prediksi depresi berbasis *Explainable Artificial Intelligence* (XAI) yang disebut SHIELD.")
    st.write("Tujuan utama dari web ini adalah untuk mengidentifikasi tingkat depresi pada siswa secara cepat, objektif, dan akurat agar dapat mendukung proses pencegahan maupun intervensi sejak dini.")
    
    st.header("📖 Latar Belakang")
    st.write("Depresi merupakan salah satu gangguan kesehatan mental yang paling banyak dialami oleh siswa akibat tingginya tekanan akademik, perubahan lingkungan sosial, kondisi ekonomi, serta tuntutan pencapaian. Berdasarkan data WHO dan Kementerian Kesehatan RI, permasalahan kesehatan mental pada kelompok usia produktif menunjukkan tren peningkatan yang signifikan.")
    
with col2:
    st.header("⚙️ Metodologi")
    st.markdown("""
    * **Algoritma:** Random Forest Classifier
    * **Feature Selection:** SHAP (SHapley Additive exPlanations)
    * **Dataset:** 502 data siswa dari platform Kaggle
    * **Evaluasi:** Stratified 5-Fold Cross Validation
    """)
    st.info("💡 **Inovasi:** Pendekatan ini tidak hanya berfokus pada akurasi, tetapi juga memberikan transparansi (interpretabilitas) agar hasil prediksi dapat dipahami secara logis menggunakan SHAP.")

st.divider()

# ==========================================
# PERFORMA MODEL & SELEKSI FITUR
# ==========================================
st.header("🚀 Hasil & Performa Model")

st.write("Pada penelitian ini, penggunaan seluruh atribut (10 fitur) tidak selalu berkorelasi dengan performa yang optimal. Oleh karena itu, dilakukan reduksi menjadi **8 fitur terpenting** berdasarkan nilai SHAP tertinggi.")
st.write("Pemangkasan atribut ini terbukti tidak hanya menyederhanakan arsitektur model, tetapi juga mampu menghasilkan performa klasifikasi yang lebih baik dibandingkan penggunaan seluruh fitur secara utuh.")

# Menampilkan metrik performa dengan UI yang menarik
st.subheader("Perbandingan Kinerja: Model Final (8 Fitur SHAP) vs Baseline (10 Fitur)")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="Accuracy", value="90.64%", delta="Naik dari 88.84%")
with m2:
    st.metric(label="Precision", value="90.64%", delta="Naik dari 88.31%")
with m3:
    st.metric(label="Recall", value="90.85%", delta="Naik dari 89.67%")
with m4:
    st.metric(label="F1-Score", value="90.69%", delta="Naik dari 88.95%")

st.caption("Catatan: Evaluasi kinerja di atas dihasilkan dari penerapan model Random Forest hasil feature selection berbasis SHAP menggunakan skema Stratified 5-Fold Cross Validation.")

st.divider()

# ==========================================
# PANDUAN PENGGUNAAN (ALUR WEB)
# ==========================================
st.header("🗺️ Alur Penggunaan Web")
st.write("Gunakan menu navigasi di sebelah kiri (Sidebar) untuk mengeksplorasi aplikasi ini:")
st.markdown("""
1. **📊 EDA (Exploratory Data Analysis):** Melihat visualisasi distribusi data target dan sekilas tentang karakteristik dataset siswa yang digunakan.
2. **⭐ Feature Importance:** Memahami alasan di balik prediksi model dan melihat 8 fitur utama penyumbang depresi terbesar menurut analisis SHAP.
3. **🔮 Predict:** Mencoba langsung sistem deteksi dini (skrining) depresi dengan memasukkan data simulasi siswa.
""")

st.success("👈 Silakan buka sidebar di sebelah kiri untuk mulai menjalankan aplikasi!")