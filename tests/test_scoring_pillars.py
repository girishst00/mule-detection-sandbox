import json
from pathlib import Path
from app.schemas.scenario import ScenarioGraphPayload
from app.core.scoring_pillars import compute_composite_risk_score

def test_scenario_04_scoring():
    # Update this line to use Path(__file__).parent
    fixture_path = Path(__file__).parent / "fixtures" / "scenario_04.json"
    
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = ScenarioGraphPayload(**data)
    result = compute_composite_risk_score(payload)

    assert result["scenario_id"] == "SCN-04"
    assert result["velocity_liquidation_pillar"] == 100.0
    assert result["composite_risk_score"] > 70.0
    assert result["status"] == "FLAGGED_HIGH_RISK"