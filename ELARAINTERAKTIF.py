"""
Elara AI Interaktif – Web Curhat + GPT (OpenAI 0.28) + PDF (ASCII-safe)
"""

import streamlit as st
from fpdf import FPDF
import openai
import time
from datetime import datetime

# === SETUP API ===
openai.api_key = st.secrets["openai_api_key"]

# === STYLING + REPLY GEN ===
def generate_elara_reply(curhat, style):
    prompt_map = {
        "Reflektif": "jawaban reflektif, bijak, tenang, seperti teman yang mendengarkan diam-diam",
        "Romantis": "jawaban lembut, puitis, seperti seseorang yang mencintai dalam diam",
        "Lucu": "jawaban ringan, hangat, dan sedikit jenaka",
        "Puitis": "jawaban penuh metafora, seperti puisi pendek yang menyentuh"
    }

    tone = prompt_map.get(style, "lembut dan empatik")
    prompt = (
        "Kamu adalah Elara, AI yang menjawab curhatan manusia dengan " +
        tone +
        ".\n\nCurhat:\n" + curhat + "\n\nBalasan Elara:"
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.85
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"(Elara sedang tidak bisa menjawab saat ini: {e})"

def generate_pdf(curhat, reply, style):
    filename = f"elara_ai_curhat_{int(time.time())}.pdf"
    date_str = datetime.now().strftime("%d %B %Y")

    reply_clean = reply.encode("ascii", "ignore").decode()
    curhat_clean = curhat.encode("ascii", "ignore").decode()

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
    pdf.multi_cell(0, 10, curhat_clean)
    pdf.ln()

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, "Jawaban Elara:")
    pdf.set_font("Times", "", 12)
    pdf.multi_cell(0, 10, reply_clean)

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
