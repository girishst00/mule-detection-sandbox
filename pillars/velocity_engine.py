from datetime import datetime, timedelta
from typing import Dict, List

class VelocityEngine:
    """
    Pillar 1: Tracks micro-burst velocity, sudden dormancy inversion, 
    and pass-through ratios without introducing future look-ahead leakage.
    """
    def __init__(self, historical_window_days: int = 30):
        self.historical_window_days = historical_window_days

    def evaluate_velocity(self, account_id: str, transaction_history: List[Dict], current_tx: Dict) -> Dict:
        current_amount = current_tx.get("amount", 0.0)
        current_time = datetime.fromisoformat(current_tx.get("timestamp"))

        # Combine history and current transaction for unified window evaluation
        all_txs = transaction_history + [current_tx]
# Combine history and current transaction for unified window evaluation
        all_txs = transaction_history + [current_tx]

        # Filter transactions within a short trailing time window (e.g., last 1 hour)
        recent_window = current_time - timedelta(hours=1)
        recent_txs = [
            tx for tx in all_txs
            if datetime.fromisoformat(tx.get("timestamp")) >= recent_window
        ]

        burst_count = len(recent_txs)
        
        # Support both 'type' and 'direction' keys (case-insensitive check)
        total_inflow_recent = sum(
            tx.get("amount", 0.0) for tx in recent_txs 
            if str(tx.get("type", tx.get("direction", ""))).lower() in ["in", "inbound"]
        )
        total_outflow_recent = sum(
            tx.get("amount", 0.0) for tx in recent_txs 
            if str(tx.get("type", tx.get("direction", ""))).lower() in ["out", "outbound"]
        )

        # Pass-through ratio check (funds arriving and leaving almost instantly)
        pass_through_ratio = (
            min(total_inflow_recent, total_outflow_recent) / max(total_inflow_recent, 1.0)
        )
        
        # Dormancy inversion flag (account inactive for > 14 days, followed by sudden high volume)
        dormancy_flag = False
        if transaction_history:
            last_tx_time = datetime.fromisoformat(transaction_history[-1].get("timestamp"))
            inactivity_period = (current_time - last_tx_time).days
            if inactivity_period > 14 and current_amount > 50000:  # configurable threshold
                dormancy_flag = True

        risk_score = 0.0
        reasons = []

        if burst_count >= 5:
            risk_score += 0.4
            reasons.append(f"High frequency micro-burst: {burst_count} transactions in 1 hour.")
        if pass_through_ratio > 0.85 and total_inflow_recent > 10000:
            risk_score += 0.4
            reasons.append(f"High pass-through ratio detected: {pass_through_ratio:.2f}")
        if dormancy_flag:
            risk_score += 0.5
            reasons.append("Dormancy inversion pattern detected.")

        return {
            "account_id": account_id,
            "velocity_risk_score": min(risk_score, 1.0),
            "reasons": reasons,
            "metrics": {
                "burst_count": burst_count,
                "pass_through_ratio": pass_through_ratio,
                "dormancy_inversion": dormancy_flag
            }
        }