"""Main FastAPI application for Pathology Workflow Agent."""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from src.config import settings
from src.workflows.pathology_workflow import pathology_workflow

app = FastAPI(
    title=settings.app_name,
    description="Automated pathology workflow system with AI agents",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PathologyReportRequest(BaseModel):
    """Request model for submitting pathology reports."""
    patient_id: str
    raw_report_text: str
    report_id: str | None = None


class WorkflowResponse(BaseModel):
    """Response model for workflow execution."""
    workflow_id: str
    status: str
    message: str
    data: Dict[str, Any] | None = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.app_name,
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
    }


@app.post("/api/v1/reports/submit", response_model=WorkflowResponse)
async def submit_pathology_report(request: PathologyReportRequest):
    """Submit a pathology report for processing.

    This endpoint initiates the complete workflow:
    1. Extract structured data with PhenoML
    2. Process report with AI agent
    3. Upload to Epic EHR
    4. Notify clinician
    5. Generate clinical plan
    6. Communicate with patient
    7. Schedule follow-up
    """
    try:
        report_id = request.report_id or str(uuid.uuid4())

        # Run the complete workflow
        result = await pathology_workflow.run(
            report_id=report_id,
            patient_id=request.patient_id,
            raw_report_text=request.raw_report_text,
        )

        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])

        return WorkflowResponse(
            workflow_id=report_id,
            status="completed",
            message="Pathology report processed successfully",
            data={
                "report_id": report_id,
                "current_step": result.get("current_step"),
                "diagnosis": result.get("pathology_report", {}).get("diagnosis"),
                "epic_uploaded": result.get("epic_status", {}).get("status") == "uploaded",
                "clinician_notified": result.get("notification_sent", False),
                "patient_communicated": result.get("patient_communication") is not None,
                "follow_up_scheduled": result.get("follow_up_scheduled", False),
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/reports/{report_id}")
async def get_report_status(report_id: str):
    """Get status of a pathology report workflow.

    TODO: Implement state persistence and retrieval
    """
    return {
        "report_id": report_id,
        "status": "not_implemented",
        "message": "State persistence not yet implemented",
    }


@app.post("/api/v1/workflow/test")
async def test_workflow():
    """Test endpoint with sample pathology report."""
    sample_report = """
    PATHOLOGY REPORT

    Patient: Test Patient
    Specimen: Colon biopsy

    CLINICAL HISTORY: Screening colonoscopy

    GROSS DESCRIPTION:
    Received are multiple fragments of tan-pink tissue measuring 0.3 cm in aggregate.

    MICROSCOPIC DESCRIPTION:
    Sections show colonic mucosa with mild architectural distortion and focal
    high-grade dysplasia. No invasive carcinoma is identified.

    DIAGNOSIS:
    Colon, biopsy:
    - High-grade dysplasia (precancerous changes)
    - Recommend close follow-up and repeat colonoscopy in 3-6 months
    """

    result = await pathology_workflow.run(
        report_id=str(uuid.uuid4()),
        patient_id="test_patient_001",
        raw_report_text=sample_report,
    )

    return {
        "test_status": "completed",
        "workflow_result": result,
    }


def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
