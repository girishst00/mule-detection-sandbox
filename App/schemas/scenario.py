from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class TransactionPayload(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    source_account_id: str = Field(..., description="Originating account ID")
    destination_account_id: str = Field(..., description="Receiving account ID")
    amount: float = Field(..., gt=0, description="Transfer amount in base currency")
    timestamp: datetime = Field(..., description="Timestamp of the transaction")
    institution_id: str = Field(..., description="Financial institution routing ID")

class AccountNode(BaseModel):
    account_id: str = Field(..., description="Unique account identifier")
    institution_id: str = Field(..., description="Bank or institution code")
    is_dormant: bool = Field(..., description="Flag indicating if account was dormant > 90 days")
    dormancy_duration_days: int = Field(..., ge=0, description="Total days of prior inactivity")
    kyc_risk_tier: str = Field(..., description="Initial KYC rating (LOW, MEDIUM, HIGH)")

class ScenarioGraphPayload(BaseModel):
    scenario_id: str = Field(..., description="Identifier like SCN-04")
    scenario_name: str = Field(..., description="Human-readable typology name")
    accounts: List[AccountNode] = Field(..., description="Set of accounts involved in the graph topology")
    transactions: List[TransactionPayload] = Field(..., description="Ordered list of transaction events")