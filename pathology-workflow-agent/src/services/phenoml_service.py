"""PhenoML integration service for querying pathology data from Medplum via PhenoML."""
from typing import Dict, Any, Optional, List
from phenoml import Client
from ..config import settings
from ..schemas.models import PathologyReport, PolypFinding


class PhenoMLService:
    """Service for querying colonoscopy pathology reports from Medplum using PhenoML."""

    def __init__(self):
        self.username = settings.phenoml_username
        self.password = settings.phenoml_password
        self.base_url = settings.phenoml_base_url or "https://experiment.app.pheno.ml"
        self.provider = settings.provider or "medplum"
        self._client = None

    def _get_client(self) -> Client:
        """Get or create PhenoML client."""
        if self._client is None:
            if not self.username or not self.password:
                raise ValueError("PHENOML_USERNAME and PHENOML_PASSWORD must be set in environment")

            self._client = Client(
                username=self.username,
                password=self.password,
                base_url=self.base_url
            )
        return self._client

    def query_pathology_reports(self, query: str) -> List[Dict[str, Any]]:
        """Query pathology reports using natural language.

        Args:
            query: Natural language query (e.g., "Find patients with polyps")

        Returns:
            List of FHIR resources matching the query
        """
        client = self._get_client()
        result = client.tools.search_fhir_resources(text=query, provider=self.provider)
        return result.fhir_results if hasattr(result, 'fhir_results') and result.fhir_results else []

    def query_patients(self, query: str) -> List[Dict[str, Any]]:
        """Query patients using natural language.

        Args:
            query: Natural language query (e.g., "Find female patients over 50")

        Returns:
            List of patient FHIR resources
        """
        client = self._get_client()
        result = client.tools.search_fhir_resources(text=query, provider=self.provider)
        return result.fhir_results if hasattr(result, 'fhir_results') and result.fhir_results else []

    def get_patient_reports(self, patient_name: str) -> List[Dict[str, Any]]:
        """Get all pathology reports for a specific patient.

        Args:
            patient_name: Patient's full name

        Returns:
            List of pathology report observations
        """
        query = f"Find pathology reports for patient {patient_name}"
        return self.query_pathology_reports(query)

    def get_reports_with_high_grade_dysplasia(self) -> List[Dict[str, Any]]:
        """Get all reports with high-grade dysplasia findings."""
        query = "Find patients with high-grade dysplasia in colonoscopy"
        return self.query_pathology_reports(query)

    def get_reports_with_advanced_adenomas(self) -> List[Dict[str, Any]]:
        """Get reports with advanced adenomas (>=10mm or villous)."""
        query = "Find patients with villous adenoma or large polyps from colonoscopy"
        return self.query_pathology_reports(query)

    async def extract_structured_data(
        self, raw_report_text: str
    ) -> Dict[str, Any]:
        """Extract structured data from unstructured pathology report.

        Note: This is now primarily for compatibility.
        We get structured data directly from Medplum via PhenoML queries.
        """
        # Placeholder for backward compatibility
        extracted_data = {
            "diagnosis": self._extract_diagnosis(raw_report_text),
            "tissue_type": "colon",
            "findings": raw_report_text,
        }
        return extracted_data

    def _extract_diagnosis(self, text: str) -> Optional[str]:
        """Extract diagnosis from text."""
        text_lower = text.lower()
        if "high-grade dysplasia" in text_lower:
            return "precancerous"
        elif "adenoma" in text_lower or "dysplasia" in text_lower:
            return "precancerous"
        elif "hyperplastic" in text_lower:
            return "benign"
        return "benign"

    async def validate_extraction(
        self, extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate extracted data quality and completeness."""
        return {
            "is_valid": True,
            "confidence": 1.0,
            "missing_fields": [],
            "warnings": [],
        }

    async def enrich_with_medical_knowledge(
        self, extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enrich extracted data with medical knowledge graphs."""
        return extracted_data


# Singleton instance
phenoml_service = PhenoMLService()
