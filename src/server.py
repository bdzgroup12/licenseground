import asyncio
import logging
import sys
from typing import Optional, Dict, Any

from mcp.server.fastmcp import FastMCP

from src.client import licenseground_client

logger = logging.getLogger(__name__)

# Initialize FastMCP Client Connector
mcp = FastMCP(
    name="LicenseGround - Trade Contractor & Regulatory Truth",
    instructions=(
        "Official client connector for LicenseGround Cloud Regulatory APIs. "
        "Verifies trade contractor licenses, standing, disciplinary orders, workers' comp insurance, "
        "and surety bonds across California (CSLB), Florida (DBPR), Texas (TDLR), New York (NYC DOB), "
        "Massachusetts (CSL), Illinois (Chicago DOB), and Arizona (ROC), "
        "as well as Federal SAM.gov debarment and OSHA safety violation audits."
    ),
)


@mcp.tool()
async def verify_license(
    state: str,
    entity_name: Optional[str] = None,
    license_number: Optional[str] = None,
    trade: str = "any",
    city: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Verify an entity's trade contractor license against official state licensing boards.

    Args:
        state: Two-letter US state code ('CA', 'FL', 'TX', 'NY', 'MA', 'IL', or 'AZ'). Required.
        entity_name: The company name, DBA, or contractor name to verify (e.g. 'Apex Roofing LLC').
        license_number: The official state license or certificate ID (e.g. '1058291', 'CCC1330999', 'TACLA29188C').
        trade: Trade category: 'roofing', 'hvac', 'electrical', 'plumbing', 'general_contractor', or 'any'. Default is 'any'.
        city: Optional city to filter geographic disambiguation.

    Returns:
        Deterministic, machine-actionable JSON containing verification status, canonical name,
        active standing, disciplinary action count, workers' compensation status, bond status, and confidence score.
    """
    return await licenseground_client.verify_license(
        state=state,
        entity_name=entity_name,
        license_number=license_number,
        trade=trade,
        city=city,
    )


@mcp.tool()
async def check_compliance_risk(
    state: str,
    entity_name: Optional[str] = None,
    license_number: Optional[str] = None,
    trade: str = "any",
    require_workers_comp: bool = True,
    require_surety_bond: bool = True,
    max_disciplinary_actions: int = 0,
    min_confidence_score: float = 0.85,
) -> Dict[str, Any]:
    """
    Perform an automated compliance and liability risk assessment for autonomous onboarding, hiring, or payments.

    Args:
        state: Two-letter US state code ('CA', 'FL', 'TX', 'NY', 'MA', 'IL', or 'AZ'). Required.
        entity_name: Company name or DBA to assess.
        license_number: State license number to assess.
        trade: Trade category: 'roofing', 'hvac', 'electrical', 'plumbing', 'general_contractor', or 'any'.
        require_workers_comp: If true, fails compliance if no verified workers' comp policy is active on file.
        require_surety_bond: If true, fails compliance if contractor bond is inactive or missing.
        max_disciplinary_actions: Maximum allowed board citations or disciplinary orders (default 0).
        min_confidence_score: Minimum entity name match confidence threshold (0.0 to 1.0, default 0.85).

    Returns:
        JSON with 'can_hire' boolean, 'risk_level' ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'),
        'risk_score' (0.0 to 100.0), specific 'flags', and the full underlying verification result.
    """
    return await licenseground_client.check_compliance_risk(
        state=state,
        entity_name=entity_name,
        license_number=license_number,
        trade=trade,
        require_workers_comp=require_workers_comp,
        require_surety_bond=require_surety_bond,
        max_disciplinary_actions=max_disciplinary_actions,
        min_confidence_score=min_confidence_score,
    )


@mcp.tool()
async def search_contractors(
    state: str,
    trade: str,
    city: Optional[str] = None,
    limit: int = 10,
) -> Dict[str, Any]:
    """
    Discover active, verified trade contractors by trade classification and location.

    Args:
        state: Two-letter US state code ('CA', 'FL', 'TX', 'NY', 'MA', 'IL', or 'AZ'). Required.
        trade: Trade category ('roofing', 'hvac', 'electrical', 'plumbing', 'general_contractor'). Required.
        city: Optional city to filter contractors by location.
        limit: Maximum number of contractors to return (1 to 50, default 10).

    Returns:
        JSON list of verified contractors with active licenses, phone numbers, and addresses.
    """
    return await licenseground_client.search_contractors(
        state=state,
        trade=trade,
        city=city,
        limit=limit,
    )


@mcp.tool()
async def check_federal_debarment(entity_name: str) -> Dict[str, Any]:
    """
    Check if a contractor is actively debarred or suspended on the federal SAM.gov Excluded Parties List System (EPLS).
    Crucial for public contracts, infrastructure, and enterprise B2B compliance.

    Args:
        entity_name: Official business or entity name to evaluate against federal sanctions.
    """
    return await licenseground_client.check_federal_debarment(entity_name=entity_name)


@mcp.tool()
async def audit_osha_safety(entity_name: str) -> Dict[str, Any]:
    """
    Audit contractor worksite safety history against the OSHA inspection and enforcement database.
    Evaluates willful safety violations, repeat fall protection citations, and cumulative penalties.

    Args:
        entity_name: Official business or entity name to evaluate.
    """
    return await licenseground_client.audit_osha_safety(entity_name=entity_name)


@mcp.tool()
async def get_registry_status() -> Dict[str, Any]:
    """
    Check the system health, cache performance statistics, and multi-state registry connectivity.

    Returns:
        JSON object with cache hit/miss counts, total records cached, and connector status for CA, FL, TX, NY, MA, IL, AZ.
    """
    return await licenseground_client.get_registry_status()


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
