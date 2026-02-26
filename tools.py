import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from crewai.tools import tool

search_tool = SerperDevTool()

@tool("Financial Document Reader")
def read_data_tool(path: str = 'data/sample.pdf') -> str:
    """Read and extract text from a PDF financial document.

    Args:
        path: Path to the PDF file. Defaults to 'data/sample.pdf'.

    Returns:
        Full extracted text of the financial document.
    """
    from langchain_community.document_loaders import PDFMinerLoader

    docs = PDFMinerLoader(file_path=path).load()

    full_report = ""
    for data in docs:
        content = data.page_content
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
        full_report += content + "\n"

    return full_report


class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        processed_data = financial_document_data
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
        return "Investment analysis functionality to be implemented"


class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):
        return "Risk assessment functionality to be implemented"
