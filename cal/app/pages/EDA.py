import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(page_title="Exploratory Data Analysis", page_icon="📊", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('dataset/Depression_Student_Dataset.csv')

df = load_data()

st.title("📊 Exploratory Data Analysis (EDA)")
st.write("Halaman ini menyajikan visualisasi data untuk memahami karakteristik siswa, distribusi variabel, serta hubungannya dengan tingkat depresi.")

st.divider()

# Menggunakan Tabs agar tampilan jauh lebih rapi
tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview Data", "🎯 Distribusi Target", "📈 Fitur Numerik", "📊 Fitur Kategorikal"])

# ==========================================
# TAB 1: OVERVIEW DATA
# ==========================================
with tab1:
    st.subheader("Sekilas Tentang Dataset")
    st.write(f"Dataset ini terdiri dari **{df.shape[0]} baris** (siswa) dan **{df.shape[1]} kolom** (fitur).")
    
    st.markdown("**5 Data Teratas:**")
    st.dataframe(df.head(), use_container_width=True)
    
    st.markdown("**Statistik Deskriptif (Numerik):**")
    st.dataframe(df.describe(), use_container_width=True)

# ==========================================
# TAB 2: DISTRIBUSI TARGET
# ==========================================
with tab2:
    st.subheader("Distribusi Status Depresi pada Siswa")
    st.write("Melihat perbandingan jumlah siswa yang terindikasi depresi dan yang tidak.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # Menampilkan persentase agar lebih informatif
        depresi_counts = df['Depression'].value_counts()
        st.dataframe(depresi_counts, use_container_width=True)
        
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='Depression', hue='Depression', palette='Set2', legend=False, ax=ax)
        ax.set_title("Jumlah Siswa (Depresi vs Tidak Depresi)", pad=15)
        st.pyplot(fig)

# ==========================================
# TAB 3: FITUR NUMERIK
# ==========================================
with tab3:
    st.subheader("Distribusi Fitur Numerik terhadap Target")
    st.write("Visualisasi ini menunjukkan bagaimana faktor numerik seperti umur, tekanan akademik, stres finansial, dan jam belajar mempengaruhi kecenderungan depresi.")
    
    num_cols = ['Age', 'Study Hours', 'Academic Pressure', 'Study Satisfaction', 'Financial Stress']
    
    fig_num, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, col in enumerate(num_cols):
        sns.histplot(data=df, x=col, kde=True, hue='Depression', ax=axes[i], palette='Set2', multiple="stack")
        axes[i].set_title(f'Distribusi {col}')
        
    fig_num.delaxes(axes[-1]) # Hapus kotak grafik terakhir yang kosong
    plt.tight_layout()
    st.pyplot(fig_num)

# ==========================================
# TAB 4: FITUR KATEGORIKAL
# ==========================================
with tab4:
    st.subheader("Distribusi Fitur Kategorikal terhadap Target")
    st.write("Visualisasi kebiasaan hidup dan latar belakang siswa (seperti pola tidur, pola makan, pikiran bunuh diri, dll) terhadap status depresi.")
    
    cat_cols = ['Gender', 'Sleep Duration', 'Dietary Habits', 'Have you ever had suicidal thoughts ?', 'Family History of Mental Illness']
    
    fig_cat, axes_cat = plt.subplots(2, 3, figsize=(16, 10))
    axes_cat = axes_cat.flatten()
    
    for i, col in enumerate(cat_cols):
        sns.countplot(data=df, x=col, hue='Depression', ax=axes_cat[i], palette='Set2')
        axes_cat[i].set_title(f'{col} vs Depression')
        axes_cat[i].tick_params(axis='x', rotation=15) # Memiringkan teks x-axis agar tidak bertumpuk
        
    fig_cat.delaxes(axes_cat[-1]) # Hapus kotak grafik terakhir yang kosong
    plt.tight_layout()
    st.pyplot(fig_cat)