from pathlib import Path
import json
from app.schemas.scenario import ScenarioGraphPayload

def test_scenario_04_payload_validation():
    fixture_path = Path(__file__).parent / "fixtures" / "scenario_04.json"
    assert fixture_path.exists(), "Fixture file scenario_04.json not found!"
    
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    payload = ScenarioGraphPayload(**data)
    assert payload.scenario_id == "SCN-04"