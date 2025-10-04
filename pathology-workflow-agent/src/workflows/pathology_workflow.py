"""LangGraph workflow for pathology report processing."""
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from ..schemas.models import (
    WorkflowState,
    PathologyReport,
    EpicUploadStatus,
    ClinicalPlan,
    PatientCommunication,
)
from ..services.phenoml_service import phenoml_service
from ..services.epic_service import epic_service
from ..agents.report_processor import report_processor
from ..agents.clinical_planner import clinical_planner
from ..agents.patient_communicator import patient_communicator


class PathologyWorkflowState(TypedDict):
    """State for pathology workflow graph."""
    report_id: str
    patient_id: str
    raw_report_text: str
    pathology_report: Dict[str, Any] | None
    extracted_data: Dict[str, Any] | None
    epic_status: Dict[str, Any] | None
    notification_sent: bool
    clinical_plan: Dict[str, Any] | None
    patient_communication: Dict[str, Any] | None
    follow_up_scheduled: bool
    error: str | None
    current_step: str


class PathologyWorkflow:
    """LangGraph workflow for automated pathology report processing."""

    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the workflow graph."""
        workflow = StateGraph(PathologyWorkflowState)

        # Add nodes for each step
        workflow.add_node("extract_data", self._extract_with_phenoml)
        workflow.add_node("process_report", self._process_report)
        workflow.add_node("upload_to_epic", self._upload_to_epic)
        workflow.add_node("notify_clinician", self._notify_clinician)
        workflow.add_node("create_clinical_plan", self._create_clinical_plan)
        workflow.add_node("communicate_with_patient", self._communicate_with_patient)
        workflow.add_node("schedule_follow_up", self._schedule_follow_up)

        # Define workflow edges
        workflow.set_entry_point("extract_data")
        workflow.add_edge("extract_data", "process_report")
        workflow.add_edge("process_report", "upload_to_epic")
        workflow.add_edge("upload_to_epic", "notify_clinician")
        workflow.add_edge("notify_clinician", "create_clinical_plan")
        workflow.add_edge("create_clinical_plan", "communicate_with_patient")
        workflow.add_edge("communicate_with_patient", "schedule_follow_up")
        workflow.add_edge("schedule_follow_up", END)

        return workflow.compile()

    async def _extract_with_phenoml(
        self, state: PathologyWorkflowState
    ) -> PathologyWorkflowState:
        """Extract structured data using PhenoML."""
        try:
            raw_text = state["raw_report_text"]
            extracted_data = await phenoml_service.extract_structured_data(raw_text)

            state["extracted_data"] = extracted_data
            state["current_step"] = "data_extracted"
            return state

        except Exception as e:
            state["error"] = f"PhenoML extraction failed: {str(e)}"
            return state

    async def _process_report(
        self, state: PathologyWorkflowState
    ) -> PathologyWorkflowState:
        """Process report with AI agent."""
        try:
            raw_text = state["raw_report_text"]
            report = await report_processor.analyze_report(raw_text)

            # Enrich with PhenoML data
            if state.get("extracted_data"):
                report.extracted_data = state["extracted_data"]

            report.report_id = state["report_id"]
            report.patient_id = state["patient_id"]

            state["pathology_report"] = report.model_dump()
            state["current_step"] = "report_processed"
            return state

        except Exception as e:
            state["error"] = f"Report processing failed: {str(e)}"
            return state

    async def _upload_to_epic(
        self, state: PathologyWorkflowState
    ) -> PathologyWorkflowState:
        """Upload report to Epic EHR."""
        try:
            report_dict = state["pathology_report"]
            report = PathologyReport(**report_dict)

            epic_status = await epic_service.upload_pathology_report(report)

            state["epic_status"] = epic_status.model_dump()
            state["current_step"] = "uploaded_to_epic"
            return state

        except Exception as e:
            state["error"] = f"Epic upload failed: {str(e)}"
            return state

    async def _notify_clinician(
        self, state: PathologyWorkflowState
    ) -> PathologyWorkflowState:
        """Send notification to clinician."""
        try:
            report_dict = state["pathology_report"]
            clinician_id = "default_clinician"  # TODO: Extract from report or config

            success = await epic_service.send_notification(
                clinician_id=clinician_id,
                report_id=state["report_id"],
                message=f"New pathology report ready for review: {state['report_id']}",
            )

            state["notification_sent"] = success
            state["current_step"] = "clinician_notified"
            return state

        except Exception as e:
            state["error"] = f"Notification failed: {str(e)}"
            return state

    async def _create_clinical_plan(
        self, state: PathologyWorkflowState
    ) -> PathologyWorkflowState:
        """Create clinical plan using AI agent."""
        try:
            report_dict = state["pathology_report"]
            report = PathologyReport(**report_dict)
            clinician_id = "default_clinician"  # TODO: Extract from system

            plan = await clinical_planner.create_clinical_plan(report, clinician_id)

            state["clinical_plan"] = plan.model_dump()
            state["current_step"] = "plan_created"
            return state

        except Exception as e:
            state["error"] = f"Clinical plan creation failed: {str(e)}"
            return state

    async def _communicate_with_patient(
        self, state: PathologyWorkflowState
    ) -> PathologyWorkflowState:
        """Generate and send patient communication."""
        try:
            report_dict = state["pathology_report"]
            plan_dict = state["clinical_plan"]

            report = PathologyReport(**report_dict)
            plan = ClinicalPlan(**plan_dict)

            communication = await patient_communicator.generate_patient_message(
                report=report,
                clinical_plan=plan,
                message_type="portal",
            )

            # Send the message
            await patient_communicator.send_message(communication)

            state["patient_communication"] = communication.model_dump()
            state["current_step"] = "patient_communicated"
            return state

        except Exception as e:
            state["error"] = f"Patient communication failed: {str(e)}"
            return state

    async def _schedule_follow_up(
        self, state: PathologyWorkflowState
    ) -> PathologyWorkflowState:
        """Schedule follow-up appointments."""
        try:
            plan_dict = state["clinical_plan"]
            plan = ClinicalPlan(**plan_dict)

            # TODO: Implement actual scheduling system integration
            # For now, just mark as scheduled
            state["follow_up_scheduled"] = True
            state["current_step"] = "completed"
            return state

        except Exception as e:
            state["error"] = f"Follow-up scheduling failed: {str(e)}"
            return state

    async def run(
        self, report_id: str, patient_id: str, raw_report_text: str
    ) -> Dict[str, Any]:
        """Run the complete workflow.

        Args:
            report_id: Unique report identifier
            patient_id: Patient identifier
            raw_report_text: Raw pathology report text

        Returns:
            Final workflow state
        """
        initial_state: PathologyWorkflowState = {
            "report_id": report_id,
            "patient_id": patient_id,
            "raw_report_text": raw_report_text,
            "pathology_report": None,
            "extracted_data": None,
            "epic_status": None,
            "notification_sent": False,
            "clinical_plan": None,
            "patient_communication": None,
            "follow_up_scheduled": False,
            "error": None,
            "current_step": "initialized",
        }

        final_state = await self.graph.ainvoke(initial_state)
        return final_state


# Singleton workflow instance
pathology_workflow = PathologyWorkflow()
