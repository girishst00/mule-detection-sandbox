from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from services import create_pillar_record, get_pillar_record, evaluate_pillar_risk

app = FastAPI(title="Mule Detection Sandbox", version="1.0.0")

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
    return {
        "status": "success",
        "id": record.id,
        "entity_reference": record.entity_reference,
        "risk_score": record.risk_score,
        "risk_tier": record.risk_tier
    }

@app.get("/pillars/{record_id}")
def read_pillar_endpoint(record_id: int, db: Session = Depends(get_db)):
    record = get_pillar_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {
        "id": record.id,
        "entity_reference": record.entity_reference,
        "status": record.status,
        "risk_score": record.risk_score,
        "risk_tier": record.risk_tier,
        "metrics": [{"pillar_name": m.pillar_name, "metric_score": m.metric_score, "details": m.details} for m in record.pillar_metrics]
    }

@app.post('/evaluate/')
def evaluate_entity_endpoint(payload: PillarCreateRequest):
    metrics_data = [m.model_dump() for m in payload.metrics]
    evaluation = evaluate_pillar_risk(metrics_data)
    return {
        'entity_reference': payload.entity_reference,
        'evaluation_summary': evaluation
    }
