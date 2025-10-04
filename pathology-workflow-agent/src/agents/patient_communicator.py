"""Agent for communicating with patients about pathology results."""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ..config import settings
from ..schemas.models import PatientCommunication, ClinicalPlan, PathologyReport
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class PatientMessageExtraction(BaseModel):
    """Structured extraction schema for patient communications."""
    message_content: str = Field(description="Patient-friendly message explaining results and next steps")


class PatientCommunicatorAgent:
    """Agent for generating patient-friendly communications."""

    def __init__(self):
        self.llm = ChatOpenAI(
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
        system_prompt = """You are a compassionate medical communication AI assistant.
        Generate clear, empathetic, and non-alarming messages for patients about their pathology results.

        Guidelines:
        - Use plain language, avoid medical jargon
        - Be empathetic and supportive
        - Clearly explain next steps
        - Encourage patients to contact their care team with questions
        - Balance transparency with appropriate reassurance
        - Never provide definitive medical advice - always defer to the clinician"""

        user_prompt = f"""
        Generate a patient communication for:

        Diagnosis: {report.diagnosis.value}
        Key Findings: {report.findings[:200]}...

        Next Steps:
        {chr(10).join(f"- {action}" for action in clinical_plan.follow_up_actions[:3])}

        Urgency: {clinical_plan.urgency_level}

        Create a {message_type} message that informs the patient while maintaining appropriate tone.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        # Use structured output with gpt-4o
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
