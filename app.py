import streamlit as st
import base64
import requests
import edge_tts
import asyncio
from deep_translator import GoogleTranslator

async def generate_edge_speech(text, voice):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save("output.mp3")
    return "output.mp3"



# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="VoiceCraft AI",
    page_icon="🎧",
    layout="centered"
)

# ---------- CUSTOM CSS (PRO LOOK) ----------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #e6f2ff;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #9ec9ff;
    margin-bottom: 30px;
}

.stButton>button {
    background-color: #4fc3f7;
    color: black;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.6em 1.2em;
}

.stDownloadButton>button {
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🎧 VoiceCraft AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">✨ Convert your text into natural speech instantly</div>', unsafe_allow_html=True)

# ---------- TEXT INPUT ----------
text = st.text_area("📝 Enter your text", height=150)
# 🌍 Translate language selector
translate_options = {
    "🇺🇸 English": "en",
    "🇮🇳 Hindi": "hi",
    "🌸 Telugu": "te",
    "🎶 Tamil": "ta",
    "🪔 Bengali": "bn",
    "💠 Gujarati": "gu",
    "🎵 Kannada": "kn",
    "🌿 Malayalam": "ml",
    "🪶 Punjabi": "pa"
}

target_lang_name = st.selectbox(
    "🌐 Translate text to",
    list(translate_options.keys())
)

target_lang = translate_options[target_lang_name]

# ---------- LANGUAGES ----------
voices = {
    "🇺🇸 English (Female)": "en-US-JennyNeural",
    "🇺🇸 English (Male)": "en-US-GuyNeural",
    "🇮🇳 Hindi (Female)": "hi-IN-SwaraNeural",
    "🇮🇳 Hindi (Male)": "hi-IN-MadhurNeural",
    "🌸 Telugu": "te-IN-ShrutiNeural",
    "🎶 Tamil": "ta-IN-PallaviNeural",
    "🪔 Bengali": "bn-IN-TanishaaNeural",
    "💠 Gujarati": "gu-IN-DhwaniNeural",
    "🎵 Kannada": "kn-IN-SapnaNeural",
    "🌿 Malayalam": "ml-IN-SobhanaNeural",
    "🪶 Punjabi": "pa-IN-GaganNeural"
}

# 🎯 auto voice mapping based on translate language
auto_voice_map = {
    "en": "en-US-JennyNeural",
    "hi": "hi-IN-SwaraNeural",
    "te": "te-IN-ShrutiNeural",
    "ta": "ta-IN-PallaviNeural",
    "bn": "bn-IN-TanishaaNeural",
    "gu": "gu-IN-DhwaniNeural",
    "kn": "kn-IN-SapnaNeural",
    "ml": "ml-IN-SobhanaNeural",
    "pa": "pa-IN-GaganNeural"
}
# 📝 Show translated text
translated_text = ""

if text.strip():
    try:
        if target_lang != "en":
            translated_text = GoogleTranslator(
                source="auto",
                target=target_lang
            ).translate(text)
        else:
            translated_text = text
    except:
        translated_text = text

st.text_area(
    "📝 Translated text",
    value=translated_text,
    height=120,
    disabled=True
)

# 🔊 auto-select voice based on translation language
voice = auto_voice_map.get(target_lang, "en-US-JennyNeural")


st.markdown("<br>", unsafe_allow_html=True)

# ---------- GENERATE ----------
if st.button("🔊 Generate Speech"):

    if text.strip():

        with st.spinner("🎙️ Generating your audio..."):

            
            
            
            # 🔊 then generate speech
            # 🔊 generate speech using already translated text
            file_path = asyncio.run(generate_edge_speech(translated_text, voice))
            if file_path:
              # 🔥 AUTO PLAY
              with open(file_path, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()

                audio_html = f"""
                    <audio autoplay controls style="width:100%;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

              # download
              with open(file_path, "rb") as f:
                st.download_button(
                  label="⬇️ Download MP3",
                  data=f,
                  file_name="voicecraft_output.mp3",
                  mime="audio/mp3"
                )
            else:
              st.error("❌ Audio generation failed. Check API key.")


            

            

