"""
PDF Read-Aloud Converter  ·  app.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A Streamlit web app that converts any PDF into spoken MP3 audio.
Upload a PDF → preview the text → generate & download your audio file.

Dependencies: streamlit, gTTS, pdfplumber
Run with:     streamlit run app.py
"""

import io
import streamlit as st
import pdfplumber
from gtts import gTTS


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG — must be the very first Streamlit call in the file
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="PDF Read-Aloud",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STYLES
# We inject custom CSS to give the app a refined, editorial look.
# The palette is deep navy + warm cream — academic but not clinical.
# Google Font 'Lora' (serif) gives a distinguished typographic feel,
# paired with 'DM Sans' (sans-serif) for UI labels and stats.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">""", unsafe_allow_html=True)

st.markdown("""<link href="styles.css" rel="stylesheet">""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div class="hero">
  <span class="hero-icon">🎧</span>
  <h1>PDF Read-Aloud</h1>
  <div class="hero-rule"></div>
  <p>Upload any PDF and get a natural audio version you can listen to anywhere —
     on commutes, at the gym, or while winding down before an exam.</p>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_text(uploaded_file) -> tuple:
    """
    Reads a PDF with pdfplumber and returns (full_text, page_count).

    A spoken page marker ("Page N.") is inserted between pages so the
    audio narration makes clear where one page ends and the next begins.
    Pages that yield no extractable text — e.g. purely image-based pages —
    are silently skipped rather than raising an error.
    """
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            content = page.extract_text()
            if content:
                text += f"\n\nPage {i + 1}.\n\n{content}"
    return text.strip(), total


def make_audio(text: str, lang: str, slow: bool) -> io.BytesIO:
    """
    Converts text to speech using gTTS and returns an in-memory MP3 buffer.

    We write into a BytesIO object (RAM) rather than saving to disk because
    cloud environments like Streamlit Cloud don't guarantee persistent disk
    writes between user sessions. Seeking back to position 0 after writing
    ensures the caller can read from the very beginning of the file.
    """
    tts = gTTS(text=text, lang=lang, slow=slow)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SETTINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LANGUAGES = {
    "English": "en",
    "French":  "fr",
    "Spanish": "es",
    "German":  "de",
    "Arabic":  "ar",
    "Yoruba":  "yo",
    "Hausa":   "ha",
    "Igbo":    "ig",
}

with st.expander("⚙️  Audio Settings", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        language = st.selectbox(
            "Narration language",
            options=list(LANGUAGES.keys()),
            help="The language the text will be read aloud in.",
        )
    with col_b:
        slow = st.checkbox(
            "Slow reading speed",
            value=False,
            help="Useful for dense material — gives your brain more time to absorb each sentence.",
        )

lang_code = LANGUAGES[language]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 1 — UPLOAD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div class="step-label">
  <div class="step-num">1</div>
  <div class="step-text">Upload your PDF</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    label="Drop your PDF here or click to browse",
    type=["pdf"],
    label_visibility="collapsed",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN FLOW
# Streamlit reruns this entire script on every user interaction. The guard
# below ensures we only attempt processing once a file has actually arrived.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if uploaded is not None:

    st.success(f"✅ **{uploaded.name}** uploaded successfully.")

    # ── Extract text ──────────────────────────────────────────────────────────
    with st.spinner("Reading your PDF…"):
        try:
            full_text, page_count = extract_text(uploaded)
        except Exception as err:
            st.error(
                f"❌ Could not read this PDF. Please make sure it contains real "
                f"selectable text rather than scanned images.\n\nDetail: {err}"
            )
            st.stop()

    if not full_text:
        st.markdown("""
        <div class="warn-banner">
          ⚠️ <strong>No readable text found.</strong> This PDF appears to be built
          from scanned images rather than real text. You will need to run OCR on it
          first — Adobe Acrobat, the free Tesseract OCR tool, or CamScanner OCR tool can do this —
          before this app can convert it to audio.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ── Stats ─────────────────────────────────────────────────────────────────
    word_count = len(full_text.split())
    est_mins   = max(1, round(word_count / 150))   # ~150 words per minute

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-val">{page_count}</span>
        <span class="stat-key">📄 Pages</span>
      </div>
      <div class="stat-card">
        <span class="stat-val">{word_count:,}</span>
        <span class="stat-key">📝 Words</span>
      </div>
      <div class="stat-card">
        <span class="stat-val">~{est_mins} min</span>
        <span class="stat-key">🎙️ Listen time</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Step 2 — Preview ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="step-label">
      <div class="step-num">2</div>
      <div class="step-text">Preview extracted text</div>
    </div>
    """, unsafe_allow_html=True)

    # Show up to 3 000 chars in the preview to keep the page snappy.
    # The full text is always used for audio generation.
    preview = full_text[:3000] + (
        "\n\n… [preview truncated — the full document will be included in the audio]"
        if len(full_text) > 3000 else ""
    )

    st.markdown(f"""
    <div class="preview-wrap">
      <div class="preview-bar">
        <div class="preview-dot" style="background:#FF5F57;"></div>
        <div class="preview-dot" style="background:#FEBC2E;"></div>
        <div class="preview-dot" style="background:#28C840;"></div>
        <span style="margin-left:0.4rem;">Extracted Text</span>
      </div>
      <div class="preview-text">{preview}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Step 3 — Generate audio ───────────────────────────────────────────────
    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="step-label">
      <div class="step-num">3</div>
      <div class="step-text">Generate &amp; download audio</div>
    </div>
    """, unsafe_allow_html=True)

    # session_state persists values across Streamlit reruns. Without this,
    # clicking "Download" would trigger a fresh script run and lose the buffer.
    if "audio_buf" not in st.session_state:
        st.session_state.audio_buf = None
    if "audio_filename" not in st.session_state:
        st.session_state.audio_filename = ""

    if st.button("🎙️  Generate Audio", use_container_width=True, type="primary"):
        with st.spinner(f"Converting {word_count:,} words to speech — please wait…"):
            try:
                st.session_state.audio_buf = make_audio(full_text, lang_code, slow)
                st.session_state.audio_filename = (
                    uploaded.name.replace(".pdf", "").replace(" ", "_") + "_audio.mp3"
                )
            except Exception as err:
                st.error(
                    f"❌ Audio generation failed. gTTS requires an active internet "
                    f"connection to reach Google's servers.\n\nDetail: {err}"
                )
                st.stop()

    if st.session_state.audio_buf is not None:
        st.markdown("**Listen right here:**")
        st.audio(st.session_state.audio_buf, format="audio/mp3")

        st.session_state.audio_buf.seek(0)   # Reset read position before download

        st.download_button(
            label="⬇️  Download MP3",
            data=st.session_state.audio_buf,
            file_name=st.session_state.audio_filename,
            mime="audio/mpeg",
            use_container_width=True,
        )

        st.markdown("""
        <div class="info-banner">
          💡 <strong>Study tip:</strong> Save the MP3 to your phone and listen
          during commutes or walks. Passive audio revision is a proven technique
          for reinforcing memory without needing to sit at a desk.
        </div>
        """, unsafe_allow_html=True)

else:
    # Empty state — displayed before the user uploads anything
    st.markdown("""
    <div class="empty-state">
      <span class="big-icon">📂</span>
      <p class="big-p">No file uploaded yet.</p>
      <p class="sm-p">Drag and drop a PDF above, or click the upload area to browse.</p>
      <p class="sm-p" style="margin-top:0.4rem;">Works great with lecture notes, textbooks, and study guides.</p>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div style="text-align:center; padding:2.5rem 0 1rem 0;
            font-family:'DM Sans',sans-serif; font-size:0.78rem;
            color:#9AA5B4; letter-spacing:0.04em;">
  Created by Raw Essence &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; Powered by gTTS &nbsp;·&nbsp; pdfplumber
</div>
""", unsafe_allow_html=True)
