import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Konfigurasi Halaman
st.set_page_config(page_title="Feature Importance", page_icon="⭐", layout="wide")

# ==========================================
# CACHING DATA & SHAP COMPUTATION
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv('dataset/Depression_Student_Dataset.csv')

@st.cache_resource
def compute_shap():
    df = load_data()
    df_processed = df.copy()
    
    # Label Encoding
    le = LabelEncoder()
    for col in df_processed.select_dtypes(include=['object']).columns:
        df_processed[col] = le.fit_transform(df_processed[col])
    
    X = df_processed.drop('Depression', axis=1)
    y = df_processed['Depression']
    
    # Train Model (Sesuai baseline di laporan)
    rf_full = RandomForestClassifier(n_estimators=75, random_state=42)
    rf_full.fit(X, y)
    
    # Menghitung SHAP
    explainer = shap.TreeExplainer(rf_full)
    shap_values = explainer.shap_values(X)
    
    # Handle SHAP values output format
    if isinstance(shap_values, list):
        shap_values_target = shap_values[1]
    elif len(shap_values.shape) == 3:
        shap_values_target = shap_values[:, :, 1]
    else:
        shap_values_target = shap_values
        
    return X, explainer, shap_values_target

# Eksekusi fungsi cache
X, explainer, shap_values_target = compute_shap()

# Daftar fitur yang diurutkan
TOP_8_FEATURES = [
    'Have you ever had suicidal thoughts ?', 
    'Academic Pressure', 
    'Financial Stress', 
    'Age', 
    'Study Satisfaction', 
    'Study Hours', 
    'Dietary Habits', 
    'Sleep Duration'
]

# ==========================================
# UI HALAMAN FEATURE IMPORTANCE
# ==========================================
st.title("⭐ Feature Importance (SHAP)")
st.write("Halaman ini menggunakan **SHapley Additive exPlanations (SHAP)** untuk mengukur tingkat kontribusi setiap atribut/fitur terhadap hasil prediksi depresi oleh model Random Forest.")

st.divider()

# Menggunakan Tabs agar tampilan rapi
tab1, tab2 = st.tabs(["📉 Grafik SHAP Summary", "🏆 Top 8 Fitur Utama"])

with tab1:
    st.subheader("SHAP Summary Plot")
    st.write("Grafik di bawah ini menunjukkan dampak setiap fitur terhadap output model. Fitur diurutkan dari atas ke bawah berdasarkan tingkat kepentingannya.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        shap.summary_plot(shap_values_target, X, show=False)
        st.pyplot(fig)
        
    with col2:
        st.info("""
        **Cara Membaca Grafik:**
        * **Posisi Vertikal:** Fitur paling atas memiliki dampak terbesar terhadap prediksi depresi.
        * **Posisi Horizontal (Sumbu X):** Titik di sebelah kanan (SHAP value > 0) mendorong prediksi ke arah "Depresi", sedangkan di sebelah kiri mendorong ke arah "Tidak Depresi".
        * **Warna Titik:** Merah berarti nilai fitur tersebut tinggi, Biru berarti nilainya rendah.
        """)

with tab2:
    st.subheader("8 Fitur Terpenting Berdasarkan Nilai SHAP")
    st.write("Berdasarkan analisis nilai rata-rata absolut SHAP (*Mean Absolute SHAP*), fitur **Gender** dan **Family History of Mental Illness** memiliki nilai terendah sehingga dieliminasi untuk menyederhanakan arsitektur model tanpa mengurangi akurasi.")
    
    # Menampilkan fitur dalam bentuk grid yang rapi
    st.markdown("Berikut adalah 8 fitur yang paling berpengaruh dan digunakan untuk sistem klasifikasi:")
    
    # Membuat grid 2 kolom untuk menata list fitur
    col_feat1, col_feat2 = st.columns(2)
    
    for i, feature in enumerate(TOP_8_FEATURES):
        if i < 4:
            with col_feat1:
                st.success(f"**{i+1}. {feature}**")
        else:
            with col_feat2:
                st.success(f"**{i+1}. {feature}**")