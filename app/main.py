from fastapi import FastAPI, Query
import subprocess
import uuid
import os

app = FastAPI()

@app.get("/convert")
def convert_youtube_to_mp3(url: str = Query(...)):
    video_id = str(uuid.uuid4())
    output_path = f"/tmp/{video_id}.mp3"
    try:
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", f"/tmp/{video_id}.%(ext)s",
            url
        ], check=True)
        return {"status": "success", "file": f"/download/{video_id}.mp3"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "detail": str(e)}

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"/tmp/{filename}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    return {"status": "error", "message": "File not found"}
