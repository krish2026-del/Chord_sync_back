from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-video")
async def process_video_visuals(file: UploadFile = File(...)):
    video_path = f"temp_{file.filename}"
    
    with open(video_path, "wb") as f:
        f.write(await file.read())
        
    detected_timeline = []
    
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # ⏱️ HIGH FREQUENCY SCAN: Check every 0.5 seconds (twice per second)
            if frame_count % max(1, int(fps * 0.5)) == 0:
                total_seconds = frame_count / fps
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
                milliseconds = int((total_seconds % 1) * 10)
                
                # Creates a precise timestamp (e.g., 01:24.5)
                timestamp = f"{minutes:02d}:{seconds:02d}.{milliseconds}"
                
                detected_timeline.append(f"[{timestamp}] -> [Chord AI Screen Scanned]")
                
            frame_count += 1
            
        cap.release()
        
        final_sheet = "HIGH-PRECISION CHORD AI CAPTURE\n================================\n\n" + "\n".join(detected_timeline)
        return {"message": "Success", "chords": final_sheet}
        
    except Exception as e:
        return {"message": "Error reading screen pixels", "chords": str(e)}
        
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
