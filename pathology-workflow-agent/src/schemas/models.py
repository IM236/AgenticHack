"""Data models for pathology workflow."""
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from pydantic import BaseModel, Field


class DiagnosisType(str, Enum):
    """Pathology diagnosis types."""
    BENIGN = "benign"
    PRECANCEROUS = "precancerous"
    CANCEROUS = "cancerous"
    INCONCLUSIVE = "inconclusive"


class PolypFinding(BaseModel):
    """Individual polyp finding from colonoscopy."""
    number: int
    type: str  # tubular adenoma, villous adenoma, hyperplastic, etc.
    location: str  # colon segment
    size_mm: int
    dysplasia: str  # no dysplasia, low-grade, high-grade
    removal_method: str


class PathologyReport(BaseModel):
    """Colonoscopy pathology report model from PhenoML/Medplum."""
    id: str
    patient_id: str
    patient_name: str
    accession_number: str
    procedure_date: str  # YYYY-MM-DD format
    procedure_type: str
    indication: str  # screening, surveillance, diagnostic
    physician: str
    specimen_type: str
    clinical_history: str
    cecal_intubation: bool
    prep_quality: str
    num_polyps: int
    polyps: List[PolypFinding]
    report_date: str
    pathologist: str
    surveillance_recommendation: str

    # Legacy compatibility fields
    @property
    def report_id(self) -> str:
        return self.id

    @property
    def findings(self) -> str:
        """Generate findings summary from polyps."""
        findings = []
        for polyp in self.polyps:
            findings.append(
                f"Polyp {polyp.number}: {polyp.type} in {polyp.location}, "
                f"{polyp.size_mm}mm, {polyp.dysplasia}"
            )
        return "; ".join(findings)

    @property
    def diagnosis(self) -> DiagnosisType:
        """Determine diagnosis from polyp findings."""
        # Check for high-grade dysplasia or advanced adenomas
        for polyp in self.polyps:
            if "high-grade" in polyp.dysplasia.lower():
                return DiagnosisType.PRECANCEROUS
            if polyp.size_mm >= 10 and "adenoma" in polyp.type.lower():
                return DiagnosisType.PRECANCEROUS

        # Check for any adenomas
        if any("adenoma" in p.type.lower() for p in self.polyps):
            return DiagnosisType.PRECANCEROUS

        # Otherwise benign
        return DiagnosisType.BENIGN

    @property
    def recommendations(self) -> str:
        return f"Surveillance colonoscopy recommended in {self.surveillance_recommendation}"


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
