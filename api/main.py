# api/main.py
from fastapi import FastAPI
from typing import List
from . import crud, schemas

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Telegram Analytics API"}

@app.get("/api/reports/top-products", response_model=List[schemas.TopObject])
def top_objects(limit: int = 10):
    return crud.get_top_objects(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.Activity])
def channel_activity(channel_name: str):
    return crud.get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=List[schemas.Message])
def search(query: str):
    return crud.search_messages(query)
