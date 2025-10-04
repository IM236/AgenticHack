"""Data models for pathology workflow."""
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class DiagnosisType(str, Enum):
    """Pathology diagnosis types."""
    BENIGN = "benign"
    PRECANCEROUS = "precancerous"
    CANCEROUS = "cancerous"
    INCONCLUSIVE = "inconclusive"


class PathologyReport(BaseModel):
    """Pathology report model."""
    report_id: str
    patient_id: str
    pathologist_id: str
    tissue_sample_id: str
    diagnosis: DiagnosisType
    findings: str
    recommendations: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    raw_text: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None


class EpicUploadStatus(BaseModel):
    """Epic upload status model."""
    report_id: str
    epic_document_id: Optional[str] = None
    status: str  # uploaded, failed, pending
    uploaded_at: Optional[datetime] = None
    error_message: Optional[str] = None


class ClinicalPlan(BaseModel):
    """Clinical plan model."""
    plan_id: str
    report_id: str
    patient_id: str
    clinician_id: str
    diagnosis: DiagnosisType
    treatment_plan: str
    follow_up_actions: list[str]
    urgency_level: str  # routine, urgent, emergency
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PatientCommunication(BaseModel):
    """Patient communication model."""
    communication_id: str
    patient_id: str
    report_id: str
    message_type: str  # email, portal, phone
    message_content: str
    sent_at: Optional[datetime] = None
    delivery_status: str  # sent, delivered, failed


class WorkflowState(BaseModel):
    """LangGraph workflow state."""
    report_id: str
    patient_id: str
    pathology_report: Optional[PathologyReport] = None
    epic_status: Optional[EpicUploadStatus] = None
    notification_sent: bool = False
    clinical_plan: Optional[ClinicalPlan] = None
    patient_notified: bool = False
    follow_up_scheduled: bool = False
    error: Optional[str] = None
    current_step: str = "initialized"
