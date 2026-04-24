from fastapi import FastAPI
import json
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "articles.json")

@app.get("/")
def root():
    return {"message": "API Wired Articles aktif"}

@app.get("/articles")
def get_articles():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "total": len(data),
            "articles": data
        }
    except Exception as e:
        return {"error": str(e)}