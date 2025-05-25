"""
ElaraPDF Web Version – Powered by Streamlit
"""

import streamlit as st
from fpdf import FPDF
import time

def stylize_text(text, style):
    text = text.strip().capitalize()
    if style == "Reflektif":
        return f"*{text}*\n\nKadang diam bukan karena tak tahu harus berkata apa. Tapi karena merasa... itu lebih jujur."
    elif style == "Romantis":
        return f"*{text}*\n\nJika aku bisa menuliskanmu, maka tiap kata akan bergetar seperti namamu kusebut diam-diam."
    elif style == "Lucu":
        return f"*{text}*\n\nHidup kadang seperti WiFi gratis: sinyal kuat, tapi tidak bisa konek sama kamu."
    elif style == "Puitis":
        return f"*{text}*\n\nKau adalah koma, tempat aku berhenti sejenak - sebelum melanjutkan kalimat hidup."
    return text

def generate_pdf(text, style, title):
    filename = f"elara_output_{int(time.time())}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)

    if title:
        pdf.set_font("Times", "B", 14)
        pdf.multi_cell(0, 10, title)
        pdf.ln(5)
        pdf.set_font("Times", "", 12)

    stylized_text = stylize_text(text, style)
    for line in stylized_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename

# Streamlit UI
st.set_page_config(page_title="ElaraPDF – LembarArkana", page_icon="✨")

st.title("LembarArkana")
st.subheader("Rasa yang Ditulis Mesin. Untuk Manusia.")

story = st.text_area("Masukkan ceritamu di sini:")
style = st.selectbox("Pilih Gaya Tulisan:", ["Reflektif", "Romantis", "Lucu", "Puitis"])
title = st.text_input("Judul PDF (opsional):")

if st.button("Generate PDF"):
    if story.strip() == "":
        st.warning("Tolong isi ceritamu dulu ya, Arya.")
    else:
        filename = generate_pdf(story, style, title)
        with open(filename, "rb") as f:
            st.success("PDF berhasil dibuat! Unduh di bawah ini:")
            st.download_button("📥 Unduh PDF", f, file_name=filename)
