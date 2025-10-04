#!/usr/bin/env python3
"""Test individual endpoints separately with timeouts."""

import asyncio
import json
import sys
import os
import time
from dotenv import load_dotenv

# Load .env file BEFORE importing anything else
load_dotenv('.env')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.schemas.models import PathologyReport, ClinicalPlan
from src.agents.clinical_planner import clinical_planner
from src.agents.patient_communicator import patient_communicator
from src.services.phenoml_service import phenoml_service


async def test_load_report():
    """Test 1: Load pathology report from JSON."""
    print("\n" + "="*80)
    print("TEST 1: Load Pathology Report from JSON")
    print("="*80)

    start = time.time()
    try:
        with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
            reports_data = json.load(f)

        report_data = reports_data[0]
        report = PathologyReport(**report_data)

        elapsed = time.time() - start
        print(f"✓ Report loaded successfully in {elapsed:.2f}s")
        print(f"  Patient: {report.patient_name}")
        print(f"  Diagnosis: {report.diagnosis.value}")
        print(f"  Polyps: {report.num_polyps}")
        return True, elapsed
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Failed in {elapsed:.2f}s: {e}")
        return False, elapsed


async def test_clinical_planner_only():
    """Test 2: Clinical Planner Agent only."""
    print("\n" + "="*80)
    print("TEST 2: Clinical Planner (GPT-5)")
    print("="*80)

    # Load report
    with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
        reports_data = json.load(f)
    report = PathologyReport(**reports_data[0])

    print(f"Patient: {report.patient_name}")
    print(f"Diagnosis: {report.diagnosis.value}")
    print()

    start = time.time()
    try:
        # Set 10 second timeout
        clinical_plan = await asyncio.wait_for(
            clinical_planner.create_clinical_plan(
                report=report,
                clinician_id="dr-test-001"
            ),
            timeout=10.0
        )

        elapsed = time.time() - start
        print(f"✓ Clinical plan created in {elapsed:.2f}s")
        print(f"  Treatment: {clinical_plan.treatment_plan[:100]}...")
        print(f"  Actions: {len(clinical_plan.follow_up_actions)}")
        print(f"  Urgency: {clinical_plan.urgency_level}")
        return True, elapsed, clinical_plan
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.2f}s")
        return False, elapsed, None
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Failed in {elapsed:.2f}s: {e}")
        import traceback
        traceback.print_exc()
        return False, elapsed, None


async def test_patient_communicator_only():
    """Test 3: Patient Communicator Agent only."""
    print("\n" + "="*80)
    print("TEST 3: Patient Communicator (GPT-5)")
    print("="*80)

    # Load report
    with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
        reports_data = json.load(f)
    report = PathologyReport(**reports_data[0])

    # Create a simple clinical plan
    clinical_plan = ClinicalPlan(
        plan_id="test-plan",
        report_id=report.id,
        patient_id=report.patient_id,
        clinician_id="dr-test",
        diagnosis=report.diagnosis,
        treatment_plan=f"Surveillance in {report.surveillance_recommendation}",
        follow_up_actions=[
            f"Schedule colonoscopy in {report.surveillance_recommendation}",
            "Continue routine screenings"
        ],
        urgency_level="routine"
    )

    print(f"Patient: {report.patient_name}")
    print(f"Diagnosis: {report.diagnosis.value}")
    print()

    start = time.time()
    try:
        # Set 10 second timeout
        communication = await asyncio.wait_for(
            patient_communicator.generate_patient_message(
                report=report,
                clinical_plan=clinical_plan,
                message_type="portal"
            ),
            timeout=10.0
        )

        elapsed = time.time() - start
        print(f"✓ Patient message created in {elapsed:.2f}s")
        print(f"  Message length: {len(communication.message_content)} chars")
        print(f"  First 200 chars: {communication.message_content[:200]}...")
        return True, elapsed
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.2f}s")
        return False, elapsed
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Failed in {elapsed:.2f}s: {e}")
        import traceback
        traceback.print_exc()
        return False, elapsed


async def test_phenoml_query_only():
    """Test 4: PhenoML Query only."""
    print("\n" + "="*80)
    print("TEST 4: PhenoML Query")
    print("="*80)

    start = time.time()
    try:
        # Set 10 second timeout
        patients = await asyncio.wait_for(
            asyncio.to_thread(
                phenoml_service.query_patients,
                "Find patients named Jessica Jones"
            ),
            timeout=10.0
        )

        elapsed = time.time() - start
        print(f"✓ Query completed in {elapsed:.2f}s")
        print(f"  Found {len(patients)} patient(s)")
        return True, elapsed
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.2f}s")
        return False, elapsed
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Failed in {elapsed:.2f}s: {e}")
        return False, elapsed


async def main():
    """Run all individual endpoint tests."""
    print("\n" + "="*80)
    print("INDIVIDUAL ENDPOINT TESTS (10s timeout each)")
    print("="*80)

    results = []

    # Test 1: Load Report
    print("\n>>> Running Test 1...")
    success, elapsed = await test_load_report()
    results.append(("Load Report", success, elapsed))

    # Test 2: Clinical Planner
    print("\n>>> Running Test 2...")
    success, elapsed, clinical_plan = await test_clinical_planner_only()
    results.append(("Clinical Planner (GPT-5)", success, elapsed))

    # Test 3: Patient Communicator
    print("\n>>> Running Test 3...")
    success, elapsed = await test_patient_communicator_only()
    results.append(("Patient Communicator (GPT-5)", success, elapsed))

    # Test 4: PhenoML Query
    print("\n>>> Running Test 4...")
    success, elapsed = await test_phenoml_query_only()
    results.append(("PhenoML Query", success, elapsed))

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    for test_name, success, elapsed in results:
        status = "✓ PASS" if success else "✗ FAIL/TIMEOUT"
        print(f"{status}: {test_name:<30} - {elapsed:.2f}s")

    print("\n" + "="*80)

    passed = sum(1 for _, success, _ in results if success)
    print(f"\n{passed}/{len(results)} tests passed\n")

    return passed == len(results)


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
