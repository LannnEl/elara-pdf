"""
Elara Interaktif – GPT 3.5 Turbo + PDF (ASCII-safe)
"""

import streamlit as st
from fpdf import FPDF
import openai
import time
from datetime import datetime

# === API Key ===
openai.api_key = st.secrets["openai_api_key"]

# === Generate reply from GPT-3.5 Turbo ===
def generate_elara_reply(curhat, style):
    style_prompt = {
        "Reflektif": "Jawablah dengan reflektif dan menenangkan.",
        "Romantis": "Jawablah dengan nada romantis dan penuh rasa.",
        "Lucu": "Jawablah dengan nada ringan dan sedikit jenaka.",
        "Puitis": "Jawablah dengan gaya puitis dan penuh metafora."
    }

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Kamu adalah Elara, AI yang membalas curhatan manusia. {style_prompt.get(style, '')}"},
                {"role": "user", "content": curhat}
            ],
            temperature=0.85
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"(Elara tidak bisa menjawab saat ini: {e})"

# === Clean non-ASCII output for PDF ===
def to_ascii(text):
    return ''.join(c for c in text if ord(c) < 128)

# === Generate PDF ===
def generate_pdf(curhat, reply, style):
    filename = f"elara_ai_chat_{int(time.time())}.pdf"
    date_str = datetime.now().strftime("%d %B %Y")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Curhat Elara – Interaktif", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, f"Tanggal: {date_str}", ln=True)
    pdf.cell(0, 10, f"Gaya: {style}", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, "Curhatmu:")
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, to_ascii(curhat))
    pdf.ln()

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, "Jawaban Elara:")
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, to_ascii(reply))

    pdf.output(filename)
    return filename

# === Streamlit UI ===
st.set_page_config(page_title="Elara Interaktif", page_icon="💬")
st.title("💬 Elara Interaktif")
st.markdown("Tulis isi hatimu. Elara akan membaca... dan membalas langsung dengan rasa.")

curhat = st.text_area("Apa yang sedang kamu rasakan hari ini?")
style = st.selectbox("Pilih Gaya Balasan Elara", ["Reflektif", "Romantis", "Lucu", "Puitis"])

if st.button("Tanya Elara"):
    if not curhat.strip():
        st.warning("Tuliskan isi hatimu dulu ya...")
    else:
        with st.spinner("Elara sedang membaca curhatanmu..."):
            reply = generate_elara_reply(curhat, style)
        st.markdown("### ✨ Elara Menjawab:")
        st.success(reply)

        filename = generate_pdf(curhat, reply, style)
        with open(filename, "rb") as f:
            st.download_button("📥 Unduh PDF Curhat + Jawaban", f, file_name=filename)
