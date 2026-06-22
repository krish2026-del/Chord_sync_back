from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import librosa
import numpy as np
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHORD_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

@app.post("/process-video")
async def process_audio(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"
    
    # Save the uploaded audio track directly
    with open(audio_path, "wb") as f:
        f.write(await file.read())
        
    try:
        # Load and analyze musical pitches
        y, sr = librosa.load(audio_path, sr=None)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        mean_chroma = np.mean(chroma, axis=1)
        dominant_note = CHORD_NAMES[np.argmax(mean_chroma)]
        
        return {
            "message": "Success",
            "chords": f"[{dominant_note}] Major Key Detected\n\nAnalysis complete."
        }
    except Exception as e:
        return {"message": "Error", "chords": str(e)}
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
