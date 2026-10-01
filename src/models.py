from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class StateCode(str, Enum):
    CA = "CA"
    FL = "FL"
    TX = "TX"
    NY = "NY"
    MA = "MA"
    IL = "IL"
    AZ = "AZ"


class TradeCategory(str, Enum):
    ROOFING = "roofing"
    HVAC = "hvac"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    GENERAL_CONTRACTOR = "general_contractor"
    ANY = "any"


class LicenseStatus(str, Enum):
    ACTIVE_CURRENT = "ACTIVE/CURRENT"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    INACTIVE = "INACTIVE"
    CANCELLED = "CANCELLED"
    NOT_FOUND = "NOT_FOUND"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LicenseVerificationResult(BaseModel):
    verified: bool
    canonical_name: str
    dba_name: Optional[str] = None
    license_number: str
    state: str
    trade_classification: str
    status: str
    is_active: bool
    workers_comp_covered: bool
    workers_comp_insurer: Optional[str] = None
    bond_status: Optional[str] = None
    disciplinary_actions: int = 0
    expiration_date: Optional[str] = None
    source_registry: str
    grounding_confidence: float
    cached: bool = False
    cached_at: Optional[str] = None


class ComplianceRiskResult(BaseModel):
    can_hire: bool
    risk_level: str
    risk_score: float
    flags: List[str] = Field(default_factory=list)
    license_result: Optional[Dict[str, Any]] = None
    sam_debarred: bool = False
    osha_violation_count: int = 0
    summary: str


class ContractorItem(BaseModel):
    canonical_name: str
    dba_name: Optional[str] = None
    license_number: str
    state: str
    trade_classification: str
    status: str
    city: Optional[str] = None
    phone: Optional[str] = None
    workers_comp_covered: bool = False


class ContractorSearchResult(BaseModel):
    query_state: str
    query_trade: str
    total_found: int
    contractors: List[ContractorItem] = Field(default_factory=list)


class FederalDebarmentResult(BaseModel):
    entity_name: str
    is_debarred: bool
    exclusion_type: Optional[str] = None
    sam_record_found: bool = False
    classification: Optional[str] = None
    status: str
    timestamp: str


class OshaSafetyAuditResult(BaseModel):
    entity_name: str
    total_violations: int = 0
    serious_violations: int = 0
    willful_violations: int = 0
    repeat_violations: int = 0
    total_penalties_usd: float = 0.0
    inspection_count: int = 0
    status: str
    safety_rating: str
