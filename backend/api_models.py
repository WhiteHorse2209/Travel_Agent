from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str

class EmailRequest(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str
    thread_id: str
