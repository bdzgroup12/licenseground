import pytest
from unittest.mock import AsyncMock, patch
from src.models import (
    LicenseVerificationResult,
    ComplianceRiskResult,
    ContractorSearchResult,
    FederalDebarmentResult,
    OshaSafetyAuditResult,
)
from src.client import LicenseGroundClient
from src.server import mcp


def test_models_validation():
    verif = LicenseVerificationResult(
        verified=True,
        canonical_name="ACME ROOFING LLC",
        license_number="123456",
        state="CA",
        trade_classification="roofing",
        status="ACTIVE",
        is_active=True,
        workers_comp_covered=True,
        source_registry="CSLB",
        grounding_confidence=0.98,
    )
    assert verif.verified is True
    assert verif.canonical_name == "ACME ROOFING LLC"

    comp = ComplianceRiskResult(
        can_hire=True,
        risk_level="LOW",
        risk_score=95.0,
        flags=[],
        summary="Compliant contractor.",
    )
    assert comp.can_hire is True
    assert comp.risk_level == "LOW"


def test_client_headers():
    client = LicenseGroundClient(api_key="lg_test_key_123")
    headers = client._headers()
    assert headers["X-Agent-API-Key"] == "lg_test_key_123"
    assert "LicenseGround-MCP-Client" in headers["User-Agent"]


@pytest.mark.asyncio
async def test_client_verify_license_mock():
    client = LicenseGroundClient(api_key="lg_test_key_123")
    mock_response = {
        "verified": True,
        "canonical_name": "SUNSET ELECTRIC INC",
        "license_number": "987654",
        "state": "CA",
        "trade_classification": "electrical",
        "status": "ACTIVE",
        "is_active": True,
        "workers_comp_covered": True,
        "source_registry": "CSLB",
        "grounding_confidence": 0.99,
    }

    with patch.object(client, "_post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await client.verify_license(state="CA", entity_name="Sunset Electric")
        assert result["verified"] is True
        assert result["canonical_name"] == "SUNSET ELECTRIC INC"
        mock_post.assert_awaited_once_with(
            "/v1/verify",
            {
                "state": "CA",
                "entity_name": "Sunset Electric",
                "license_number": None,
                "trade": "any",
                "city": None,
            },
        )


def test_mcp_tools_registered():
    tools = [tool.name for tool in mcp._tool_manager.list_tools()]
    expected_tools = [
        "verify_license",
        "check_compliance_risk",
        "search_contractors",
        "check_federal_debarment",
        "audit_osha_safety",
        "get_registry_status",
    ]
    for expected in expected_tools:
        assert expected in tools
