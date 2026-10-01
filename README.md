<p align="center">
  <img src="assets/logo.png" width="180" alt="LicenseGround Logo" style="border-radius: 16px;">
</p>

# LicenseGround MCP Server

[![smithery badge](https://smithery.ai/badge/licenseground)](https://smithery.ai/server/licenseground)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Transport](https://img.shields.io/badge/MCP%20Transport-Streamable%20HTTP%20%7C%20Stdio-success.svg)](https://licenseground.com/mcp)

Official [Model Context Protocol (MCP)](https://modelcontextprotocol.io) client connector for **[LicenseGround](https://licenseground.com)**: providing AI agents, autonomous procurement systems, and invoice dispatchers with **real-time, machine-readable regulatory ground truth** for US trade contractors.

---

## ⚡️ Quickstart: Connect to the Cloud Server (Zero Install)

You do not need to install Python or maintain local packages to use LicenseGround. Connect directly to our high-availability cloud endpoint:

### 1. Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "licenseground": {
      "url": "https://licenseground.com/mcp",
      "headers": {
        "X-Agent-API-Key": "YOUR_LICENSEGROUND_API_KEY"
      }
    }
  }
}
```

*Config file locations:*
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### 2. Cursor / Windsurf / Claude Code

Add a new MCP server in your IDE settings:
* **Name:** `licenseground`
* **Type:** `Streamable HTTP` (or `SSE`)
* **Endpoint URL:** `https://licenseground.com/mcp`
* **Custom Headers:** `X-Agent-API-Key: YOUR_LICENSEGROUND_API_KEY`

### 3. Smithery CLI

Install directly via [Smithery](https://smithery.ai/server/licenseground):

```bash
npx -y @smithery/cli install licenseground --client claude
```

---

## 🛠️ Available MCP Tools

| Tool | Description |
| :--- | :--- |
| `verify_license` | Direct regulatory inquiry against official licensing boards (**California CSLB**, **Florida DBPR**, **Texas TDLR**, **New York DOB**, **Massachusetts CSL**, **Illinois Chicago DOB**, **Arizona ROC**). Returns license status, expiration, classifications, disciplinary flags, and workers' comp insurance. |
| `check_compliance_risk` | Comprehensive composite risk evaluation for autonomous onboarding or accounts payable. Audits license standing, workers' comp coverage, surety bonds, OSHA citations, and SAM.gov debarment to output a deterministic `can_hire` score and flags. |
| `search_contractors` | Discover active, verified trade contractors by trade classification, state, and geographic proximity across supported jurisdictions. |
| `check_federal_debarment` | Checks the Federal **SAM.gov** System for Award Management exclusion list for debarred entities, active exclusions, and SAM unique entity identifiers. |
| `audit_osha_safety` | Inspects official OSHA safety records for active investigations, standard violations, serious citations, and penalty history. |
| `get_registry_status` | Returns system latency, cache hit statistics, and board scraping health metrics across all supported jurisdictions. |

---

## 💻 Local Stdio Connector

If your agent runtime requires a local `stdio` subprocess:

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/bdzgroup12/licenseground.git
cd licenseground
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` or export your API key:

```bash
export LICENSEGROUND_API_KEY="your_licenseground_api_key"
```

*(Get your API key at [licenseground.com](https://licenseground.com))*

### 3. Run via Stdio

```bash
python -m src.server
```

### 4. Claude Desktop Stdio Config

```json
{
  "mcpServers": {
    "licenseground": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/licenseground",
      "env": {
        "LICENSEGROUND_API_KEY": "your_licenseground_api_key"
      }
    }
  }
}
```

---

## 🐳 Docker

Run with Docker:

```bash
docker build -t licenseground-mcp .
docker run -i --rm -e LICENSEGROUND_API_KEY="your_api_key" licenseground-mcp
```

---

## 📄 License

This client package is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌐 Links

* **Official Website:** [licenseground.com](https://licenseground.com)
* **Get API Key & Pricing:** [licenseground.com/#pricing](https://licenseground.com/#pricing)
* **MCP Streamable HTTP Endpoint:** `https://licenseground.com/mcp`
