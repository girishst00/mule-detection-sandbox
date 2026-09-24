from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from services import create_pillar_record, get_pillar_record

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Pillar Sandbox API", version="2.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MetricItem(BaseModel):
    pillar_name: str
    metric_score: float = 0.0
    details: str | None = None

class PillarCreateRequest(BaseModel):
    entity_reference: str
    metrics: list[MetricItem]

@app.post("/pillars/")
def create_pillar_endpoint(payload: PillarCreateRequest, db: Session = Depends(get_db)):
    metrics_data = [m.model_dump() for m in payload.metrics]
    record = create_pillar_record(db, entity_ref=payload.entity_reference, metrics_data=metrics_data)
    return {"status": "success", "id": record.id, "entity_reference": record.entity_reference}

@app.get("/pillars/{record_id}")
def read_pillar_endpoint(record_id: int, db: Session = Depends(get_db)):
    record = get_pillar_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {
        "id": record.id,
        "entity_reference": record.entity_reference,
        "status": record.status,
        "metrics": [{"pillar_name": m.pillar_name, "metric_score": m.metric_score, "details": m.details} for m in record.pillar_metrics]
    }

from services import evaluate_pillar_risk

@app.post('/evaluate/')
def evaluate_entity_endpoint(payload: PillarCreateRequest):
    metrics_data = [m.model_dump() for m in payload.metrics]
    evaluation = evaluate_pillar_risk(metrics_data)
    return {
        'entity_reference': payload.entity_reference,
        'evaluation_summary': evaluation
    }
