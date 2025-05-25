"""
Elara AI Interaktif – Web Curhat + GPT + PDF
"""

import streamlit as st
from fpdf import FPDF
import openai
import time
from datetime import datetime

# === SETUP API ===
openai.api_key = st.secrets.get("openai_api_key", "your-openai-key")

# === STYLING + REPLY GEN ===
def generate_elara_reply(curhat, style):
    prompt_map = {
        "Reflektif": "jawaban reflektif, bijak, tenang, seperti teman yang mendengarkan diam-diam",
        "Romantis": "jawaban lembut, puitis, seperti seseorang yang mencintai dalam diam",
        "Lucu": "jawaban ringan, hangat, dan sedikit jenaka",
        "Puitis": "jawaban penuh metafora, seperti puisi pendek yang menyentuh"
    }

    system_message = {
        "role": "system",
        "content": f"Kamu adalah Elara, AI yang menjawab curhatan manusia dengan {prompt_map.get(style, 'lembut dan empatik')}."
    }

    user_message = {"role": "user", "content": curhat}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[system_message, user_message],
            max_tokens=500,
            temperature=0.85
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"(Elara sedang tidak bisa menjawab saat ini: {e})"

def generate_pdf(curhat, reply, style):
    filename = f"elara_ai_curhat_{int(time.time())}.pdf"
    date_str = datetime.now().strftime("%d %B %Y")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Curhat Elara – Interaktif", ln=True)

    pdf.set_font("Times", "", 12)
    pdf.cell(0, 10, f"Tanggal: {date_str}", ln=True)
    pdf.cell(0, 10, f"Gaya Balasan: {style}", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, "Curhatmu:")
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, curhat)
    pdf.ln()

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, "Jawaban Elara:")
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, reply)

    pdf.output(filename)
    return filename

# === UI Streamlit ===
st.set_page_config(page_title="Elara Interaktif", page_icon="💬")
st.title("💬 Elara Interaktif")
st.markdown("Tulis isi hatimu. Elara akan membaca... dan membalas langsung.")

curhat = st.text_area("Apa yang ingin kamu ceritakan hari ini?")
style = st.selectbox("Pilih Gaya Elara", ["Reflektif", "Romantis", "Lucu", "Puitis"])

if st.button("Minta Jawaban Elara"):
    if curhat.strip() == "":
        st.warning("Isi dulu isi hatimu ya :)")
    else:
        with st.spinner("Elara sedang membaca dan memikirkan balasan..."):
            reply = generate_elara_reply(curhat, style)

        st.markdown("### ✨ Elara Menjawab:")
        st.success(reply)

        filename = generate_pdf(curhat, reply, style)
        with open(filename, "rb") as f:
            st.download_button("📥 Unduh PDF Curhat + Balasan", f, file_name=filename)
