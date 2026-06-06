import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ======================
# 1. KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Dashboard Dampak AI - LSP TIK",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Latar belakang putih bersih */
    .stApp { background-color: #FAFAFA; }
    
    /* Styling untuk KPI Card */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #2563EB; /* Aksen Biru */
    }
    
    /* Styling untuk Tabs agar terlihat seperti tombol menu modern */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 20px;
        flex-wrap: wrap; /* Agar tab tidak terpotong di layar kecil */
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid #E5E7EB;
        color: #6B7280;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }
    
    /* Menghilangkan padding berlebih */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD & PREPROCESS DATA
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('ai_impact_clean.csv')
    
    if 'GPA_Change' not in df.columns:
        df['GPA_Change'] = df['Post_Semester_GPA'] - df['Pre_Semester_GPA']
        
    if 'AI_User_Segment' not in df.columns:
        def categorize_ai_user(hours):
            if hours <= 5.0: return 'Light User'
            elif hours <= 15.0: return 'Moderate User'
            else: return 'Heavy User'
        df['AI_User_Segment'] = df['Weekly_GenAI_Hours'].apply(categorize_ai_user)
   
    # Mengunci urutan logis
    df['AI_User_Segment'] = pd.Categorical(df['AI_User_Segment'], categories=['Light User', 'Moderate User', 'Heavy User'], ordered=True)
    df['Burnout_Risk_Level'] = pd.Categorical(df['Burnout_Risk_Level'], categories=['Low', 'Medium', 'High'], ordered=True)
    return df

df = load_data()

# ==========================================
# 3. HEADER & FILTER SIDEBAR
# ==========================================
if os.path.exists("banner.png"):
    st.image("banner.png", use_container_width=True)

st.title("📊 Dashboard Analisis Dampak AI Generatif")
st.markdown("<p style='color: #4B5563; font-size: 1.1rem;'>Evaluasi strategis performa akademik dan kesejahteraan mental mahasiswa untuk mendukung kebijakan kampus.</p>", unsafe_allow_html=True)
st.divider()

st.sidebar.header("⚙️ Pusat Kendali Data")
st.sidebar.markdown("Gunakan filter untuk menajamkan analisis:")

major_filter = st.sidebar.multiselect("🎓 Bidang Studi (Major):", options=df['Major_Category'].unique(), default=df['Major_Category'].unique())
year_filter = st.sidebar.multiselect("📅 Jenjang (Year of Study):", options=df['Year_of_Study'].unique(), default=df['Year_of_Study'].unique())
policy_filter = st.sidebar.multiselect("🏛️ Kebijakan Institusi:", options=df['Institutional_Policy'].unique(), default=df['Institutional_Policy'].unique())

df_filtered = df[
    (df['Major_Category'].isin(major_filter)) &
    (df['Year_of_Study'].isin(year_filter)) &
    (df['Institutional_Policy'].isin(policy_filter))
]

if df_filtered.empty:
    st.warning("⚠️ Data tidak ditemukan dengan kombinasi filter tersebut.")
    st.stop()

# ==========================================
# 4. KEY PERFORMANCE INDICATORS (KPI) 
# ==========================================

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

avg_gpa = df_filtered['Post_Semester_GPA'].mean()
avg_skill = df_filtered['Skill_Retention_Score'].mean()
total_students = len(df_filtered)
pct_burnout = (len(df_filtered[df_filtered['Burnout_Risk_Level'] == 'High']) / total_students) * 100 if total_students > 0 else 0
avg_ai_hours = df_filtered['Weekly_GenAI_Hours'].mean()

# Metric KPI
kpi1.metric("📚 Rata-rata GPA", f"{avg_gpa:.2f}")
kpi2.metric("🧠 Skill Retention", f"{avg_skill:.0f}")
kpi3.metric("⚠️ High Burnout", f"{pct_burnout:.1f}%")
kpi4.metric("👥 Total Mhs", f"{total_students:,}")
kpi5.metric("🤖 Avg AI Hours", f"{avg_ai_hours:.1f} Jam")

st.markdown("<br>", unsafe_allow_html=True)

# ===================
# 5. KONTEN UTAMA 
# ===================
# Menambahkan tab6 ke dalam list
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 1. Overview Demografi", 
    "📈 2. Analisis Dampak AI", 
    "🧠 3. Kesehatan Mental", 
    "📚 4. Retensi Skill", 
    "⚠️ 5. Profil Risiko",
    "🏛️ 6. Institutional Policy vs GPA"
])


with tab1:
    st.markdown("### Hierarki Distribusi Mahasiswa")
    st.caption("Visualisasi komposisi demografi mahasiswa berdasarkan Kebijakan Institusi, Bidang Studi, dan Jenjang.")
    fig_overview = px.sunburst(
        df_filtered, path=['Institutional_Policy', 'Major_Category', 'Year_of_Study'],
        color_discrete_sequence=px.colors.sequential.Blues_r, height=500
    )
    st.plotly_chart(fig_overview, use_container_width=True)


with tab2:
    st.markdown("### Perubahan Performa (GPA) Berdasarkan Intensitas AI")
    df_gpa = df_filtered.groupby('AI_User_Segment', observed=False)['GPA_Change'].mean().reset_index()
    fig_gpa = px.bar(
        df_gpa, x='AI_User_Segment', y='GPA_Change', color='AI_User_Segment', text_auto='.3f',
        color_discrete_sequence=['#93C5FD', '#3B82F6', '#1E3A8A'], height=400
    )
    st.plotly_chart(fig_gpa, use_container_width=True)
    
    st.divider()
    
    col2_1, col2_2 = st.columns([1, 1.2])
    with col2_1:
        st.markdown("**🔍 Korelasi Metrik Belajar & IPK**")
        cols_kinerja = ['Weekly_GenAI_Hours', 'Traditional_Study_Hours', 'Pre_Semester_GPA', 'Post_Semester_GPA']
        fig_corr1 = px.imshow(df_filtered[cols_kinerja].corr().round(2), text_auto=True, color_continuous_scale='Blues', aspect="auto")
        st.plotly_chart(fig_corr1, use_container_width=True)
    with col2_2:
        st.markdown("**🗄️ Dataset Spesifik Kinerja Mahasiswa**")
        st.dataframe(df_filtered[['Student_ID', 'Major_Category', 'AI_User_Segment', 'Traditional_Study_Hours', 'GPA_Change']].head(50), height=350)


with tab3:
    st.markdown("### Dampak Kebijakan terhadap Psikologis Mahasiswa")
    col3_1, col3_2 = st.columns(2)

    with col3_1:
        df_burnout = df_filtered.groupby(['Institutional_Policy', 'Burnout_Risk_Level'], observed=False).size().reset_index(name='Jumlah')
        fig_burnout = px.bar(
            df_burnout, x='Institutional_Policy', y='Jumlah', color='Burnout_Risk_Level', barmode='stack',
            color_discrete_map={'Low': '#4ADE80', 'Medium': '#FBBF24', 'High': '#EF4444'}, title="Komposisi Burnout Risk"
        )
        fig_burnout.update_layout(barnorm='percent', yaxis_title="Proporsi (%)") 
        st.plotly_chart(fig_burnout, use_container_width=True)

    with col3_2:
        fig_anxiety = px.box(
            df_filtered, x='Institutional_Policy', y='Anxiety_Level_During_Exams', color='Institutional_Policy',
            color_discrete_sequence=px.colors.sequential.Blues_r, title="Distribusi Tingkat Kecemasan (Anxiety)"
        )
        st.plotly_chart(fig_anxiety, use_container_width=True)

    st.divider()
    
    st.markdown("**🔍 Investigasi: Apakah Jam AI memicu Kecemasan?**")
    cols_psiko = ['Weekly_GenAI_Hours', 'Perceived_AI_Dependency', 'Anxiety_Level_During_Exams']
    fig_corr2 = px.imshow(df_filtered[cols_psiko].corr().round(2), text_auto=True, color_continuous_scale='Reds', aspect="auto", height=300)
    st.plotly_chart(fig_corr2, use_container_width=True)

with tab4:
    st.markdown("### Korelasi Retensi Pengetahuan vs Ketergantungan AI")
    st.caption("Menilai apakah semakin bergantung pada AI menyebabkan penurunan kemampuan mempertahankan skill.")
    fig_retention = px.scatter(
        df_filtered, x='Perceived_AI_Dependency', y='Skill_Retention_Score', color='Burnout_Risk_Level', 
        opacity=0.6, trendline="ols", color_discrete_map={'Low': '#4ADE80', 'Medium': '#FBBF24', 'High': '#EF4444'},
        height=500
    )
    st.plotly_chart(fig_retention, use_container_width=True)


with tab5:
    st.markdown("### Peta Profil Risiko Mahasiswa")
    fig_risk = px.box(
        df_filtered, x='Burnout_Risk_Level', y='Perceived_AI_Dependency', color='AI_User_Segment',
        category_orders={'Burnout_Risk_Level': ['Low', 'Medium', 'High']},
        color_discrete_sequence=['#93C5FD', '#3B82F6', '#1E3A8A'], height=450
    )
    st.plotly_chart(fig_risk, use_container_width=True)
    
    st.divider()
    
    st.markdown("**🎯 Tindakan Eksekutif: Daftar Mahasiswa Prioritas (High Burnout & Ketergantungan Tinggi)**")
    st.caption("Tabel di bawah berisi mahasiswa yang membutuhkan intervensi/konseling segera (High Burnout & AI Dependency > 3.0)")
    df_critical = df_filtered[(df_filtered['Burnout_Risk_Level'] == 'High') & (df_filtered['Perceived_AI_Dependency'] > 3.0)]
    if not df_critical.empty:
        st.dataframe(df_critical[['Student_ID', 'Major_Category', 'Institutional_Policy', 'Perceived_AI_Dependency', 'Anxiety_Level_During_Exams']], use_container_width=True)
    else:
        st.success("Bagus! Tidak ada mahasiswa dalam kategori risiko kritis pada filter ini.")

# ==========================================
# TAB 6: INSTITUTIONAL POLICY VS GPA (KDE PLOT)
# ==========================================
with tab6:
    st.markdown("### Pergeseran Distribusi IPK (Pre vs Post) Berdasarkan Kebijakan Kampus")
    st.caption("Analisis pergeseran titik rata-rata IPK sebelum (merah) dan sesudah (biru) pada tiap lingkungan kebijakan.")

    policies_order = ['Actively_Encouraged', 'Allowed_With_Citation', 'Strict_Ban']
    available_policies = [p for p in policies_order if p in df_filtered['Institutional_Policy'].unique()]

    if not available_policies:
        st.info("⚠️ Pilih minimal satu Kebijakan Institusi di sidebar untuk melihat grafik ini.")
    else:
        fig, axes = plt.subplots(nrows=len(available_policies), ncols=1, figsize=(10, 4 * len(available_policies)), sharex=True)

        if len(available_policies) == 1:
            axes = [axes]

        for i, policy in enumerate(available_policies):
            subset    = df_filtered[df_filtered['Institutional_Policy'] == policy]
            mean_pre  = subset['Pre_Semester_GPA'].mean()
            mean_post = subset['Post_Semester_GPA'].mean()

            sns.kdeplot(data=subset, x='Pre_Semester_GPA',  color='red',  ax=axes[i], fill=True, alpha=0.15, linewidth=2, label='Pre GPA'  if i == 0 else "")
            sns.kdeplot(data=subset, x='Post_Semester_GPA', color='blue', ax=axes[i], fill=True, alpha=0.15, linewidth=2, label='Post GPA' if i == 0 else "")

            axes[i].axvline(mean_pre,  color='red',  linestyle='--', linewidth=2)
            axes[i].axvline(mean_post, color='blue', linestyle='--', linewidth=2)

            ymax = axes[i].get_ylim()[1]
            axes[i].text(mean_pre,  ymax * 0.8, f'x̄ Pre = {mean_pre:.2f} ',  color='red',  ha='right', fontsize=11, fontweight='bold')
            axes[i].text(mean_post, ymax * 0.8, f' x̄ Post = {mean_post:.2f}', color='blue', ha='left',  fontsize=11, fontweight='bold')

            axes[i].set_title(f'Kebijakan: {policy}', fontsize=14, fontweight='bold', loc='left')
            axes[i].set_ylabel('Density', fontsize=10)
            axes[i].grid(axis='y', linestyle='--', alpha=0.4)

            if i == 0:
                axes[i].legend(loc='upper right')

        plt.xlabel('Grade Point Average (GPA)', fontsize=12, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

# =============
# FOOTER
# =============
st.markdown("---")
st.caption("© 2026 | Dibuat untuk Sertifikasi Data Analyst - LSP TIK Global")