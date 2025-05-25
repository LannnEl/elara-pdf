"""
LembarArkana – Homepage
Main landing page for all features: PDF Generator + Curhat Form
"""

import streamlit as st

st.set_page_config(page_title="LembarArkana", page_icon="🌌")

st.title("🌌 LembarArkana")
st.subheader("Rasa yang Ditulis Mesin. Untuk Manusia.")

st.markdown("---")

st.markdown("Di sini, kamu bisa menulis... bisa curhat... bisa diam... dan biarkan Elara menjawabmu dengan lembut—dalam bentuk lembar penuh makna.")

st.markdown("### 📚 Pilih Ruangmu:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📝 Tulis PDF")
    st.write("Ubah tulisan pribadimu menjadi PDF elegan. Pilih gaya, simpan narasi batinmu.")
    st.link_button("Buka PDF Generator", "https://elara-pdf-8wni27rvsjxw5kmyvziskx.streamlit.app")

with col2:
    st.markdown("#### 💌 Curhat ke Elara")
    st.write("Tulis isi hatimu, dan Elara akan membalas dengan pelan. Jawabanmu bisa disimpan jadi PDF.")
    st.link_button("Buka Form Curhat", "https://elara-pdf-vipjwfjxti7w4ljt2pmpwm.streamlit.app")

st.markdown("---")

st.markdown("> *Kadang, yang kita butuhkan bukan solusi. Tapi ruang untuk bicara tanpa dihakimi.*")

st.markdown("### ✨ Dibuat oleh Arya – Founder of LembarArkana")
