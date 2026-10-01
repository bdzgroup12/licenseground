import os
import httpx
from typing import Optional, Dict, Any

API_BASE_URL = os.environ.get("LICENSEGROUND_API_BASE", "https://licenseground.com").rstrip("/")
DEFAULT_TIMEOUT = float(os.environ.get("LICENSEGROUND_TIMEOUT", "15.0"))


class LicenseGroundClient:
    """Official asynchronous client for LicenseGround Cloud Verification APIs."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LICENSEGROUND_API_KEY") or os.environ.get("X_AGENT_API_KEY") or ""

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "LicenseGround-MCP-Client/1.0.0",
        }
        if self.api_key:
            headers["X-Agent-API-Key"] = self.api_key
        return headers

    async def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE_URL}{endpoint}"
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            try:
                response = await client.post(url, headers=self._headers(), json=payload)
            except httpx.RequestError as exc:
                return {
                    "error": "Connection Failed",
                    "message": f"Could not connect to LicenseGround Cloud API at {url}: {exc}",
                }

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 402:
                detail = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                return {
                    "error": "Payment Required",
                    "status_code": 402,
                    "message": detail.get("message", "API key balance depleted or key missing."),
                    "upgrade_url": "https://licenseground.com/#pricing",
                    "get_free_key": "https://licenseground.com/#get-key",
                }
            elif response.status_code == 404:
                return {"error": "Not Found", "status_code": 404, "message": "Resource not found."}
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "status_code": response.status_code,
                    "detail": response.text,
                }

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{API_BASE_URL}{endpoint}"
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            try:
                response = await client.get(url, headers=self._headers(), params=params)
            except httpx.RequestError as exc:
                return {
                    "error": "Connection Failed",
                    "message": f"Could not connect to LicenseGround Cloud API at {url}: {exc}",
                }

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 402:
                return {
                    "error": "Payment Required",
                    "status_code": 402,
                    "message": "API key balance depleted or key missing.",
                    "upgrade_url": "https://licenseground.com/#pricing",
                    "get_free_key": "https://licenseground.com/#get-key",
                }
            else:
                return {
                    "error": f"HTTP {response.status_code}",
                    "status_code": response.status_code,
                    "detail": response.text,
                }

    async def verify_license(
        self,
        state: str,
        entity_name: Optional[str] = None,
        license_number: Optional[str] = None,
        trade: str = "any",
        city: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload = {
            "state": state.upper(),
            "entity_name": entity_name,
            "license_number": license_number,
            "trade": trade.lower(),
            "city": city,
        }
        return await self._post("/v1/verify", payload)

    async def check_compliance_risk(
        self,
        state: str,
        entity_name: Optional[str] = None,
        license_number: Optional[str] = None,
        trade: str = "any",
        require_workers_comp: bool = True,
        require_surety_bond: bool = True,
        max_disciplinary_actions: int = 0,
        min_confidence_score: float = 0.85,
    ) -> Dict[str, Any]:
        payload = {
            "state": state.upper(),
            "entity_name": entity_name,
            "license_number": license_number,
            "trade": trade.lower(),
            "require_workers_comp": require_workers_comp,
            "require_surety_bond": require_surety_bond,
            "max_disciplinary_actions": max_disciplinary_actions,
            "min_confidence_score": min_confidence_score,
        }
        return await self._post("/v1/compliance-check", payload)

    async def search_contractors(
        self,
        state: str,
        trade: str,
        city: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        payload = {
            "state": state.upper(),
            "trade": trade.lower(),
            "city": city,
            "limit": limit,
        }
        return await self._post("/v1/search", payload)

    async def check_federal_debarment(self, entity_name: str) -> Dict[str, Any]:
        return await self._post("/v1/federal/debarment-check", {"entity_name": entity_name})

    async def audit_osha_safety(self, entity_name: str) -> Dict[str, Any]:
        return await self._post("/v1/safety/osha-audit", {"entity_name": entity_name})

    async def get_registry_status(self) -> Dict[str, Any]:
        return await self._get("/v1/health")


licenseground_client = LicenseGroundClient()
