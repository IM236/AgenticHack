#!/usr/bin/env python3
"""Test patient message generation with colonoscopy pathology data (without OpenAI)."""

import json
from src.schemas.models import PathologyReport, ClinicalPlan, DiagnosisType


def generate_simple_patient_message(report: PathologyReport, clinical_plan: ClinicalPlan) -> str:
    """Generate a simple patient message without AI."""

    message = f"""Dear {report.patient_name},

Your recent colonoscopy results from {report.procedure_date} are now available.

PROCEDURE SUMMARY:
We found {report.num_polyps} polyp(s) during your colonoscopy, which were removed and sent for analysis.

FINDINGS:
{report.findings}

WHAT THIS MEANS:
"""

    if report.diagnosis == DiagnosisType.PRECANCEROUS:
        message += """The polyps showed some pre-cancerous changes. This is relatively common and doesn't mean you have cancer. These findings indicate that regular monitoring with colonoscopy is important to catch any changes early.
"""
    elif report.diagnosis == DiagnosisType.BENIGN:
        message += """The polyps were benign (non-cancerous). This is good news! Regular surveillance colonoscopy will help ensure your continued health.
"""

    message += f"""
NEXT STEPS:
"""
    for action in clinical_plan.follow_up_actions:
        message += f"• {action}\n"

    message += f"""
SURVEILLANCE PLAN:
Your next colonoscopy is recommended in {report.surveillance_recommendation}.

URGENCY:
This is a {clinical_plan.urgency_level} matter. {
    'Please schedule your follow-up soon.' if clinical_plan.urgency_level == 'urgent'
    else 'You can schedule at your convenience during normal business hours.'
}

If you have any questions or concerns about these results, please don't hesitate to contact your healthcare provider.

Best regards,
{report.pathologist}
"""

    return message


def main():
    """Test generating patient message from colonoscopy report."""

    # Load a sample report
    with open('dummy-data-generation/data/pathology_reports.json', 'r') as f:
        reports_data = json.load(f)

    print("="*80)
    print("Patient Message Generation Test (Colonoscopy Pathology)")
    print("="*80)
    print()

    for i, report_data in enumerate(reports_data[:2], 1):  # Test first 2 reports
        # Create PathologyReport from JSON
        report = PathologyReport(**report_data)

        print(f"\n{'='*80}")
        print(f"REPORT {i}: {report.patient_name}")
        print(f"{'='*80}\n")

        print(f"Procedure Date: {report.procedure_date}")
        print(f"Diagnosis: {report.diagnosis.value}")
        print(f"Findings: {report.findings}")
        print(f"Surveillance: {report.surveillance_recommendation}")
        print()

        # Create a mock clinical plan
        clinical_plan = ClinicalPlan(
            plan_id=f"test-plan-{i:03d}",
            report_id=report.id,
            patient_id=report.patient_id,
            clinician_id="dr-smith-001",
            diagnosis=report.diagnosis,
            treatment_plan=f"Surveillance colonoscopy in {report.surveillance_recommendation}",
            follow_up_actions=[
                f"Schedule follow-up colonoscopy in {report.surveillance_recommendation}",
                "Continue routine health screenings",
                "Maintain a healthy diet with plenty of fiber",
                "Contact your doctor if you experience any concerning symptoms"
            ],
            urgency_level="urgent" if report.diagnosis == DiagnosisType.PRECANCEROUS else "routine"
        )

        # Generate patient message
        message = generate_simple_patient_message(report, clinical_plan)

        print("-"*80)
        print("PATIENT MESSAGE:")
        print("-"*80)
        print(message)
        print()


if __name__ == "__main__":
    main()
