# api/schemas.py
from pydantic import BaseModel

class Message(BaseModel):
    message_id: int
    channel: str
    message: str
    views: int

class TopObject(BaseModel):
    detected_object_class: str
    count: int

class Activity(BaseModel):
    date: str
    count: int
