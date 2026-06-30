import streamlit as st
import pandas as pd
import joblib
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Predict", page_icon="🔮", layout="wide")

@st.cache_resource
def load_model():
    # Load model dari folder src
    return joblib.load('src/model_depresi_8_fitur.pkl')

model = load_model()

# Fitur diurutkan persis seperti array SHAP
TOP_8_FEATURES = [
    'Have you ever had suicidal thoughts ?', 'Academic Pressure', 'Financial Stress', 
    'Age', 'Study Satisfaction', 'Study Hours', 'Dietary Habits', 'Sleep Duration'
]

st.title("🔮 SHIELD: Deteksi Dini Depresi")
st.write("Silakan masukkan data profil dan kebiasaan siswa ke dalam formulir di bawah ini. Sistem akan memproses data tersebut menggunakan model Machine Learning yang telah dilatih untuk memprediksi tingkat kerentanan terhadap depresi[cite: 1].")

st.divider()

# Membuat form input dengan desain yang lebih rapi
with st.form("prediction_form", clear_on_submit=False):
    st.subheader("📝 Formulir Data Siswa")
    st.write("Lengkapi 8 parameter indikator di bawah ini.")
    
    # Kelompok 1: Psikologis & Akademik
    st.markdown("#### 1. Kondisi Psikologis & Akademik")
    col1, col2 = st.columns(2)
    with col1:
        suicidal_thoughts = st.selectbox("Apakah pernah memiliki pikiran untuk bunuh diri?", ["Tidak", "Ya"])
        academic_pressure = st.slider("Tingkat Tekanan Akademik (1: Sangat Rendah - 5: Sangat Tinggi)", 1, 5, 3)
    with col2:
        financial_stress = st.slider("Tingkat Stres Finansial (1: Sangat Rendah - 5: Sangat Tinggi)", 1, 5, 3)
        study_satisfaction = st.slider("Tingkat Kepuasan Belajar (1: Sangat Rendah - 5: Sangat Tinggi)", 1, 5, 3)
        
    st.markdown("<br>", unsafe_allow_html=True) # Spasi kosong
    
    # Kelompok 2: Demografi & Gaya Hidup
    st.markdown("#### 2. Demografi & Gaya Hidup")
    col3, col4 = st.columns(2)
    with col3:
        age = st.number_input("Usia Siswa (Tahun)", min_value=15, max_value=40, value=20)
        study_hours = st.number_input("Durasi Belajar Harian (Jam)", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
    with col4:
        dietary_habits = st.selectbox("Pola Makan", ["Sehat", "Sedang", "Tidak Sehat"])
        sleep_duration = st.selectbox("Rata-rata Durasi Tidur", ["Kurang dari 5 jam", "5-6 jam", "7-8 jam", "Lebih dari 8 jam"])
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tombol Submit Lebar
    submit_button = st.form_submit_button("🚀 Analisis Data Sekarang", use_container_width=True)
    
if submit_button:
    # Mapping dari input UI bahasa Indonesia ke format angka yang dipahami model
    suicidal_map = {"Tidak": 0, "Ya": 1}
    dietary_map = {"Sehat": 0, "Sedang": 1, "Tidak Sehat": 2}
    sleep_map = {"5-6 jam": 0, "7-8 jam": 1, "Kurang dari 5 jam": 2, "Lebih dari 8 jam": 3}
    
    # Membuat DataFrame langsung dengan nilai yang sudah di-mapping
    input_df = pd.DataFrame([{
        'Have you ever had suicidal thoughts ?': suicidal_map[suicidal_thoughts],
        'Academic Pressure': academic_pressure,
        'Financial Stress': financial_stress,
        'Age': age,
        'Study Satisfaction': study_satisfaction,
        'Study Hours': study_hours,
        'Dietary Habits': dietary_map[dietary_habits],
        'Sleep Duration': sleep_map[sleep_duration]
    }])
    
    # Susun kolom sesuai urutan fitur saat model ditraining
    input_df = input_df[TOP_8_FEATURES]
    
    st.divider()
    
    # Efek Loading interaktif
    with st.spinner('Sistem sedang mengekstraksi fitur dan melakukan klasifikasi...'):
        time.sleep(1.5) # Memberikan jeda waktu agar terasa proses perhitungannya
        prediction = model.predict(input_df)
    
    # Menampilkan Hasil Prediksi
    st.markdown("### 📊 Hasil Analisis Sistem SHIELD")
    
    if prediction[0] == 1:
        st.error("🚨 **Peringatan Tinggi: Indikasi Depresi Terdeteksi**")
        st.write("Berdasarkan parameter yang dimasukkan, sistem mendeteksi bahwa siswa memiliki kerentanan yang tinggi terhadap depresi.")
        
        # Kotak Rekomendasi
        st.warning("""
        **💡 Rekomendasi Intervensi:**
        * Disarankan untuk segera menjadwalkan sesi dengan konselor akademik atau psikolog kampus.
        * Evaluasi kembali beban akademik dan pertimbangkan untuk mengurangi intensitasnya sementara waktu.
        * Perhatikan pola tidur dan pastikan siswa mendapatkan dukungan sosial yang cukup.
        """)
    else:
        st.success("✅ **Status Aman: Tidak Ada Indikasi Depresi Signifikan**")
        st.write("Berdasarkan parameter yang dimasukkan, kondisi psikologis dan gaya hidup siswa saat ini berada dalam rentang yang wajar dan aman.")
        
        # Kotak Rekomendasi
        st.info("""
        **💡 Rekomendasi Preventif:**
        * Pertahankan pola makan sehat dan durasi tidur yang konsisten.
        * Kelola tingkat stres finansial dan tekanan akademik secara berkala.
        * Terus lakukan kegiatan yang dapat meningkatkan tingkat kepuasan belajar.
        """)