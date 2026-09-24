from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from pillars.velocity_engine import VelocityEngine
from pillars.graph_engine import GraphIntelligenceEngine
from pillars.scoring_engine import RiskOrchestrator

app = FastAPI(
    title="Multi-Pillar Mule Detection API",
    version="1.0.0",
    description="Sandbox prototype combining behavioral telemetry and network graph intelligence."
)

velocity_engine = VelocityEngine()
graph_engine = GraphIntelligenceEngine()
risk_orchestrator = RiskOrchestrator()

class EvaluationRequest(BaseModel):
    account_id: str
    current_transaction: Dict
    transaction_history: List[Dict]
    network_edges: Optional[List[Dict]] = []

@app.post("/evaluate-mule-risk")
def evaluate_risk(payload: EvaluationRequest):
    try:
        # 1. Evaluate Pillar 1: Velocity & Behavioral Telemetry
        v_res = velocity_engine.evaluate_velocity(
            payload.account_id, 
            payload.transaction_history, 
            payload.current_transaction
        )

        # 2. Ingest & Evaluate Pillar 2: Graph Intelligence
        if payload.network_edges:
            graph_engine.ingest_edges(payload.network_edges)
        g_res = graph_engine.analyze_node_topology(payload.account_id)

        # 3. Evaluate Pillar 3: Dynamic Orchestration
        decision = risk_orchestrator.orchestrate_decision(v_res, g_res)

        return {
            "status": "success",
            "evaluation": decision,
            "details": {
                "velocity_analysis": v_res,
                "graph_analysis": g_res
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))