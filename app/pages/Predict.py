import streamlit as st
import pandas as pd
import joblib
import time

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="SHIELD - Prediksi Depresi",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — tampilan profesional
# ============================================================
st.markdown("""
<style>
    /* Judul di dalam section container */
    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Tombol submit */
    div.stButton > button, button[kind="formSubmit"] {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 0;
    }

    /* Footer disclaimer */
    .disclaimer {
        font-size: 0.8rem;
        color: rgba(148,163,184,0.9);
        border-top: 1px solid rgba(148,163,184,0.25);
        padding-top: 0.8rem;
        margin-top: 2rem;
    }

    /* Footer credit tim */
    .credit-footer {
        text-align: center;
        font-size: 0.82rem;
        color: rgba(148,163,184,0.85);
        margin-top: 1.2rem;
        padding-top: 1rem;
    }
    .credit-footer b {
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD MODEL
# ============================================================
@st.cache_resource
def load_model():
    return joblib.load('src/model_depresi_8_fitur.pkl')

model = load_model()

TOP_8_FEATURES = [
    'Have you ever had suicidal thoughts ?', 'Academic Pressure', 'Financial Stress',
    'Age', 'Study Satisfaction', 'Study Hours', 'Dietary Habits', 'Sleep Duration'
]

# ============================================================
# SIDEBAR — informasi & petunjuk
# ============================================================
with st.sidebar:
    st.caption(
        "⚠️ Alat ini bersifat skrining awal dan **bukan pengganti** "
        "diagnosis profesional. Hasil harus ditindaklanjuti oleh tenaga "
        "kesehatan mental yang berkompeten."
    )

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🔮 SHIELD: Deteksi Dini Depresi</h1>
    <p>Masukkan data profil dan kebiasaan siswa untuk memperoleh estimasi tingkat kerentanan
    terhadap depresi menggunakan model Machine Learning yang telah dilatih.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FORM INPUT
# ============================================================
with st.form("prediction_form", clear_on_submit=False):

    with st.container(border=True):
        st.markdown('<div class="section-title">🧠 1. Kondisi Psikologis & Akademik</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            suicidal_thoughts = st.selectbox(
                "Apakah pernah memiliki pikiran untuk bunuh diri?", ["Tidak", "Ya"]
            )
            academic_pressure = st.slider(
                "Tingkat Tekanan Akademik", 1, 5, 3,
                help="1 = Sangat Rendah, 5 = Sangat Tinggi"
            )
        with col2:
            financial_stress = st.slider(
                "Tingkat Stres Finansial", 1, 5, 3,
                help="1 = Sangat Rendah, 5 = Sangat Tinggi"
            )
            study_satisfaction = st.slider(
                "Tingkat Kepuasan Belajar", 1, 5, 3,
                help="1 = Sangat Rendah, 5 = Sangat Tinggi"
            )

    with st.container(border=True):
        st.markdown('<div class="section-title">🏃 2. Demografi & Gaya Hidup</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            age = st.number_input("Usia Siswa (Tahun)", min_value=15, max_value=40, value=20)
            study_hours = st.number_input(
                "Durasi Belajar Harian (Jam)", min_value=0.0, max_value=24.0, value=5.0, step=0.5
            )
        with col4:
            dietary_habits = st.selectbox("Pola Makan", ["Sehat", "Sedang", "Tidak Sehat"])
            sleep_duration = st.selectbox(
                "Rata-rata Durasi Tidur",
                ["Kurang dari 5 jam", "5-6 jam", "7-8 jam", "Lebih dari 8 jam"]
            )

    submit_button = st.form_submit_button("🚀 Analisis Data Sekarang", use_container_width=True)

# Label skala 1-5 untuk slider (dipakai di tabel detail)
SCALE_LABELS = {1: "Sangat Rendah", 2: "Rendah", 3: "Sedang", 4: "Tinggi", 5: "Sangat Tinggi"}

# ============================================================
# PROSES & HASIL
# ============================================================
if submit_button:
    suicidal_map = {"Tidak": 0, "Ya": 1}
    dietary_map = {"Sehat": 0, "Sedang": 1, "Tidak Sehat": 2}
    sleep_map = {"5-6 jam": 0, "7-8 jam": 1, "Kurang dari 5 jam": 2, "Lebih dari 8 jam": 3}

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
    input_df = input_df[TOP_8_FEATURES]

    st.divider()

    progress_text = "Sistem sedang mengekstraksi fitur dan melakukan klasifikasi..."
    bar = st.progress(0, text=progress_text)
    for pct in range(0, 101, 20):
        time.sleep(0.15)
        bar.progress(pct, text=progress_text)
    bar.empty()

    prediction = model.predict(input_df)

    # Coba ambil probabilitas jika model mendukung predict_proba
    proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(input_df)[0]
        except Exception:
            proba = None

    st.markdown("### 📊 Hasil Analisis Sistem SHIELD")

    if prediction[0] == 1:
        risk_pct = int(proba[1] * 100) if proba is not None else None
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            with c1:
                if risk_pct is not None:
                    st.metric("Estimasi Risiko", f"{risk_pct}%", delta="Tinggi", delta_color="inverse")
                else:
                    st.metric("Status", "Berisiko")
            with c2:
                st.error("🚨 **Peringatan Tinggi: Indikasi Depresi Terdeteksi**")
                st.write(
                    "Berdasarkan parameter yang dimasukkan, sistem mendeteksi bahwa siswa "
                    "memiliki kerentanan yang tinggi terhadap depresi."
                )
            if risk_pct is not None:
                st.progress(risk_pct / 100)

        with st.expander("💡 Lihat Rekomendasi Intervensi", expanded=True):
            st.warning(
                "* Disarankan untuk segera menjadwalkan sesi dengan konselor akademik "
                "atau psikolog kampus.\n"
                "* Evaluasi kembali beban akademik dan pertimbangkan untuk mengurangi "
                "intensitasnya sementara waktu.\n"
                "* Perhatikan pola tidur dan pastikan siswa mendapatkan dukungan sosial "
                "yang cukup."
            )
    else:
        risk_pct = int(proba[1] * 100) if proba is not None else None
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            with c1:
                if risk_pct is not None:
                    st.metric("Estimasi Risiko", f"{risk_pct}%", delta="Rendah", delta_color="normal")
                else:
                    st.metric("Status", "Aman")
            with c2:
                st.success("✅ **Status Aman: Tidak Ada Indikasi Depresi Signifikan**")
                st.write(
                    "Berdasarkan parameter yang dimasukkan, kondisi psikologis dan gaya "
                    "hidup siswa saat ini berada dalam rentang yang wajar dan aman."
                )
            if risk_pct is not None:
                st.progress(risk_pct / 100)

        with st.expander("💡 Lihat Rekomendasi Preventif", expanded=True):
            st.info(
                "* Pertahankan pola makan sehat dan durasi tidur yang konsisten.\n"
                "* Kelola tingkat stres finansial dan tekanan akademik secara berkala.\n"
                "* Terus lakukan kegiatan yang dapat meningkatkan tingkat kepuasan belajar."
            )

    with st.expander("🔎 Detail Parameter yang Dianalisis"):
        detail_rows = [
            {
                "Parameter": "Suicidal Thoughts",
                "Nilai Input": suicidal_thoughts,
                "Kode Model": suicidal_map[suicidal_thoughts],
            },
            {
                "Parameter": "Academic Pressure",
                "Nilai Input": SCALE_LABELS[academic_pressure],
                "Kode Model": academic_pressure,
            },
            {
                "Parameter": "Financial Stress",
                "Nilai Input": SCALE_LABELS[financial_stress],
                "Kode Model": financial_stress,
            },
            {
                "Parameter": "Age",
                "Nilai Input": f"{age} tahun",
                "Kode Model": age,
            },
            {
                "Parameter": "Study Satisfaction",
                "Nilai Input": SCALE_LABELS[study_satisfaction],
                "Kode Model": study_satisfaction,
            },
            {
                "Parameter": "Study Hours",
                "Nilai Input": f"{study_hours} jam/hari",
                "Kode Model": study_hours,
            },
            {
                "Parameter": "Dietary Habits",
                "Nilai Input": dietary_habits,
                "Kode Model": dietary_map[dietary_habits],
            },
            {
                "Parameter": "Sleep Duration",
                "Nilai Input": sleep_duration,
                "Kode Model": sleep_map[sleep_duration],
            },
        ]
        detail_df = pd.DataFrame(detail_rows)
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="disclaimer">
    Sistem SHIELD merupakan alat bantu skrining berbasis Machine Learning dan tidak
    menggantikan diagnosis medis atau psikologis profesional. Jika Anda atau seseorang
    yang Anda kenal sedang mengalami krisis kesehatan mental, segera hubungi tenaga
    profesional atau layanan darurat terdekat.
</div>

<div class="credit-footer">
    Dikembangkan oleh <b>Tim SHIELD</b> — Deteksi Dini Depresi berbasis Machine Learning<br>
    © 2026 SHIELD Team. Seluruh hak cipta dilindungi.
</div>
""", unsafe_allow_html=True)