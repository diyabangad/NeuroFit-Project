import os
import torch
import whisper
from transformers import pipeline

# Optional Vosk fallback
try:
    from ml_model.hello import transcribe_audio as vosk_transcribe
except Exception:
    vosk_transcribe = None

# Load Whisper model (for transcription)
print("🔁 Loading Whisper model... (this may take a minute)")
whisper_model = whisper.load_model("base")
print("✅ Whisper model loaded.")

# Load Hugging Face sentiment analysis model
print("🧠 Loading sentiment analysis model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=0 if device == "cuda" else -1)
print("✅ Sentiment model loaded.")


def process_audio_file(file_path):
    """
    1. Transcribe speech → text with Whisper
    2. Run sentiment analysis on transcription
    3. Map sentiment → mood + Spotify playlist
    """

    # Step 1: Transcribe audio with Whisper
    print(f"🎙️ Transcribing with Whisper: {file_path}")
    try:
        result = whisper_model.transcribe(file_path)
        text = result.get("text", "").strip()
    except Exception as e:
        print("⚠️ Whisper transcription error:", e)
        text = ""

    # If Whisper returned empty transcription and Vosk is available, try Vosk
    if (not text) and vosk_transcribe is not None:
        try:
            print("🔁 Whisper returned empty; falling back to Vosk...")
            vosk_text = vosk_transcribe(file_path)
            if vosk_text:
                text = vosk_text.strip()
                print("✅ Vosk fallback transcription obtained.")
        except Exception as e:
            print("⚠️ Vosk fallback failed:", e)

    # Step 2: Sentiment analysis
    if text:
        sentiment = sentiment_pipeline(text)[0]
        label = sentiment["label"]
        score = sentiment["score"]
    else:
        label = "NEUTRAL"
        score = 0.0

    # Step 3: Map to mood categories
    if label == "POSITIVE":
        mood = "Happy"
        playlist = "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC"
    elif label == "NEGATIVE":
        mood = "Sad"
        playlist = "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1"
    else:
        mood = "Neutral"
        playlist = "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"

    # Step 4: Return results
    return {
        "transcription": text,
        "sentiment": label,
        "confidence": round(score, 2),
        "mood": mood,
        "spotify_playlist": playlist
    }
