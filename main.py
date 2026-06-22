from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import easyocr
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the English text scanner model
reader = easyocr.Reader(['en'], gpu=False)

@app.post("/process-video")
async def process_video_visuals(file: UploadFile = File(...)):
    video_path = f"temp_{file.filename}"
    with open(video_path, "wb") as f:
        f.write(await file.read())
        
    detected_timeline = []
    last_chord = ""
    
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Scan frame pixels every 0.5 seconds
            if frame_count % max(1, int(fps * 0.5)) == 0:
                # 🎯 DIRECT SCAN: Since you pre-cropped it, we read the full frame directly
                result = reader.readtext(frame, detail=0)
                
                # Join the letters found together (e.g., "G", "C", "Am")
                detected_text = " ".join(result).strip() if result else ""
                
                # Only add if text is found and it's a new chord change
                if detected_text and detected_text != last_chord:
                    total_seconds = frame_count / fps
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    timestamp = f"{minutes:02d}:{seconds:02d}"
                    
                    detected_timeline.append(f"[{timestamp}]  {detected_text}")
                    last_chord = detected_text
                
            frame_count += 1
            
        cap.release()
        
        if not detected_timeline:
            final_sheet = "Video scanned successfully, but no text characters could be identified in the cropped area."
        else:
            final_sheet = "CHORD AI EXTREME ACCURACY SHEET\n===============================\n\n" + "\n".join(detected_timeline)
            
        return {"message": "Success", "chords": final_sheet}
        
    except Exception as e:
        return {"message": "Error processing video file", "chords": str(e)}
        
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
