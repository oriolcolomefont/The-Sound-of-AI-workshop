from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class QueryMessage(BaseModel):
    id: int 
    request: str

app = FastAPI()
router = APIRouter()

@router.post("/api/echo/")
def echo(query: QueryMessage):
    return { 
        "type": "response", 
        "id": query.id + 1,
        "text": query.request
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)