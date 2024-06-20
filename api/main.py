import os
import subprocess

from clean_action import clean_action
from describe_action import describe_action
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generate_score import generate_score_action
from pydantic import BaseModel
from variate_action import variate_action

ASSETS_PATH = f"../client/public/assets"

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
        "text": query.prompt,
        "melody": query.melody
    }

@router.post("/api/describe/")
def describe(query: QueryMessage):
    [melody, uuid] = describe_action(query.melody, ASSETS_PATH)

    return { 
        "type": "response", 
        "id": query.id + 1,
        "text": "Generated variation:",
        "melody": melody,
        "uuid": uuid,
    }    

@router.post("/api/clean/")
def clean(query: QueryMessage):
    [melody, uuid] = clean_action(query.melody, ASSETS_PATH)

    print(f"Cleaned melody {uuid}: {melody}")

    return { 
        "type": "response", 
        "id": query.id + 1,
        "text": "Here's your melody:",
        "melody": melody,
        "uuid": uuid,
    }
    
@router.post("/api/variate/")
def variate(query: QueryMessage): 
    [melody, uuid] = variate_action(query.melody, ASSETS_PATH)

    print(f"Variated melody {uuid}: {melody}")
    
    return {
        "type": "response",
        "id": query.id + 1,
        "text": "Here's your variated melody:",
        "melody": melody,
        "uuid": uuid,
    }

@router.post("/api/generate/")
def generate(query: QueryMessage): 
    [melody, uuid] = generate_score_action(query.prompt, ASSETS_PATH)

    print(f"Variated melody {uuid}: {melody}")
    
    return {
        "type": "response",
        "id": query.id + 1,
        "text": "Here's your variated melody:",
        "melody": melody,
        "uuid": uuid,
    }
    

app.include_router(router)