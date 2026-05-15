# 🧠 NeuroFit — Real-Time Voice-Based Mood Detection & Wellness Dashboard

NeuroFit is a real-time mental wellness web app that analyzes your voice to detect your emotional state and visualizes it on an interactive dashboard. Built with ML, Web, and Cloud technologies as a collaborative project.

---

## 🎯 What It Does

- 🎙️ Takes **voice input** from the user
- 📝 Transcribes speech using **OpenAI Whisper**
- 🤖 Classifies emotional state (happy, sad, angry, neutral, etc.) using **BERT**
- 📊 Displays results on a **real-time interactive dashboard**
- 🔐 Authenticates users and stores session data via **Firebase**

---

## 🏗️ Architecture

```
Voice Input
    ↓
Whisper (Speech-to-Text)
    ↓
BERT Model (Mood Classification)
    ↓
Flask Backend (REST API)
    ↓
Streamlit Frontend (Dashboard)
    ↓
Firebase (Auth + Real-Time Storage)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Speech-to-Text | OpenAI Whisper |
| Mood Classification | BERT (Hugging Face Transformers) |
| Backend | Flask |
| Frontend | Streamlit |
| Auth & Storage | Firebase |
| Data Handling | NumPy, Pandas |
| Version Control | Git + GitHub |

---

## 📁 Project Structure

```
neurofit/
├── backend/
│   ├── app.py                 # Flask API — main entry point
│   ├── whisper_model.py       # Speech-to-text transcription module
│   ├── bert_classifier.py     # Mood classification module
│   └── firebase_config.py     # Firebase initialization & helpers
├── frontend/
│   └── dashboard.py           # Streamlit dashboard UI
├── models/
│   └── bert_mood/             # Fine-tuned BERT model weights
├── utils/
│   └── audio_utils.py         # Audio recording & preprocessing helpers
├── requirements.txt
└── README.md
```

## 🧪 Models Used

**Whisper** (`openai/whisper-base`)
- Handles speech-to-text transcription from raw audio input
- Chosen for its accuracy across accents and noisy environments

**BERT** (`bert-base-uncased`)
- Fine-tuned for multi-class mood/emotion classification
- Input: transcribed text → Output: emotion label + confidence score

Mood labels supported:
`happy` · `sad` · `angry` · `neutral` · `fearful` · `surprised`

---

## 👥 Team

| Name | Role | GitHub |
|------|------|--------|
| Diya Bangad | ML + Backend | [@diyabangad](https://github.com/diyabangad) |
| Digvijay Nandan | Frontend + Firebase | [@digvijaynandan](https://github.com/digvijaynandan) |

---

## 🚧 Roadmap

- [ ] Multilingual support via Whisper large model
- [ ] Mood trend tracking over time with historical graphs
- [ ] Mobile-responsive UI
- [ ] Export mood session reports as PDF
- [ ] Real-time audio streaming instead of recorded input

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

