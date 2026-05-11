from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from analyze_chat import analyze_chat, parse_chat
import json
from io import StringIO
from pathlib import Path

app = FastAPI(title="WhatsApp Chat Analyzer", version="1.0.0")

# Mount static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse(Path(__file__).parent / "index.html")

@app.get("/health/")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload and analyze WhatsApp chat file"""
    try:
        content = await file.read()
        text = content.decode("utf-8")  
        
        if not text.strip():
            return {"error": "Empty file or unreadable content"}

        # Parse the chat data
        chat_data = parse_chat_from_text(text)
        
        if not chat_data:
            return {"error": "No valid messages found in file"}
        
        # Analyze the chat
        analysis = analyze_chat(chat_data)
        
        return {
            "filename": file.filename,
            "status": "success",
            "data": analysis
        }
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}", "status": "error"}

def parse_chat_from_text(text):
    """Parse chat text directly"""
    import re
    from datetime import datetime
    
    chat_data = []
    message_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[APM]{2}) - ([^:]+?): (.+)")
    
    for line in text.split("\n"):
        line = line.replace("\u202f", " ")
        match = message_pattern.match(line)
        if match:
            date_str, time_str, sender, message = match.groups()
            try:
                timestamp = datetime.strptime(date_str + ", " + time_str, "%m/%d/%y, %I:%M %p")
                chat_data.append({"timestamp": timestamp, "sender": sender, "message": message})
            except ValueError:
                continue
    
    return chat_data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)



