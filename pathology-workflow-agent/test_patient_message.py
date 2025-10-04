#!/usr/bin/env python3
"""Test patient message generation with colonoscopy pathology data."""

import asyncio
import json
from src.schemas.models import PathologyReport, ClinicalPlan, DiagnosisType
from src.agents.patient_communicator import patient_communicator


async def test_patient_message():
    """Test generating patient message from colonoscopy report."""

    # Load a sample report
    with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
        reports_data = json.load(f)

    # Use first report
    report_data = reports_data[0]

    # Create PathologyReport from JSON
    report = PathologyReport(**report_data)

    print("="*80)
    print("Testing Patient Message Generation")
    print("="*80)
    print()

    print(f"Patient: {report.patient_name}")
    print(f"Procedure Date: {report.procedure_date}")
    print(f"Diagnosis: {report.diagnosis.value}")
    print(f"Findings: {report.findings}")
    print(f"Surveillance: {report.surveillance_recommendation}")
    print()

    # Create a mock clinical plan
    clinical_plan = ClinicalPlan(
        plan_id="test-plan-001",
        report_id=report.id,
        patient_id=report.patient_id,
        clinician_id="dr-smith-001",
        diagnosis=report.diagnosis,
        treatment_plan=f"Surveillance colonoscopy in {report.surveillance_recommendation}",
        follow_up_actions=[
            f"Schedule follow-up colonoscopy in {report.surveillance_recommendation}",
            "Continue routine health screenings",
            "Contact your doctor if you experience any symptoms"
        ],
        urgency_level="routine" if report.diagnosis == DiagnosisType.BENIGN else "urgent"
    )

    print("Generating patient message...")
    print()

    # Generate patient message
    communication = await patient_communicator.generate_patient_message(
        report=report,
        clinical_plan=clinical_plan,
        message_type="portal"
    )

    print("="*80)
    print("PATIENT MESSAGE:")
    print("="*80)
    print()
    print(communication.message_content)
    print()
    print("="*80)
    print(f"Message Type: {communication.message_type}")
    print(f"Delivery Status: {communication.delivery_status}")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(test_patient_message())
