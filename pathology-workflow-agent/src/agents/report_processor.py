"""Agent for processing pathology reports."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..config import settings
from ..schemas.models import PathologyReport, DiagnosisType
from pydantic import BaseModel, Field


class PathologyReportExtraction(BaseModel):
    """Structured extraction schema for pathology reports."""
    diagnosis: DiagnosisType = Field(description="The diagnosis type: benign, precancerous, cancerous, or inconclusive")
    findings: str = Field(description="Key clinical findings from the pathology report")
    recommendations: str | None = Field(default=None, description="Clinical recommendations for follow-up or treatment")


class ReportProcessorAgent:
    """Agent for processing and analyzing pathology reports."""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.1,
        )
        # Configure structured output
        self.structured_llm = self.llm.with_structured_output(PathologyReportExtraction)

    async def analyze_report(self, raw_text: str) -> PathologyReport:
        """Analyze raw pathology report text and extract structured information.

        Args:
            raw_text: Raw pathology report text

        Returns:
            Structured PathologyReport
        """
        system_prompt = """You are a medical AI assistant specialized in pathology report analysis.
        Extract key information from pathology reports including:
        - Diagnosis type (benign, precancerous, cancerous, inconclusive)
        - Key findings
        - Recommendations for follow-up

        Be precise and only extract information explicitly stated in the report."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Analyze this pathology report:\n\n{raw_text}"),
        ]

        # Use structured output with gpt-4o
        extracted: PathologyReportExtraction = await self.structured_llm.ainvoke(messages)

        return PathologyReport(
            report_id="temp_id",
            patient_id="temp_patient",
            pathologist_id="temp_pathologist",
            tissue_sample_id="temp_sample",
            diagnosis=extracted.diagnosis,
            findings=extracted.findings,
            recommendations=extracted.recommendations,
            raw_text=raw_text,
        )


report_processor = ReportProcessorAgent()
