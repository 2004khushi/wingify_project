from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_data_tool

analyze_financial_document = Task(
    description=(
        "Analyze the uploaded financial document to answer the user's query: {query}\n"
        "Steps:\n"
        "1. Use the read_data_tool to load the financial document from path: {file_path}\n"
        "2. Identify key financial metrics: revenue, net income, EPS, margins, debt ratios.\n"
        "3. Compare year-over-year and quarter-over-quarter trends where data is available.\n"
        "4. Provide a structured, evidence-based answer to the query.\n"
        "5. Use the search tool only to verify publicly known market context if needed."
    ),
    expected_output=(
        "A structured financial analysis report containing:\n"
        "- Executive summary answering the user's query\n"
        "- Key financial metrics extracted from the document\n"
        "- Year-over-year / quarter-over-quarter trend analysis\n"
        "- Relevant market context (sourced and cited)\n"
        "- Clear disclaimers where data is insufficient"
    ),
    agent=financial_analyst,
    tools=[read_data_tool],
    async_execution=False,
)

investment_analysis = Task(
    description=(
        "Based on the financial document analysis, provide investment recommendations "
        "for the user's query: {query}\n"
        "Steps:\n"
        "1. Review the financial analysis output from the previous task.\n"
        "2. Assess valuation using applicable metrics (P/E, P/B, EV/EBITDA, DCF where possible).\n"
        "3. Identify catalysts and headwinds supported by the document data.\n"
        "4. Provide a clear buy/hold/sell rationale with supporting evidence.\n"
        "5. Include a standard investment disclaimer."
    ),
    expected_output=(
        "A professional investment recommendation including:\n"
        "- Valuation summary with supporting metrics\n"
        "- Key investment thesis (bull and bear case)\n"
        "- Specific, evidence-based recommendation with rationale\n"
        "- Risk factors that could affect the recommendation\n"
        "- Standard disclaimer: 'This is not personalised financial advice.'"
    ),
    agent=investment_advisor,
    tools=[read_data_tool],
    async_execution=False,
)

risk_assessment = Task(
    description=(
        "Perform a risk assessment based on the financial document and user query: {query}\n"
        "Steps:\n"
        "1. Identify market, credit, liquidity, and operational risks from the document.\n"
        "2. Quantify each risk where data allows (e.g., debt-to-equity, current ratio, beta).\n"
        "3. Assess the company's risk mitigation strategies if disclosed.\n"
        "4. Provide an overall risk rating (Low / Medium / High) with justification."
    ),
    expected_output=(
        "A structured risk assessment report including:\n"
        "- Risk category breakdown (market / credit / liquidity / operational)\n"
        "- Quantified risk metrics extracted from the document\n"
        "- Overall risk rating with clear justification\n"
        "- Recommended risk mitigation considerations"
    ),
    agent=risk_assessor,
    tools=[read_data_tool],
    async_execution=False,
)

verification = Task(
    description=(
        "Verify that the uploaded file is a genuine financial document before analysis.\n"
        "Steps:\n"
        "1. Use read_data_tool to load the file from path: {file_path}\n"
        "2. Check for the presence of standard financial statement indicators "
        "(e.g., balance sheet, income statement, cash flow, auditor notes).\n"
        "3. Return a clear PASS or FAIL verdict with reasoning.\n"
        "4. If FAIL, describe what type of document it appears to be instead."
    ),
    expected_output=(
        "A verification report with:\n"
        "- PASS or FAIL verdict\n"
        "- List of financial indicators found (or not found)\n"
        "- Document type classification\n"
        "- Confidence level (High / Medium / Low) with reasoning"
    ),
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False
)
