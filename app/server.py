import os
from typing import List, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ner_service import SecureBertNERProvider

app = FastAPI(title="SecureBERT NER API")

# Initialize the NER provider
# We assume the model is available at the path defined in config.py or relative to this file
ner_provider = SecureBertNERProvider()

class NERRequest(BaseModel):
    text: str

class NEREntity(BaseModel):
    entity_group: str
    word: str
    score: float
    start: int
    end: int

class NERResponse(BaseModel):
    entities: List[NEREntity]

@app.post("/extract", response_model=NERResponse)
async def extract_entities(request: NERRequest):
    if not request.text.strip():
        return NERResponse(entities=[])
    
    try:
        raw_entities = ner_provider.extract(request.text)
        # Ensure all required fields are present for the response model
        formatted_entities = []
        for ent in raw_entities:
            formatted_entities.append(NEREntity(
                entity_group=ent.get("entity_group", "UNKNOWN"),
                word=ent.get("word", ""),
                score=float(ent.get("score", 0.0)),
                start=ent.get("start", 0),
                end=ent.get("end", 0)
            ))
        return NERResponse(entities=formatted_entities)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
