from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from auth import current_user
from models import User
from schemas import ChatRequest, ChatResponse
from services.llm_service import chat_with_tools

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, user: User = Depends(current_user), db: Session = Depends(get_db)):
    reply = chat_with_tools(payload.message.strip(), db, user.id)
    return {"response": reply}
