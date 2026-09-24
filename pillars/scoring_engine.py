from typing import Dict

class RiskOrchestrator:
    """
    Pillar 3: Aggregates velocity signals and graph topology metrics 
    to generate an adaptive risk score and recommended action.
    """
    def __init__(self, velocity_weight: float = 0.5, graph_weight: float = 0.5):
        self.velocity_weight = velocity_weight
        self.graph_weight = graph_weight

    def orchestrate_decision(self, velocity_result: Dict, graph_result: Dict) -> Dict:
        v_score = velocity_result.get("velocity_risk_score", 0.0)
        g_score = graph_result.get("structural_risk_score", 0.0)
        
        composite_score = (v_score * self.velocity_weight) + (g_score * self.graph_weight)
        
        # Decision gating & friction orchestration
        if composite_score >= 0.75:
            action = "BLOCK_TRANSACTION"
            friction_level = "HIGH_BLOCK"
        elif composite_score >= 0.45:
            action = "STEP_UP_AUTHENTICATION"
            friction_level = "BIOMETRIC_OR_OTP_CHALLENGE"
        else:
            action = "ALLOW"
            friction_level = "NONE"

        combined_reasons = velocity_result.get("reasons", []) + graph_result.get("topology_notes", [])

        return {
            "account_id": velocity_result.get("account_id"),
            "composite_risk_score": round(composite_score, 4),
            "recommended_action": action,
            "friction_level": friction_level,
            "explanation_codes": combined_reasons
        }