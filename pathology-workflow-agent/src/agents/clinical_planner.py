"""Agent for creating clinical plans based on pathology reports."""
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..config import settings
from ..schemas.models import ClinicalPlan, PathologyReport, DiagnosisType
from datetime import datetime
import uuid
from pydantic import BaseModel, Field


class ClinicalPlanExtraction(BaseModel):
    """Structured extraction schema for clinical plans."""
    treatment_plan: str = Field(description="Detailed treatment plan and clinical recommendations")
    follow_up_actions: List[str] = Field(description="List of specific follow-up actions required")
    urgency_level: str = Field(description="Urgency level: routine, moderate, or urgent")


class ClinicalPlannerAgent:
    """Agent for generating clinical plans and follow-up actions."""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.2,
        )
        # Configure structured output
        self.structured_llm = self.llm.with_structured_output(ClinicalPlanExtraction)

    async def create_clinical_plan(
        self, report: PathologyReport, clinician_id: str
    ) -> ClinicalPlan:
        """Generate clinical plan based on pathology report.

        Args:
            report: PathologyReport with diagnosis
            clinician_id: ID of the clinician

        Returns:
            ClinicalPlan with treatment recommendations and follow-up actions
        """
        system_prompt = """You are a clinical decision support AI assistant.
        Based on pathology reports, suggest appropriate clinical plans including:
        - Treatment recommendations
        - Follow-up procedures (e.g., colonoscopy, biopsy, imaging)
        - Timeline for follow-up
        - Urgency level assessment

        Follow evidence-based medical guidelines and standard of care."""

        user_prompt = f"""
        Pathology Report Analysis:
        - Diagnosis: {report.diagnosis.value}
        - Findings: {report.findings}
        - Recommendations: {report.recommendations or 'None'}

        Generate a clinical plan with specific follow-up actions.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        # Use structured output with gpt-4o
        extracted: ClinicalPlanExtraction = await self.structured_llm.ainvoke(messages)

        return ClinicalPlan(
            plan_id=str(uuid.uuid4()),
            report_id=report.report_id,
            patient_id=report.patient_id,
            clinician_id=clinician_id,
            diagnosis=report.diagnosis,
            treatment_plan=extracted.treatment_plan,
            follow_up_actions=extracted.follow_up_actions,
            urgency_level=extracted.urgency_level,
        )

    def _determine_follow_up_actions(
        self, report: PathologyReport
    ) -> List[str]:
        """Determine follow-up actions based on diagnosis."""
        actions = []

        if report.diagnosis == DiagnosisType.CANCEROUS:
            actions.extend([
                "Schedule urgent oncology consultation",
                "Order staging CT/MRI",
                "Schedule follow-up colonoscopy in 3 months",
                "Refer to surgical oncology",
                "Discuss treatment options with patient",
            ])
        elif report.diagnosis == DiagnosisType.PRECANCEROUS:
            actions.extend([
                "Schedule follow-up colonoscopy in 6 months",
                "Educate patient on lifestyle modifications",
                "Monitor for progression",
                "Consider referral to gastroenterology",
            ])
        elif report.diagnosis == DiagnosisType.BENIGN:
            actions.extend([
                "Routine follow-up in 1 year",
                "Continue regular screening schedule",
                "Patient education on preventive care",
            ])
        else:
            actions.append("Request additional testing for conclusive diagnosis")

        return actions

    def _assess_urgency(self, diagnosis: DiagnosisType) -> str:
        """Assess urgency level based on diagnosis."""
        if diagnosis == DiagnosisType.CANCEROUS:
            return "urgent"
        elif diagnosis == DiagnosisType.PRECANCEROUS:
            return "moderate"
        else:
            return "routine"


clinical_planner = ClinicalPlannerAgent()
