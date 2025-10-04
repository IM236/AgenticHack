"""Agent for processing pathology reports."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..config import settings
from ..schemas.models import PathologyReport, DiagnosisType


class ReportProcessorAgent:
    """Agent for processing and analyzing pathology reports."""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.1,
        )

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

        # TODO: Implement structured output parsing
        response = await self.llm.ainvoke(messages)

        # Placeholder - parse LLM response into structured format
        diagnosis = self._extract_diagnosis(raw_text)

        return PathologyReport(
            report_id="temp_id",
            patient_id="temp_patient",
            pathologist_id="temp_pathologist",
            tissue_sample_id="temp_sample",
            diagnosis=diagnosis,
            findings=raw_text[:500],  # Truncate for demo
            raw_text=raw_text,
        )

    def _extract_diagnosis(self, text: str) -> DiagnosisType:
        """Extract diagnosis from text."""
        text_lower = text.lower()
        if "malignant" in text_lower or "cancer" in text_lower:
            return DiagnosisType.CANCEROUS
        elif "dysplasia" in text_lower or "precancerous" in text_lower:
            return DiagnosisType.PRECANCEROUS
        elif "benign" in text_lower:
            return DiagnosisType.BENIGN
        return DiagnosisType.INCONCLUSIVE


report_processor = ReportProcessorAgent()
