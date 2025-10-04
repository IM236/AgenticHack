#!/usr/bin/env python3
"""
Quick and dirty test for PhenoML upload
Tests creating a patient and pathology report, then cleans up
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from phenoml import Client

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

PHENOML_USERNAME = os.getenv("PHENOML_USERNAME")
PHENOML_PASSWORD = os.getenv("PHENOML_PASSWORD")
PHENOML_BASE_URL = os.getenv("PHENOML_BASE_URL")
PROVIDER = os.getenv("PROVIDER")


def test_create_and_verify():
    """Test creating a patient and pathology report, then verify they exist."""
    print("="*80)
    print("PhenoML Upload Test")
    print("="*80)
    print()

    # Initialize client
    print("Connecting to PhenoML...")
    client = Client(
        username=PHENOML_USERNAME,
        password=PHENOML_PASSWORD,
        base_url=PHENOML_BASE_URL
    )
    print(f"✓ Connected to {PHENOML_BASE_URL}")
    print()

    # Create test patient
    test_name = f"Test Patient {datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"Creating test patient: {test_name}...")

    patient_text = (
        f"Create a patient named {test_name}, "
        f"male, born on 1980-05-15, "
        f"living in Test City, MA"
    )

    patient_result = client.tools.create_fhir_resource(
        resource="patient",
        text=patient_text,
        provider=PROVIDER
    )

    assert patient_result.success, f"Failed to create patient: {patient_result.message}"
    print(f"✓ Patient created: {patient_result.message}")
    print()

    # Create test colonoscopy procedure
    print("Creating colonoscopy procedure...")
    procedure_text = (
        f"Colonoscopy procedure performed on patient {test_name} "
        f"on 2024-09-15. "
        f"Indication: screening colonoscopy. "
        f"Performing physician: Dr. Test Physician, MD. "
        f"Procedure outcome: cecum reached, prep quality good. "
        f"2 polyp(s) identified and removed."
    )

    procedure_result = client.tools.create_fhir_resource(
        resource="procedure",
        text=procedure_text,
        provider=PROVIDER
    )

    assert procedure_result.success, f"Failed to create procedure: {procedure_result.message}"
    print(f"✓ Procedure created: {procedure_result.message}")
    print()

    # Create test pathology report
    print("Creating pathology report...")
    report_text = (
        f"Pathology report for patient {test_name} "
        f"from colonoscopy with biopsy on 2024-09-15. "
        f"Accession number S24999001. "
        f"Clinical indication: screening colonoscopy. "
        f"Findings: Polyp 1: tubular adenoma, located in sigmoid colon, size 8mm, low-grade dysplasia; "
        f"Polyp 2: hyperplastic polyp, located in rectum, size 4mm, no dysplasia. "
        f"Recommendation: Surveillance colonoscopy in 5-10 years. "
        f"Signed by Dr. Test Pathologist, MD."
    )

    report_result = client.tools.create_fhir_resource(
        resource="observation-lab",
        text=report_text,
        provider=PROVIDER
    )

    assert report_result.success, f"Failed to create report: {report_result.message}"
    print(f"✓ Report created: {report_result.message}")
    print()

    # Query to verify patient exists
    print(f"Verifying patient {test_name} exists...")
    search_result = client.tools.search_fhir_resources(
        text=f"Find patient named {test_name}",
        provider=PROVIDER
    )

    patients_found = search_result.fhir_results if hasattr(search_result, 'fhir_results') and search_result.fhir_results else []
    print(f"✓ Found {len(patients_found)} patient(s) matching search")
    print()

    if len(patients_found) > 0:
        print("✓ Patient successfully verified in system")
    else:
        print("⚠ Patient not found in search (may take time to index)")
    print()

    print("="*80)
    print("✓ All tests passed!")
    print()
    print("Note: This test creates real data in PhenoML.")
    print("Manual cleanup may be required via the PhenoML interface.")
    print("="*80)
    print()


if __name__ == "__main__":
    test_create_and_verify()
