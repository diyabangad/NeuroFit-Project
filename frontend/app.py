import os
import tempfile
import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="NeuroFit Voice Dashboard",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 NeuroFit Voice Dashboard")
st.markdown("Record a short message using the browser recorder, then analyze mood and transcription.")

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="🛑 Stop & Analyze",
    just_once=True,
    use_container_width=True,
)

if audio and "bytes" in audio:
    st.info("Audio recorded. Sending to backend for processing...")

    # Save recorded bytes to a temp WAV file and send
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio["bytes"])
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            response = requests.post("http://127.0.0.1:5000/analyze", files={"file": f})

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Analysis complete")
            st.subheader("📝 Transcription")
            transcription = result.get("transcription", "")
            if transcription:
                st.write(transcription)
            else:
                st.info("No transcription returned from the backend.")
                st.json(result)

            st.subheader("📊 Mood Analysis")
            st.write(
                f"**Mood:** {result.get('mood', 'unknown')}\n"
                f"**Sentiment:** {result.get('sentiment', 'unknown')}\n"
                f"**Confidence:** {result.get('confidence', 0)}"
            )

            playlist = result.get("spotify_playlist")
            if playlist:
                st.markdown(f"[Open Playlist 🎵]({playlist})")
        else:
            st.error(f"Backend error: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Unable to reach backend: {e}")

    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
