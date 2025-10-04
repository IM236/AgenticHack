#!/usr/bin/env python3
"""Integration tests for pathology workflow agents with GPT-5."""

import asyncio
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.schemas.models import PathologyReport, ClinicalPlan
from src.agents.clinical_planner import clinical_planner
from src.agents.patient_communicator import patient_communicator
from src.services.phenoml_service import phenoml_service


async def test_phenoml_query():
    """Test querying pathology data from PhenoML/Medplum."""
    print("\n" + "="*80)
    print("TEST 1: PhenoML Data Query")
    print("="*80 + "\n")

    # Query for patients
    print("Querying for patients with colonoscopy...")
    try:
        patients = phenoml_service.query_patients("Find patients named Jessica Jones")
        print(f"✓ Found {len(patients)} patient(s)")
        if patients:
            print(f"  Sample: {patients[0].get('name', 'Unknown')}")
    except Exception as e:
        print(f"✗ Query failed: {e}")
        return False

    return True


async def test_clinical_planner():
    """Test clinical planner agent with GPT-5."""
    print("\n" + "="*80)
    print("TEST 2: Clinical Planner Agent (GPT-5)")
    print("="*80 + "\n")

    # Load sample report
    with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
        reports_data = json.load(f)

    report_data = reports_data[0]  # Jessica Jones
    report = PathologyReport(**report_data)

    print(f"Patient: {report.patient_name}")
    print(f"Diagnosis: {report.diagnosis.value}")
    print(f"Findings: {report.findings[:100]}...")
    print()

    print("Generating clinical plan with GPT-5...")
    try:
        clinical_plan = await clinical_planner.create_clinical_plan(
            report=report,
            clinician_id="dr-test-001"
        )

        print(f"✓ Clinical plan created successfully")
        print(f"\nTreatment Plan:")
        print(f"  {clinical_plan.treatment_plan}")
        print(f"\nFollow-up Actions:")
        for i, action in enumerate(clinical_plan.follow_up_actions, 1):
            print(f"  {i}. {action}")
        print(f"\nUrgency: {clinical_plan.urgency_level}")

        return True
    except Exception as e:
        print(f"✗ Clinical planner failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_patient_communicator():
    """Test patient communicator agent with GPT-5."""
    print("\n" + "="*80)
    print("TEST 3: Patient Communicator Agent (GPT-5)")
    print("="*80 + "\n")

    # Load sample report
    with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
        reports_data = json.load(f)

    report_data = reports_data[1]  # Susan Moore - high-grade dysplasia
    report = PathologyReport(**report_data)

    print(f"Patient: {report.patient_name}")
    print(f"Diagnosis: {report.diagnosis.value}")
    print(f"Findings: {report.findings[:100]}...")
    print()

    # Create clinical plan first
    print("Creating clinical plan...")
    clinical_plan = await clinical_planner.create_clinical_plan(
        report=report,
        clinician_id="dr-test-001"
    )
    print(f"✓ Clinical plan created (urgency: {clinical_plan.urgency_level})")
    print()

    print("Generating patient message with GPT-5...")
    try:
        communication = await patient_communicator.generate_patient_message(
            report=report,
            clinical_plan=clinical_plan,
            message_type="portal"
        )

        print(f"✓ Patient message generated successfully")
        print(f"\n{'-'*80}")
        print("PATIENT MESSAGE:")
        print(f"{'-'*80}")
        print(communication.message_content)
        print(f"{'-'*80}")

        return True
    except Exception as e:
        print(f"✗ Patient communicator failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_full_workflow():
    """Test complete workflow: Query → Clinical Plan → Patient Message."""
    print("\n" + "="*80)
    print("TEST 4: Full Workflow Integration")
    print("="*80 + "\n")

    # Load multiple reports
    with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
        reports_data = json.load(f)

    results = []

    for i, report_data in enumerate(reports_data[:2], 1):  # Test first 2
        print(f"\n--- Processing Report {i}: {report_data['patient_name']} ---\n")

        # Create report
        report = PathologyReport(**report_data)

        # Generate clinical plan
        clinical_plan = await clinical_planner.create_clinical_plan(
            report=report,
            clinician_id="dr-workflow-001"
        )
        print(f"✓ Clinical plan: {clinical_plan.urgency_level} urgency")

        # Generate patient message
        communication = await patient_communicator.generate_patient_message(
            report=report,
            clinical_plan=clinical_plan,
            message_type="portal"
        )
        print(f"✓ Patient message: {len(communication.message_content)} chars")

        results.append({
            "patient": report.patient_name,
            "diagnosis": report.diagnosis.value,
            "urgency": clinical_plan.urgency_level,
            "message_length": len(communication.message_content)
        })

    print(f"\n{'='*80}")
    print("WORKFLOW SUMMARY:")
    print(f"{'='*80}")
    for result in results:
        print(f"\n{result['patient']}:")
        print(f"  Diagnosis: {result['diagnosis']}")
        print(f"  Urgency: {result['urgency']}")
        print(f"  Message: {result['message_length']} characters")

    return True


async def main():
    """Run all integration tests."""
    print("\n" + "="*80)
    print("PATHOLOGY WORKFLOW INTEGRATION TESTS (GPT-5)")
    print("="*80)

    results = []

    # Test 1: PhenoML Query
    try:
        result = await test_phenoml_query()
        results.append(("PhenoML Query", result))
    except Exception as e:
        print(f"Test failed with error: {e}")
        results.append(("PhenoML Query", False))

    # Test 2: Clinical Planner
    try:
        result = await test_clinical_planner()
        results.append(("Clinical Planner", result))
    except Exception as e:
        print(f"Test failed with error: {e}")
        results.append(("Clinical Planner", False))

    # Test 3: Patient Communicator
    try:
        result = await test_patient_communicator()
        results.append(("Patient Communicator", result))
    except Exception as e:
        print(f"Test failed with error: {e}")
        results.append(("Patient Communicator", False))

    # Test 4: Full Workflow
    try:
        result = await test_full_workflow()
        results.append(("Full Workflow", result))
    except Exception as e:
        print(f"Test failed with error: {e}")
        results.append(("Full Workflow", False))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n{passed}/{total} tests passed")
    print("="*80 + "\n")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
