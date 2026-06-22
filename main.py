from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Chord Sync API is up and running!"}

@app.post("/process-video")
async def process_video(file: UploadFile = File(...)):
    return {
        "message": "Video received successfully!",
        "filename": file.filename,
        "lyrics_and_chords": "[G]                  [Em]\nTomake chueche bhalobashar morsum\n\n[C]                 [D]\nEkhon baje moner bhitor nishpapo nupur"
    }
