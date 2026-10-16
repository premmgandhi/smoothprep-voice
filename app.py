import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="SmoothPrep Voice", page_icon="🎧", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
.stApp { background: radial-gradient(circle at 85% 0%, rgba(199,235,52,.09), transparent 27%), #071A16; color:#F4F7F3; }
.block-container {max-width:1150px;padding-top:2rem}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif}
.hero {padding:28px;border:1px solid #294139;border-radius:22px;background:linear-gradient(120deg,rgba(199,235,52,.09),rgba(255,255,255,.02));margin-bottom:20px}
.kicker {color:#C7EB34;font-weight:700;letter-spacing:.14em;font-size:.76rem}
.hero h1 {font-size:2.7rem;margin:.4rem 0}
.muted {color:#A6B9AF}
.box {background:#0D211B;border:1px solid #263E34;border-radius:16px;padding:18px}
.stButton>button {border-radius:12px;background:#C7EB34;color:#071A16;border:0;font-weight:700;min-height:2.7rem}
.stButton>button:hover {background:#d8f65a;color:#071A16}
.stTextArea textarea {background:#0B1713;color:#F4F7F3;border:1px solid #365146;border-radius:12px}
div[data-testid="stAudio"] {border-radius:14px}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
 <div class="kicker">SMOOTHPREP · VOICE</div>
 <h1>Turn your notes into <span style="color:#C7EB34">audio.</span></h1>
 <p class="muted">Your study material, spoken naturally. Listen while you revise, walk, or take a break.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.35, .85], gap="large")
with left:
    st.markdown("### 🎙️ Create your study audio")
    language = st.selectbox("Voice language", ["Hindi", "English", "Tamil", "Telugu", "Bengali", "Marathi", "Kannada", "Malayalam", "Gujarati", "Punjabi"])
    style = st.selectbox("Listening style", ["Clear study narration", "Quick revision", "Friendly explanation"])
    text_input = st.text_area("Paste your notes or text", height=250, placeholder="Paste a paragraph from your lecture notes here…")
    st.caption("Tip: Start with a short paragraph for the fastest generation.")
    generate = st.button("✨ Generate audio", use_container_width=True)
with right:
    st.markdown("### ⚡ How it works")
    st.markdown("""
    <div class="box">
    <p>① <b>Paste</b><br><span class="muted">Add notes, articles, or a concept.</span></p>
    <p>② <b>Choose a language</b><br><span class="muted">Pick the language you want to listen in.</span></p>
    <p>③ <b>Listen & revise</b><br><span class="muted">Generate speech and play it right here.</span></p>
    <hr style="border-color:#263E34">
    <span class="muted">Powered by Sarvam AI text-to-speech when API credentials are configured.</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("#### Good for")
    st.write("📚 Lecture notes")
    st.write("📝 Quick revision")
    st.write("♿ Audio-first learning")
    st.write("🚶 Study while on the move")

if generate:
    if not text_input.strip():
        st.warning("Paste some text first.")
    elif len(text_input) > 4000:
        st.warning("For this quick prototype, please use a shorter passage (under 4,000 characters).")
    else:
        key = os.getenv("SARVAM_API_KEY", "").strip()
        if not key:
            st.error("SARVAM_API_KEY is missing. Add it to a .env file to generate real audio. This prototype does not fake generated audio.")
        else:
            with st.spinner("Generating speech with Sarvam AI…"):
                try:
                    from sarvamai import SarvamAI
                    client = SarvamAI(api_subscription_key=key)
                    # Current Sarvam SDK uses text_to_speech.convert; expose errors honestly if SDK differs.
                    lang_map = {"Hindi":"hi-IN","English":"en-IN","Tamil":"ta-IN","Telugu":"te-IN","Bengali":"bn-IN","Marathi":"mr-IN","Kannada":"kn-IN","Malayalam":"ml-IN","Gujarati":"gu-IN","Punjabi":"pa-IN"}
                    response = client.text_to_speech.convert(
                        text=text_input,
                        language_code=lang_map[language],
                        model="bulbul:v3",
                    )
                    audio_data = None
                    if hasattr(response, "audios") and response.audios:
                        import base64
                        audio_data = base64.b64decode(response.audios[0])
                    elif isinstance(response, dict) and response.get("audios"):
                        import base64
                        audio_data = base64.b64decode(response["audios"][0])
                    if audio_data:
                        st.success("Audio generated successfully.")
                        st.audio(audio_data, format="audio/wav")
                        st.download_button("⬇️ Download audio", audio_data, file_name="smoothprep_voice.wav", mime="audio/wav")
                    else:
                        st.error("The API returned, but the audio format was not recognized by this prototype. See terminal output or check the current Sarvam SDK response format.")
                except Exception as e:
                    st.error(f"Audio generation failed: {type(e).__name__}: {e}")
                    st.info("Check your API key, model availability, and current Sarvam SDK syntax.")
st.markdown("---")
st.caption("SmoothPrep Voice · Buildathon prototype · Live audio requires a valid Sarvam API key.")
