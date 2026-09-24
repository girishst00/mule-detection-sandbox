from sqlalchemy.orm import Session
from models import PillarMasterModel, PillarMetricModel

def create_pillar_record(db: Session, entity_ref: str, metrics_data: list):
    db_master = PillarMasterModel(entity_reference=entity_ref)
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    
    for metric in metrics_data:
        db_metric = PillarMetricModel(
            master_id=db_master.id,
            pillar_name=metric.get("pillar_name"),
            metric_score=metric.get("metric_score", 0.0),
            details=metric.get("details")
        )
        db.add(db_metric)
        
    db.commit()
    db.refresh(db_master)
    return db_master

def get_pillar_record(db: Session, record_id: int):
    return db.query(PillarMasterModel).filter(PillarMasterModel.id == record_id).first()


def evaluate_pillar_risk(metrics_data):
    if not metrics_data:
        return {'average_score': 0.0, 'risk_tier': 'Low'}
    scores = [m.get('metric_score', 0.0) for m in metrics_data]
    avg_score = sum(scores) / len(scores)
    if avg_score >= 75:
        tier = 'High'
    elif avg_score >= 40:
        tier = 'Medium'
    else:
        tier = 'Low'
    return {'average_score': round(avg_score, 2), 'risk_tier': tier}
