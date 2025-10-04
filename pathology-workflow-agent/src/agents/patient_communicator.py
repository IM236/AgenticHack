"""Agent for communicating with patients about pathology results."""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from ..config import settings
from ..schemas.models import PatientCommunication, ClinicalPlan, PathologyReport
from ..utils.gpt5_client import GPT5Client
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class PatientMessageExtraction(BaseModel):
    """Structured extraction schema for patient communications."""
    message_content: str = Field(description="Patient-friendly message explaining results and next steps")


class PatientCommunicatorAgent:
    """Agent for generating patient-friendly communications."""

    def __init__(self):
        self.llm = GPT5Client(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.3,
        )
        # Configure structured output
        self.structured_llm = self.llm.with_structured_output(PatientMessageExtraction)

    async def generate_patient_message(
        self,
        report: PathologyReport,
        clinical_plan: ClinicalPlan,
        message_type: str = "portal",
    ) -> PatientCommunication:
        """Generate patient-friendly communication about test results.

        Args:
            report: PathologyReport
            clinical_plan: ClinicalPlan with follow-up actions
            message_type: Type of communication (email, portal, phone)

        Returns:
            PatientCommunication with message content
        """
        system_prompt = """You are a medical communicator. Be brief, clear, and empathetic. Use plain language."""

        user_prompt = f"""Write brief patient message for {report.patient_name}'s colonoscopy:
- {report.num_polyps} polyp(s) found
- Diagnosis: {report.diagnosis.value}
- Next colonoscopy: {report.surveillance_recommendation}
- Urgency: {clinical_plan.urgency_level}

Keep message under 150 words. Explain results simply and reassure patient."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        # Use structured output with gpt-5
        extracted: PatientMessageExtraction = await self.structured_llm.ainvoke(messages)

        return PatientCommunication(
            communication_id=str(uuid.uuid4()),
            patient_id=report.patient_id,
            report_id=report.report_id,
            message_type=message_type,
            message_content=extracted.message_content,
            delivery_status="pending",
        )

    async def send_message(
        self, communication: PatientCommunication
    ) -> bool:
        """Send message to patient via specified channel.

        TODO: Implement actual message delivery via:
        - Patient portal API
        - Email service
        - SMS service
        """
        # Placeholder - implement actual delivery
        communication.sent_at = datetime.utcnow()
        communication.delivery_status = "sent"
        return True

    async def schedule_follow_up_call(
        self, patient_id: str, urgency: str
    ) -> Dict[str, Any]:
        """Schedule follow-up phone call with patient.

        TODO: Implement scheduling system integration
        """
        return {
            "scheduled": True,
            "appointment_time": None,
            "contact_method": "phone",
        }


patient_communicator = PatientCommunicatorAgent()
