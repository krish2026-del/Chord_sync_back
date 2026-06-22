from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This tells the browser that DartPad is allowed to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Chord Sync API is up and running!"}

@app.post("/process-video")
async def process_video(file: UploadFile = File(...)):
    return {
        "message": "Video received successfully!",
        "filename": file.filename,
        "chords": "[G]                  [Em]\nTomake chueche bhalobashar morsum\n\n[C]                 [D]\nEkhon baje moner bhitor nishpapo nupur"
    }
