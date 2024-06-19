import os
import subprocess

from abc2wav import render_abc_wav
from abc_clean import clean_abc
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import create_uuid, get_absolute_path_from_relative_to_source
from variate import variate_abc_melody

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



router = APIRouter()

class QueryMessage(BaseModel):
    id: int 
    prompt: str
    melody: str

@router.post("/api/echo/")
def echo(query: QueryMessage):
    return { 
        "type": "response", 
        "id": query.id + 1,
        "text": query.prompt
    }

@router.post("/api/clean/")
def clean(query: QueryMessage):
    input_file_path = "./clean.abc"
    
    # Save query.request content to input.abc file
    with open(input_file_path, 'w') as file:
        file.write(query.melody)
    
    
    try:
        result = subprocess.run(["python", "../abc-utils/clean1.py", input_file_path], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"{result.stderr}")

        melody = clean_abc(query.melody)
        random = create_uuid(melody)
        wav_file = f"../client/public/{random}.wav"
        wav_output = get_absolute_path_from_relative_to_source(wav_file)

        # render_abc only if file not exists
        if not os.path.exists(wav_output):
            render_abc_wav(query.melody, wav_output)

        return { 
            "type": "response", 
            "id": query.id + 1,
            "text": "Here's your melody:",
            "melody": melody,
            "wav": f"/{random}.wav"
        }
    except subprocess.CalledProcessError as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Script execution failed: {e.stderr}")
    
@router.post("/api/variate/")
def variate(query: QueryMessage): 
    melody = variate_abc_melody(query.melody)
    random = create_uuid(melody)
    wav_file = f"../client/public/{random}.wav"
    wav_output = get_absolute_path_from_relative_to_source(wav_file)
    
    render_abc_wav(melody, wav_output)    

    return {
        "type": "response",
        "id": query.id + 1,
        "text": "Here's your variated melody:",
        "melody": query.melody,
        "wav": f"/{random}.wav"    
    }
    

app.include_router(router)