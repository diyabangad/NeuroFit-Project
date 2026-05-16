# NeuroFit — Voice Mood Detection App

This project is a simple Flask + Streamlit app that records audio from your browser microphone, transcribes the speech, and detects mood using sentiment analysis.

## Project structure

- `backend/app.py` — Flask API that receives audio and returns mood results
- `frontend/app.py` — Streamlit UI for recording audio in the browser and displaying the analysis
- `ml_model/whisper_mood_pipeline.py` — transcription + sentiment pipeline
- `backend/requirements.txt` — backend dependencies
- `frontend/requirements.txt` — frontend dependencies

## Setup

1. Open a terminal in the project root:
   ```powershell
   cd "C:\Users\Home PC\OneDrive\Desktop\project\NeuroFit-Project"
   ```
2. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Upgrade pip:
   ```powershell
   python -m pip install --upgrade pip
   ```
4. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
   or install backend and frontend separately:
   ```powershell
   python -m pip install -r backend\requirements.txt
   python -m pip install -r frontend\requirements.txt
   ```

## Run the app

1. Start the backend in one terminal:
   ```powershell
   python backend\app.py
   ```
2. Start the frontend in another terminal:
   ```powershell
   streamlit run frontend\app.py
   ```
3. Open the browser link shown by Streamlit.
4. Allow microphone access, speak into the mic, and click **Analyze Mood**.

## Screenshot (working app)

_Add your screenshot here:_

`![NeuroFit working screenshot](path/to/your-screenshot.png)`

## Notes

- The frontend records audio in the browser using your microphone.
- The backend uses Whisper for transcription and sentiment classification.
- If you have issues installing packages, make sure Python and pip are correctly configured.


