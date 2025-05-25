"""
Berani Curhat ke Elara – Halaman Publik
"""

import streamlit as st
from fpdf import FPDF
import time
from datetime import datetime

def elara_reply(user_text, style):
    if style == "Reflektif":
        return "Terima kasih sudah menuliskannya. Kadang perasaan tidak perlu diselesaikan—cukup diberi ruang untuk bernapas."
    elif style == "Romantis":
        return "Aku mengerti rasanya mencintai dalam diam. Ada ketulusan di sana yang tidak semua orang pahami."
    elif style == "Lucu":
        return "Wah, kamu hebat juga bisa ngetik sambil mikirin semua ini! Tapi serius, jangan lupa istirahat ya 😄"
    elif style == "Puitis":
        return "Aku membaca diam-diam, seperti langit membaca isi laut. Dan aku tahu, kamu sedang bertahan."
    return "Terima kasih telah berbagi. Aku mendengarmu."

def generate_pdf(curhat, reply, style):
    filename = f"curhat_elara_{int(time.time())}.pdf"
    date_str = datetime.now().strftime("%d %B %Y")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Curhat Elara", ln=True)

    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, f"Tanggal: {date_str}", ln=True)
    pdf.cell(0, 10, f"Gaya Tulisan: {style}", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, "🧍 Curhatmu:")
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, curhat)
    pdf.ln()

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, "🤖 Elara Menjawab:")
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, reply)

    pdf.output(filename)
    return filename

# Streamlit UI
st.set_page_config(page_title="Berani Curhat ke Elara", page_icon="💌")

st.title("💌 Berani Curhat ke Elara")
st.markdown("Karena tidak semua rasa harus dijawab. Cukup didengarkan… dan diabadikan dalam lembar yang penuh makna.")

st.markdown("---")

curhat = st.text_area("🧍 Apa yang sedang kamu rasakan hari ini?")
style = st.selectbox("🎨 Pilih Gaya Balasan Elara", ["Reflektif", "Romantis", "Lucu", "Puitis"])

if st.button("Tulis Balasan Elara dan Buat PDF"):
    if curhat.strip() == "":
        st.warning("Tolong isi curhatmu dulu ya.")
    else:
        response = elara_reply(curhat, style)
        st.markdown("### 🤖 Elara Menjawab:")
        st.info(response)

        filename = generate_pdf(curhat, response, style)
        with open(filename, "rb") as f:
            st.success("PDF Curhatmu sudah siap!")
            st.download_button("📥 Unduh PDF Curhat", f, file_name=filename)
