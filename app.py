import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from cohere import ClientV2
from gtts import gTTS

def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

if not api_key:
    st.error("❌ COHERE_API_KEY missing in .env!")
    st.stop()

co = ClientV2(api_key=api_key)


# ------------------------------
# Simple TTS helper (Japanese)
# ------------------------------
def japanese_tts(text: str) -> bytes:
    """Turn a Japanese string into MP3 audio bytes using gTTS."""
    if not text or not text.strip():
        return b""

    tts = gTTS(text=text, lang="ja")
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


# ------------------------------
# Render assistant message
# (text + sentence audio + per-word audio)
# ------------------------------
def render_assistant_message(raw_text: str):
    lines = [ln for ln in raw_text.splitlines() if ln.strip()]

    japanese_line = next((ln for ln in lines if ln.startswith("Japanese:")), "")
    romaji_line = next((ln for ln in lines if ln.startswith("Romaji:")), "")
    romaji_breakdown_line = next(
        (ln for ln in lines if ln.startswith("Romaji breakdown:")), ""
    )
    jlpt_line = next((ln for ln in lines if ln.startswith("JLPT:")), "")

    expl_index = next(
        (i for i, ln in enumerate(lines) if ln.strip().startswith("Explanation:")), None
    )

    explanation_lines = []
    if expl_index is not None:
        explanation_lines = lines[expl_index + 1 :]

    # ---------------- Sentence & high-level info ----------------
    if japanese_line:
        st.markdown(f"**{japanese_line}**")

    if romaji_line:
        st.markdown(romaji_line)
    if romaji_breakdown_line:
        st.markdown(romaji_breakdown_line)
    if jlpt_line:
        st.markdown(jlpt_line)

    jp_sentence = japanese_line.replace("Japanese:", "").strip()
    if jp_sentence:
        st.markdown("**🔊 Listen to the whole Japanese sentence:**")
        try:
            audio_bytes = japanese_tts(jp_sentence)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.info("Couldn't generate sentence audio.")
            st.text(str(e))

    # ---------------- Explanation + per-word audio ----------------
    if explanation_lines:
        st.markdown("**Explanation & word-by-word audio:**")

        for line in explanation_lines:
            if not line.strip().startswith("-"):
                continue

            bullet = line.strip()  

            core = bullet.lstrip("-").strip()
            for sep in ["(", "：", ":"]:
                if sep in core:
                    core = core.split(sep)[0]
            jp_word = core.strip()

            cols = st.columns([6, 2])
            with cols[0]:
                st.markdown(bullet)

            if jp_word:
                try:
                    audio_bytes = japanese_tts(jp_word)
                    if audio_bytes:
                        with cols[1]:
                            st.audio(audio_bytes, format="audio/mp3")
                except Exception:
                    pass


# ------------------------------
# Streamlit Page Setup
# ------------------------------
st.set_page_config(
    page_title="Translator Tutor",
    page_icon="🗾",
)

# Load external Japanese theme CSS
load_css("styles/japanese_theme.css")

st.title("翻訳 講師 Translator Tutor 🌸")
st.write(
    "Type any English sentence and get a natural Japanese translation with a short "
    "grammar/vocabulary explanation, **romaji breakdown**, and **audio** for the "
    "whole sentence plus each key word."
)

# ------------------------------
# Chat History
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_assistant_message(msg["content"])
        else:
            st.markdown(msg["content"])

# ------------------------------
# User Input
# ------------------------------
user_input = st.chat_input("Type your English sentence...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)


    prompt = f"""
You are a friendly Japanese language teacher.

For the English sentence below, do ALL of the following:

1. Translate it into natural Japanese that a native speaker might say.
2. Provide a normal romaji (Latin alphabet) version of the full sentence.
3. Provide a romaji breakdown with clear syllable-style splits (like a dictionary, using dots).
4. Decide the approximate JLPT level (N5–N1) of the Japanese sentence.
5. Give a short grammar and vocabulary explanation that is easy for a beginner to understand.

OUTPUT FORMAT — follow this EXACT format:

Japanese: <Japanese sentence>
Romaji: <full sentence in romaji>
Romaji breakdown: <romaji broken into syllables, using dots, e.g. Wa·ta·shi no na·ma·e wa ...>
JLPT: Nx
Explanation:
- <Japanese word or phrase> (<romaji breakdown for that word>): short explanation in English.
- (2–6 bullet points total; each bullet should start with "- ")

Notes:
- Use clear, easy romaji like "konnichiwa", "tabemasu", "ramen".
- For the romaji breakdown, split at natural mora/syllable boundaries using dots, like "ta·be·mo·no", "ra·a·men".
- The Explanation bullets should also help the learner see *how to pronounce* each key chunk by including that mini breakdown in parentheses.

Now do this for the following sentence:

English: "{user_input}"
"""

    with st.chat_message("assistant"):
        try:
            response = co.chat(
                model="command-r-08-2024",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=600,
            )

            raw_text = response.message.content[0].text.strip()

            st.session_state.messages.append(
                {"role": "assistant", "content": raw_text}
            )

            render_assistant_message(raw_text)

        except Exception as e:
            st.error("❌ Error talking to Cohere API.")
            st.error(str(e))
