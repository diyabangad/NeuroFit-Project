import os
import tempfile
import streamlit as st
import requests
import numpy as np
import soundfile as sf
from streamlit_webrtc import AudioProcessorBase, WebRtcMode, webrtc_streamer
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="NeuroFit Voice Dashboard", page_icon="🎤", layout="centered")

st.title("🎙️ Real-Time Voice Mood Detection")
st.markdown("Use your microphone to record a short message, then click Analyze Mood.")

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []
        self.sample_rate = None

    # Support both recv and recv_queued to maximize compatibility
    def recv_queued(self, frame):
        audio = frame.to_ndarray()
        self.sample_rate = frame.sample_rate
        self.frames.append(audio)
        return frame

    def recv(self, frame):
        # Fallback for older streamlit-webrtc versions
        try:
            audio = frame.to_ndarray()
            self.sample_rate = frame.sample_rate
            self.frames.append(audio)
        except Exception:
            pass
        return frame

    def get_audio(self):
        if not self.frames:
            return None, None

        audio = np.concatenate(self.frames, axis=0)
        # Clear buffer after reading
        self.frames = []
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)
        return audio, self.sample_rate

ctx = webrtc_streamer(
    key="neurofit-audio",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

if ctx.audio_processor is not None:
    st.write("🎙️ Recording ready. Speak into your mic, then click Analyze Mood.")
    try:
        st.write(f"WebRTC state: {ctx.state.playing}")
    except Exception:
        pass

if ctx.audio_processor and st.button("🎤 Analyze Mood"):
    # show how many frames we captured
    try:
        total_frames = len(ctx.audio_processor.frames)
    except Exception:
        total_frames = 0
    st.write(f"Captured audio frames: {total_frames}")

    audio_data, sample_rate = ctx.audio_processor.get_audio()
    if audio_data is None or sample_rate is None:
        st.warning("No audio was recorded. Please check your microphone and try again.")
    else:
        if audio_data.dtype != np.int16:
            audio_data = np.int16(np.clip(audio_data, -1.0, 1.0) * 32767)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            sf.write(temp_wav.name, audio_data, sample_rate)
            temp_path = temp_wav.name

        try:
            with open(temp_path, "rb") as audio_file:
                response = requests.post("http://127.0.0.1:5000/analyze", files={"file": audio_file})

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
                st.subheader("📊 Mood Result")
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
                os.remove(temp_path)
            except OSError:
                pass

# JS recorder fallback UI
st.markdown("---")
st.header("Browser Recorder (fallback)")
audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="🛑 Stop & Analyze",
    just_once=True,
    use_container_width=True,
)

if audio and "bytes" in audio:
    st.info("Audio recorded (JS). Sending to backend for processing...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio["bytes"])
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as audio_file:
            response = requests.post("http://127.0.0.1:5000/analyze", files={"file": audio_file})

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Analysis complete (JS recorder)")
            st.subheader("📝 Transcription")
            transcription = result.get("transcription", "")
            if transcription:
                st.write(transcription)
            else:
                st.info("No transcription returned from the backend.")
                st.json(result)

            st.subheader("📊 Mood Result")
            st.write(
                f"**Mood:** {result.get('mood', 'unknown')}\n"
                f"**Sentiment:** {result.get('sentiment', 'unknown')}\n"
                f"**Confidence:** {result.get('confidence', 0)}"
            )
        else:
            st.error(f"Backend error: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Unable to reach backend: {e}")
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
