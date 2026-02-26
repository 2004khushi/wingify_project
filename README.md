# Financial Document Analyzer

A production-ready financial document analysis system built with CrewAI, FastAPI, and GPT-4o-mini. Upload any financial PDF (annual reports, quarterly updates, balance sheets) and receive structured AI-powered analysis, investment recommendations, and risk assessments.

---

## Bugs Found and Fixed

### `tools.py`

| # | Bug | Fix |
|---|-----|-----|
| 1 | `from crewai_tools import tools` — invalid import, `tools` does not exist at top level | Replaced with `from crewai_tools import SerperDevTool` |
| 2 | `SerperDevTool` imported from internal submodule path (fragile) | Import directly from `crewai_tools` |
| 3 | `read_data_tool` was `async` — crewai does not await tool calls | Removed `async` keyword |
| 4 | `read_data_tool` was a bare static method, not a `BaseTool` instance — pydantic validation fails when passed to `Agent(tools=[...])` | Replaced class with `@tool` decorator from `crewai.tools`, which wraps the function into a proper `BaseTool` |
| 5 | `Pdf(file_path=path)` — `Pdf` class never imported and does not exist | Replaced with `PDFMinerLoader` from `langchain_community` |
| 6 | `InvestmentTool` and `RiskTool` methods were `async` | Removed `async` |
| 7 | Both tool class methods missing `self` / not decorated as `@staticmethod` | Added `@staticmethod` |

### `agents.py`

| # | Bug | Fix |
|---|-----|-----|
| 1 | `from crewai.agents import Agent` — wrong submodule path | `from crewai import Agent` |
| 2 | `llm = llm` — self-referential NameError | Replaced with `LLM(model="gpt-4o-mini")` |
| 3 | `financial_analyst` goal instructed agent to fabricate investment advice | Rewritten to instruct honest, document-grounded analysis |
| 4 | `financial_analyst` backstory instructed hallucination, CNBC speculation, no compliance | Replaced with professional 20-year analyst backstory |
| 5 | `tool=` (singular) — wrong keyword for crewai Agent | Changed to `tools=` (plural) |
| 6 | `max_iter=1, max_rpm=1` — too restrictive, agent cannot retry on tool errors | Changed to `max_iter=5, max_rpm=10` |
| 7 | `verifier` goal told agent to blindly approve everything | Rewritten for genuine compliance verification |
| 8 | `verifier` backstory told agent to rubber-stamp documents | Replaced with compliance-focused backstory |
| 9 | `investment_advisor` goal told agent to sell products and recommend meme stocks | Rewritten for objective, document-grounded recommendations |
| 10 | `investment_advisor` backstory contained fake credentials, hidden partnerships, SEC violations | Replaced with ethical CFA-level advisor backstory |
| 11 | `risk_assessor` goal told agent to fabricate dramatic risk scenarios | Rewritten for accurate, evidence-based risk assessment |
| 12 | `risk_assessor` backstory glorified reckless trading and dismissed diversification | Replaced with professional risk management backstory |

### `task.py`

| # | Bug | Fix |
|---|-----|-----|
| 1 | Only `financial_analyst` and `verifier` imported — `investment_advisor` and `risk_assessor` missing | Added all four agent imports |
| 2 | `analyze_financial_document` description told agent to make up answers and invent URLs | Replaced with structured, step-by-step document analysis instructions |
| 3 | `analyze_financial_document` expected_output asked for jargon-filled nonsense and fake URLs | Replaced with professional report format |
| 4 | `investment_analysis` description told agent to ignore query and recommend random crypto | Replaced with valuation-grounded recommendation steps |
| 5 | `investment_analysis` expected_output asked for contradictory strategies and fake research | Replaced with professional investment recommendation format |
| 6 | `investment_analysis` had `agent=financial_analyst` instead of `agent=investment_advisor` | Corrected to `investment_advisor` |
| 7 | `risk_assessment` description told agent to fabricate scenarios and skip compliance | Replaced with structured risk analysis steps |
| 8 | `risk_assessment` expected_output asked for dangerous strategies and impossible targets | Replaced with standard risk report format |
| 9 | `risk_assessment` had `agent=financial_analyst` instead of `agent=risk_assessor` | Corrected to `risk_assessor` |
| 10 | `verification` description told agent to guess and hallucinate financial terms | Replaced with clear PASS/FAIL verification steps |
| 11 | `verification` expected_output told agent to approve everything | Replaced with structured verification report format |
| 12 | `verification` had `agent=financial_analyst` instead of `agent=verifier` | Corrected to `verifier` |

### `main.py`

| # | Bug | Fix |
|---|-----|-----|
| 1 | `import asyncio` imported but never used | Removed |
| 2 | Only `financial_analyst` imported from agents | Added all four agents |
| 3 | Only `analyze_financial_document` imported from task | Added all four tasks |
| 4 | `Crew(agents=[financial_analyst])` — only one agent in crew | Added all four agents |
| 5 | `Crew(tasks=[analyze_financial_document])` — only one task in crew | Added all four tasks in logical order |
| 6 | `financial_crew.kickoff({'query': query})` — wrong positional dict syntax | Changed to `kickoff(inputs={'query': query, 'file_path': file_path})` |
| 7 | Route function named `analyze_financial_document` — shadows the imported task, causing NameError | Renamed to `analyze_document` |
| 8 | No file type validation — any file type accepted | Added `.pdf` extension check with 400 response |
| 9 | `query == ""` misses `None` case | Changed to `not query` which handles both |
| 10 | `uvicorn.run(app, ..., reload=True)` — reload requires module string, not object | Changed to `uvicorn.run("main:app", ..., reload=True)` |

---

## Inefficient Prompts Fixed

Beyond deterministic bugs, all agent goals, backstories, task descriptions, and expected outputs were completely rewritten:

- **Goals** were replaced from instructions to hallucinate → structured, query-grounded objectives
- **Backstories** were replaced from reckless/dishonest personas → professional, compliance-aware experts  
- **Task descriptions** were replaced from vague/harmful instructions → clear numbered steps
- **Expected outputs** were replaced from nonsensical formats → professional report structures

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- OpenAI API key (get one at https://platform.openai.com/api-keys)
- Serper API key for web search (get one at https://serper.dev) — optional

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd financial-document-analyzer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### Add Sample Document

```bash
mkdir data
# Option 1: Download Tesla Q2 2025 report
curl -o data/sample.pdf https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf

# Option 2: Upload any financial PDF via the API endpoint
```

### Run the Server

```bash
python main.py
# OR
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server starts at: `http://localhost:8000`

---

## API Documentation

### `GET /`
Health check endpoint.

**Response:**
```json
{"message": "Financial Document Analyzer API is running"}
```

---

### `POST /analyze`
Upload a financial PDF and receive comprehensive AI analysis.

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | PDF file | Yes | Financial document to analyze |
| `query` | string | No | Specific question to answer (default: general analysis) |

**Example (curl):**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@data/sample.pdf;type=application/pdf" \
  -F "query=What was the revenue growth and is this a good investment?"
```

**Example (Python):**
```python
import requests

with open("data/sample.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/analyze",
        files={"file": ("sample.pdf", f, "application/pdf")},
        data={"query": "What are the key financial risks?"}
    )
print(response.json())
```

**Success Response (200):**
```json
{
  "status": "success",
  "query": "What was the revenue growth?",
  "analysis": "... full crew analysis output ...",
  "file_processed": "sample.pdf"
}
```

**Error Responses:**

| Code | Reason |
|------|--------|
| 400 | Non-PDF file uploaded |
| 500 | Internal error during analysis |

**Interactive docs:** Visit `http://localhost:8000/docs` for Swagger UI.

---

## How It Works

The system runs a sequential 4-agent CrewAI pipeline on every request:

```
Upload PDF
    ↓
1. Verifier Agent       — Confirms the document is a genuine financial report (PASS/FAIL)
    ↓
2. Financial Analyst    — Extracts key metrics, trends, and answers the user query
    ↓
3. Investment Advisor   — Provides buy/hold/sell recommendations with valuation analysis
    ↓
4. Risk Assessor        — Identifies and rates market, credit, liquidity, and operational risks
    ↓
Combined Report Returned
```

---

## Project Structure

```
financial-document-analyzer/
├── agents.py          # Agent definitions (roles, goals, backstories, LLM config)
├── task.py            # Task definitions (descriptions, expected outputs, agent assignments)
├── tools.py           # PDF reader tool and search tool
├── main.py            # FastAPI app, routes, crew orchestration
├── requirements.txt   # All dependencies
├── .env               # API keys (not committed to git)
├── .gitignore         # Excludes .env, data/, __pycache__
└── data/              # Uploaded PDFs stored temporarily during processing
```

---

## Requirements

```
crewai==0.130.0
crewai-tools==0.47.1
fastapi==0.110.3
python-multipart>=0.0.22
uvicorn
pdfminer.six>=20221105
langchain-community>=0.3.1
python-dotenv>=1.0.0
```

Full list in `requirements.txt`.
