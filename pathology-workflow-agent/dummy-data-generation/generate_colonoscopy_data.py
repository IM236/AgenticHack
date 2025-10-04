#!/usr/bin/env python3
"""
Generate Colonoscopy Pathology Data
====================================

Creates 20 patients with colonoscopy pathology reports for polyps.
Uploads to PhenoML/Medplum and saves to JSON files.

SETUP:
------
1. Ensure credentials are set in ../pathology-workflow-agent/.env
2. Run: uv run python dummy-data-generation/generate_colonoscopy_data.py
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from phenoml import Client
from dotenv import load_dotenv
from tqdm import tqdm


# =============================================================================
# CONFIGURATION
# =============================================================================

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

PHENOML_USERNAME = os.getenv("PHENOML_USERNAME")
PHENOML_PASSWORD = os.getenv("PHENOML_PASSWORD")
PHENOML_BASE_URL = os.getenv("PHENOML_BASE_URL")
PROVIDER = os.getenv("PROVIDER")

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


# =============================================================================
# SAMPLE DATA GENERATORS
# =============================================================================

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

CITIES_STATES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"),
    ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"),
    ("Dallas", "TX"), ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("San Francisco", "CA"),
    ("Indianapolis", "IN"), ("Seattle", "WA"), ("Denver", "CO"), ("Boston", "MA")
]

POLYP_TYPES = [
    "tubular adenoma",
    "tubulovillous adenoma",
    "villous adenoma",
    "hyperplastic polyp",
    "sessile serrated adenoma",
    "inflammatory polyp"
]

POLYP_LOCATIONS = [
    "ascending colon",
    "transverse colon",
    "descending colon",
    "sigmoid colon",
    "rectum",
    "cecum"
]

DYSPLASIA_GRADES = [
    "no dysplasia",
    "low-grade dysplasia",
    "high-grade dysplasia"
]

REMOVAL_METHODS = [
    "cold snare polypectomy",
    "hot snare polypectomy",
    "cold forceps biopsy",
    "endoscopic mucosal resection (EMR)"
]

INDICATIONS = [
    "screening colonoscopy",
    "surveillance colonoscopy (history of polyps)",
    "diagnostic colonoscopy (positive FIT test)",
    "surveillance colonoscopy (family history)"
]

PHYSICIANS = [
    "Dr. James Smith, MD",
    "Dr. Maria Garcia, MD",
    "Dr. David Lee, MD",
    "Dr. Lisa Patel, MD"
]


def generate_patient_data(index: int) -> Dict[str, Any]:
    """Generate realistic patient data."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    gender = random.choice(["male", "female"])

    # Age between 45-80 (colonoscopy screening age)
    age = random.randint(45, 80)
    birth_year = datetime.now().year - age
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"

    city, state = random.choice(CITIES_STATES)

    return {
        "id": f"patient_{index:03d}",
        "name": f"{first_name} {last_name}",
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "birth_date": birth_date,
        "age": age,
        "location": f"{city}, {state}"
    }


def generate_pathology_report(patient: Dict[str, Any], report_index: int) -> Dict[str, Any]:
    """Generate colonoscopy pathology report for polyps."""
    # Procedure date within last 2 years
    days_ago = random.randint(30, 730)
    procedure_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    # Number of polyps found (1-4)
    num_polyps = random.randint(1, 4)

    polyps = []
    for i in range(num_polyps):
        polyp_type = random.choice(POLYP_TYPES)
        polyp = {
            "number": i + 1,
            "type": polyp_type,
            "location": random.choice(POLYP_LOCATIONS),
            "size_mm": random.randint(3, 25),
            "dysplasia": random.choice(DYSPLASIA_GRADES) if "adenoma" in polyp_type else "no dysplasia",
            "removal_method": random.choice(REMOVAL_METHODS)
        }
        polyps.append(polyp)

    # Generate accession number
    accession = f"S{datetime.now().year % 100}{random.randint(1000, 9999)}{report_index:03d}"

    # Clinical indication
    indication = random.choice(INDICATIONS)

    # Procedure quality metrics
    cecal_intubation = random.choice([True, True, True, False])  # 75% success rate
    prep_quality = random.choice(["excellent", "good", "adequate", "poor"])

    # Surveillance recommendation based on findings
    has_advanced_adenoma = any(
        p["size_mm"] >= 10 or "high-grade" in p["dysplasia"] or "villous" in p["type"]
        for p in polyps
    )
    if has_advanced_adenoma:
        surveillance = "3 years"
    elif num_polyps >= 3:
        surveillance = "3 years"
    elif any("adenoma" in p["type"] for p in polyps):
        surveillance = "5-10 years"
    else:
        surveillance = "10 years"

    return {
        "id": f"report_{patient['id']}_{report_index:02d}",
        "patient_id": patient["id"],
        "patient_name": patient["name"],
        "accession_number": accession,
        "procedure_date": procedure_date,
        "procedure_type": "colonoscopy with biopsy",
        "indication": indication,
        "physician": random.choice(PHYSICIANS),
        "specimen_type": "colon polyp(s)",
        "clinical_history": f"{patient['age']}-year-old {patient['gender']} with {indication}",
        "cecal_intubation": cecal_intubation,
        "prep_quality": prep_quality,
        "num_polyps": num_polyps,
        "polyps": polyps,
        "report_date": procedure_date,
        "pathologist": random.choice([
            "Dr. Michael Chen, MD",
            "Dr. Sarah Williams, MD",
            "Dr. Robert Martinez, MD",
            "Dr. Jennifer Anderson, MD"
        ]),
        "surveillance_recommendation": surveillance
    }


# =============================================================================
# PHENOML CLIENT
# =============================================================================

def get_client() -> Client:
    """Get authenticated PhenoML client."""
    if not PHENOML_USERNAME or not PHENOML_PASSWORD:
        raise ValueError("PhenoML credentials not found in .env file")

    return Client(
        username=PHENOML_USERNAME,
        password=PHENOML_PASSWORD,
        base_url=PHENOML_BASE_URL
    )


# =============================================================================
# UPLOAD FUNCTIONS (following phenoml_sample.py pattern)
# =============================================================================

def upload_patient(client: Client, patient: Dict[str, Any]) -> Dict[str, Any]:
    """Upload patient to PhenoML."""
    patient_text = (
        f"Create a patient named {patient['name']}, "
        f"{patient['gender']}, born on {patient['birth_date']}, "
        f"living in {patient['location']}"
    )

    print(f"    [DEBUG] Uploading patient: {patient['name']}", flush=True)
    result = client.tools.create_fhir_resource(
        resource="patient",
        text=patient_text,
        provider=PROVIDER
    )
    print(f"    [DEBUG] Patient result: {result.success}", flush=True)

    return {"success": result.success, "message": result.message}


def upload_pathology_report(client: Client, report: Dict[str, Any]) -> Dict[str, Any]:
    """Upload pathology report as DiagnosticReport to PhenoML."""
    # Build detailed findings text
    findings = []
    for polyp in report["polyps"]:
        finding = (
            f"Polyp {polyp['number']}: {polyp['type']}, "
            f"located in {polyp['location']}, "
            f"size {polyp['size_mm']}mm, "
            f"{polyp['dysplasia']}, "
            f"removed by {polyp['removal_method']}"
        )
        findings.append(finding)

    findings_text = "; ".join(findings)

    cecal_status = "cecum reached" if report["cecal_intubation"] else "cecum not reached"

    report_text = (
        f"Pathology report for patient {report['patient_name']} "
        f"from {report['procedure_type']} on {report['procedure_date']}. "
        f"Accession number {report['accession_number']}. "
        f"Clinical indication: {report['indication']}. "
        f"Performing physician: {report['physician']}. "
        f"Procedure quality: {cecal_status}, prep quality {report['prep_quality']}. "
        f"Clinical history: {report['clinical_history']}. "
        f"Specimen: {report['specimen_type']}. "
        f"Findings: {findings_text}. "
        f"Recommendation: Surveillance colonoscopy in {report['surveillance_recommendation']}. "
        f"Signed by {report['pathologist']}."
    )

    result = client.tools.create_fhir_resource(
        resource="observation-lab",
        text=report_text,
        provider=PROVIDER
    )

    return {"success": result.success, "message": result.message}


def upload_specimen(client: Client, report: Dict[str, Any], polyp: Dict[str, Any]) -> Dict[str, Any]:
    """Upload specimen information to PhenoML."""
    specimen_text = (
        f"Specimen from patient {report['patient_name']}, "
        f"collected during colonoscopy on {report['procedure_date']}, "
        f"specimen type: colon biopsy from {polyp['location']}, "
        f"collection method: {polyp['removal_method']}, "
        f"accession number {report['accession_number']}"
    )

    result = client.tools.create_fhir_resource(
        resource="observation-clinical-result",
        text=specimen_text,
        provider=PROVIDER
    )

    return {"success": result.success, "message": result.message}


def upload_observation(client: Client, report: Dict[str, Any], polyp: Dict[str, Any]) -> Dict[str, Any]:
    """Upload polyp observation to PhenoML."""
    observation_text = (
        f"Pathology observation for patient {report['patient_name']}: "
        f"{polyp['type']} found in {polyp['location']}, "
        f"measuring {polyp['size_mm']}mm, "
        f"showing {polyp['dysplasia']}, "
        f"removed by {polyp['removal_method']}, "
        f"from procedure on {report['procedure_date']}"
    )

    result = client.tools.create_fhir_resource(
        resource="observation-clinical-result",
        text=observation_text,
        provider=PROVIDER
    )

    return {"success": result.success, "message": result.message}


def upload_procedure(client: Client, report: Dict[str, Any]) -> Dict[str, Any]:
    """Upload colonoscopy procedure to PhenoML."""
    cecal_status = "cecum reached" if report["cecal_intubation"] else "cecum not reached"

    procedure_text = (
        f"Colonoscopy procedure performed on patient {report['patient_name']} "
        f"on {report['procedure_date']}. "
        f"Indication: {report['indication']}. "
        f"Performing physician: {report['physician']}. "
        f"Procedure outcome: {cecal_status}, prep quality {report['prep_quality']}. "
        f"{report['num_polyps']} polyp(s) identified and removed."
    )

    result = client.tools.create_fhir_resource(
        resource="procedure",
        text=procedure_text,
        provider=PROVIDER
    )

    return {"success": result.success, "message": result.message}


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """Generate data and upload to PhenoML."""
    print("="*80)
    print("Colonoscopy Pathology Data Generation")
    print("="*80)
    print()

    # Initialize client
    client = get_client()
    print(f"✓ Connected to {PHENOML_BASE_URL}")
    print()

    # Generate patients
    print("Generating 20 patients...")
    patients = [generate_patient_data(i) for i in range(1, 21)]
    print(f"✓ Generated {len(patients)} patients")
    print()

    # Generate pathology reports (1 per patient for speed)
    print("Generating pathology reports...")
    all_reports = []
    for patient in patients:
        report = generate_pathology_report(patient, 1)
        all_reports.append(report)
    print(f"✓ Generated {len(all_reports)} pathology reports")
    print()

    # Save to JSON files
    patients_file = os.path.join(DATA_DIR, 'patients.json')
    reports_file = os.path.join(DATA_DIR, 'pathology_reports.json')

    with open(patients_file, 'w') as f:
        json.dump(patients, f, indent=2)
    print(f"✓ Saved patients to {patients_file}")

    with open(reports_file, 'w') as f:
        json.dump(all_reports, f, indent=2)
    print(f"✓ Saved reports to {reports_file}")
    print()

    # Upload to PhenoML
    print("Uploading to PhenoML...")
    print()

    upload_success = {"patients": 0, "procedures": 0, "reports": 0, "specimens": 0, "observations": 0}

    for patient in tqdm(patients, desc="Uploading patients", unit="patient"):
        # Upload patient
        patient_result = upload_patient(client, patient)
        if patient_result["success"]:
            upload_success["patients"] += 1

        # Find and upload reports for this patient
        patient_reports = [r for r in all_reports if r["patient_id"] == patient["id"]]

        for report in patient_reports:
            # Upload procedure
            procedure_result = upload_procedure(client, report)
            if procedure_result["success"]:
                upload_success["procedures"] += 1

            # Upload diagnostic report
            report_result = upload_pathology_report(client, report)
            if report_result["success"]:
                upload_success["reports"] += 1

    print()
    print("="*80)
    print("\n✓ Upload Summary:")
    print(f"  - Patients: {upload_success['patients']}/{len(patients)}")
    print(f"  - Procedures: {upload_success['procedures']}/{len(all_reports)}")
    print(f"  - Reports: {upload_success['reports']}/{len(all_reports)}")
    print(f"  - Specimens: {upload_success['specimens']}")
    print(f"  - Observations: {upload_success['observations']}")
    print()
    print("="*80)
    print()


if __name__ == "__main__":
    main()
