import spacy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os

# Initialize FastAPI app
app = FastAPI(
    title="NER11 Gold Standard API",
    description="High-performance Named Entity Recognition API using the NER11 Gold Standard Model.",
    version="1.0.0"
)

# Global model variable
nlp = None
MODEL_PATH = os.getenv("MODEL_PATH", "models/ner11_v3/model-best")

@app.on_event("startup")
async def load_model():
    global nlp
    try:
        print(f"Loading NER11 Gold Standard model from {MODEL_PATH}...")
        nlp = spacy.load(MODEL_PATH)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        # Fallback to checking if it's in the root or other locations if needed
        raise RuntimeError(f"Failed to load model: {e}")

class TextRequest(BaseModel):
    text: str

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    score: float = 1.0  # spaCy NER doesn't always give per-entity confidence, defaulting to 1.0

class NerResponse(BaseModel):
    entities: List[Entity]
    doc_length: int

@app.post("/ner", response_model=NerResponse)
async def extract_entities(request: TextRequest):
    if not nlp:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    doc = nlp(request.text)
    
    entities = []
    for ent in doc.ents:
        entities.append(Entity(
            text=ent.text,
            label=ent.label_,
            start=ent.start_char,
            end=ent.end_char
        ))
    
    return NerResponse(entities=entities, doc_length=len(doc))

@app.get("/health")
async def health_check():
    if nlp:
        return {"status": "healthy", "model": "loaded"}
    return {"status": "unhealthy", "model": "not_loaded"}

@app.get("/info")
async def model_info():
    if nlp:
        return {
            "model_name": "NER11 Gold Standard",
            "version": "3.0",
            "pipeline": nlp.pipe_names,
            "labels": nlp.get_pipe("ner").labels
        }
    return {"status": "model_not_loaded"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
