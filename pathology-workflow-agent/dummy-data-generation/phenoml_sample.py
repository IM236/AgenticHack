#!/usr/bin/env python3
"""
PhenoML FHIR Sample Implementation
===================================

A minimal working example for uploading and querying FHIR data using PhenoML.

SETUP:
------
1. pip install phenoml pytest python-dotenv
2. Ensure credentials are set in ../pathology-workflow-agent/.env

USAGE:
------
# Run examples:
python phenoml_sample.py

# Run tests:
pytest phenoml_sample.py -v

SAMPLE DATA:
------------
This script creates these sample FHIR records:

Patient 1: Sarah Johnson (female, DOB: 1985-06-15, Seattle, WA)
  - Condition: Hypertension (diagnosed 2019-03-10, active)
  - Medication: Lisinopril 10mg once daily

Patient 2: Michael Chen (male, DOB: 1978-11-22, Boston, MA)
  - Condition: Type 2 Diabetes (diagnosed 2018-07-15, active)
  - Medication: Metformin 1000mg twice daily

Patient 3: Emily Rodriguez (female, DOB: 1992-04-08, Portland, OR)
  - Condition: Asthma (diagnosed 2015-05-20, active)
  - Medication: Albuterol 90mcg as needed
"""

import os
from typing import Dict, List, Any
from phenoml import Client
from dotenv import load_dotenv


# =============================================================================
# CONFIGURATION - LOADED FROM .ENV FILE
# =============================================================================

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

PHENOML_USERNAME = os.getenv("PHENOML_USERNAME")
PHENOML_PASSWORD = os.getenv("PHENOML_PASSWORD")
PHENOML_BASE_URL = os.getenv("PHENOML_BASE_URL")
PROVIDER = os.getenv("PROVIDER")


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def get_client() -> Client:
    """Get authenticated PhenoML client."""
    if not PHENOML_USERNAME or not PHENOML_PASSWORD:
        raise ValueError("Update PHENOML_USERNAME and PHENOML_PASSWORD at top of file")

    return Client(
        username=PHENOML_USERNAME,
        password=PHENOML_PASSWORD,
        base_url=PHENOML_BASE_URL
    )


def upload_patient_record(client: Client, patient: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upload a complete patient record with conditions and medications.

    Args:
        client: PhenoML client
        patient: Dict with keys: name, gender, birth_date, location,
                 conditions (list), medications (list)

    Returns:
        Dict with creation results
    """
    results = {"patient": None, "conditions": [], "medications": []}

    # Create patient
    patient_text = (
        f"Create a patient named {patient['name']}, "
        f"{patient['gender']}, born on {patient['birth_date']}, "
        f"living in {patient['location']}"
    )

    patient_result = client.tools.create_fhir_resource(
        resource="patient",
        text=patient_text,
        provider=PROVIDER
    )
    results["patient"] = {"success": patient_result.success, "message": patient_result.message}

    # Create conditions
    for condition in patient.get("conditions", []):
        cond_text = (
            f"Patient {patient['name']} has {condition['name']} "
            f"diagnosed on {condition['diagnosed_date']}, currently {condition['status']}"
        )
        cond_result = client.tools.create_fhir_resource(
            resource="condition-encounter-diagnosis",
            text=cond_text,
            provider=PROVIDER
        )
        results["conditions"].append({"success": cond_result.success, "name": condition['name']})

    # Create medications
    for med in patient.get("medications", []):
        med_text = (
            f"Prescribe {med['name']} {med['dosage']} {med['frequency']} "
            f"for patient {patient['name']} for {med['indication']}"
        )
        med_result = client.tools.create_fhir_resource(
            resource="medicationrequest",
            text=med_text,
            provider=PROVIDER
        )
        results["medications"].append({"success": med_result.success, "name": med['name']})

    return results


def query_patients(client: Client, query: str) -> List[Dict[str, Any]]:
    """Query patients using natural language."""
    result = client.tools.search_fhir_resources(text=query, provider=PROVIDER)
    return result.fhir_results if hasattr(result, 'fhir_results') else []


def query_conditions(client: Client, query: str) -> List[Dict[str, Any]]:
    """Query conditions using natural language."""
    result = client.tools.search_fhir_resources(text=query, provider=PROVIDER)
    return result.fhir_results if hasattr(result, 'fhir_results') else []


# =============================================================================
# SAMPLE DATA
# =============================================================================

SAMPLE_PATIENTS = [
    {
        "name": "Sarah Johnson",
        "gender": "female",
        "birth_date": "1985-06-15",
        "location": "Seattle, WA",
        "conditions": [
            {
                "name": "Hypertension",
                "diagnosed_date": "2019-03-10",
                "status": "active"
            }
        ],
        "medications": [
            {
                "name": "Lisinopril",
                "dosage": "10mg",
                "frequency": "once daily",
                "indication": "Hypertension"
            }
        ]
    },
    {
        "name": "Michael Chen",
        "gender": "male",
        "birth_date": "1978-11-22",
        "location": "Boston, MA",
        "conditions": [
            {
                "name": "Type 2 Diabetes",
                "diagnosed_date": "2018-07-15",
                "status": "active"
            }
        ],
        "medications": [
            {
                "name": "Metformin",
                "dosage": "1000mg",
                "frequency": "twice daily",
                "indication": "Type 2 Diabetes"
            }
        ]
    },
    {
        "name": "Emily Rodriguez",
        "gender": "female",
        "birth_date": "1992-04-08",
        "location": "Portland, OR",
        "conditions": [
            {
                "name": "Asthma",
                "diagnosed_date": "2015-05-20",
                "status": "active"
            }
        ],
        "medications": [
            {
                "name": "Albuterol",
                "dosage": "90mcg",
                "frequency": "as needed",
                "indication": "Asthma"
            }
        ]
    }
]


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

def test_upload_sample_patients():
    """Test uploading sample patients."""
    client = get_client()

    for patient in SAMPLE_PATIENTS:
        result = upload_patient_record(client, patient)

        # Verify patient created
        assert result["patient"]["success"], f"Failed to create patient {patient['name']}"

        # Verify conditions created
        for cond in result["conditions"]:
            assert cond["success"], f"Failed to create condition {cond['name']}"

        # Verify medications created
        for med in result["medications"]:
            assert med["success"], f"Failed to create medication {med['name']}"


def test_query_female_patients():
    """Test querying for female patients."""
    client = get_client()

    patients = query_patients(client, "Find female patients")

    # Should find at least some female patients
    assert len(patients) > 0, "No female patients found"

    # Verify they are actually female
    has_female = any(p.get("gender") == "female" for p in patients)
    assert has_female, "Found patients but none are female"


def test_query_by_name():
    """Test querying for a specific patient by name."""
    client = get_client()

    patients = query_patients(client, "Find patient named Sarah Johnson")

    # Should find at least one patient
    assert len(patients) >= 1, "Could not find Sarah Johnson"


def test_query_diabetes_conditions():
    """Test querying for diabetes conditions."""
    client = get_client()

    conditions = query_conditions(client, "Find patients with diabetes")

    # Should find at least one diabetes condition
    assert len(conditions) >= 1, "No diabetes conditions found"


def test_end_to_end_workflow():
    """Test complete workflow: create patient and query it back."""
    client = get_client()

    # Create a unique test patient
    test_patient = {
        "name": "Test Patient E2E",
        "gender": "male",
        "birth_date": "1990-01-01",
        "location": "Test City",
        "conditions": [
            {
                "name": "Test Condition",
                "diagnosed_date": "2024-01-01",
                "status": "active"
            }
        ],
        "medications": []
    }

    # Upload
    result = upload_patient_record(client, test_patient)
    assert result["patient"]["success"], "Failed to create test patient"

    # Query back
    patients = query_patients(client, "Find patient named Test Patient E2E")
    assert len(patients) >= 1, "Could not find newly created patient"


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def main():
    """Run examples."""
    print("="*80)
    print("PhenoML FHIR Sample Implementation")
    print("="*80)
    print()

    # Initialize client
    client = get_client()
    print(f"✓ Connected to {PHENOML_BASE_URL}")
    print()

    # Upload sample patients
    print("Uploading sample patients...")
    for i, patient in enumerate(SAMPLE_PATIENTS, 1):
        print(f"\n  Patient {i}: {patient['name']}")
        result = upload_patient_record(client, patient)

        print(f"    ✓ Patient created: {result['patient']['success']}")
        print(f"    ✓ Conditions: {len(result['conditions'])}")
        print(f"    ✓ Medications: {len(result['medications'])}")

    print()
    print("="*80)

    # Query patients
    print("\nQuerying female patients...")
    female_patients = query_patients(client, "Find female patients")
    print(f"  Found {len(female_patients)} female patients")

    # Show first 3
    for i, patient in enumerate(female_patients[:3], 1):
        name_obj = patient.get('name', [{}])[0]
        given = ' '.join(name_obj.get('given', []))
        family = name_obj.get('family', '')
        name = f"{given} {family}".strip() or "Unknown"
        print(f"    {i}. {name} (DOB: {patient.get('birthDate', 'N/A')})")

    print()
    print("="*80)

    # Query conditions
    print("\nQuerying diabetes conditions...")
    diabetes = query_conditions(client, "Find patients with diabetes")
    print(f"  Found {len(diabetes)} diabetes condition(s)")

    print()
    print("="*80)
    print("\n✓ All examples completed successfully!")
    print("\nRun tests with: pytest phenoml_sample.py -v")
    print()


if __name__ == "__main__":
    main()
