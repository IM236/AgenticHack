# Physican Assistant

An automated pathology workflow system powered by AI agents that processes pathology reports, integrates with Epic EHR, and manages clinical follow-up workflows using LangGraph and OpenAI.

## Overview

This system automates the entire pathology report workflow from initial report submission through patient communication and follow-up scheduling. It leverages AI agents built with LangChain and orchestrated using LangGraph to ensure seamless processing of medical pathology reports.

## Architecture

### System Components

The application is structured in distinct layers:

```
pathology-workflow-agent/
├── main.py                          # FastAPI application entry point
├── src/
│   ├── config.py                    # Configuration management
│   ├── schemas/
│   │   └── models.py                # Pydantic data models
│   ├── services/
│   │   ├── phenoml_service.py       # PhenoML structured data extraction
│   │   └── epic_service.py          # Epic FHIR integration
│   ├── agents/
│   │   ├── report_processor.py      # Report analysis agent
│   │   ├── clinical_planner.py      # Clinical plan generation agent
│   │   └── patient_communicator.py  # Patient communication agent
│   └── workflows/
│       └── pathology_workflow.py    # LangGraph workflow orchestration
```

### Layer Architecture

#### 1. **API Layer** (`main.py`)
- **FastAPI Application**: Exposes REST endpoints for report submission and status tracking
- **Endpoints**:
  - `POST /api/v1/reports/submit` - Submit pathology reports for processing
  - `GET /api/v1/reports/{report_id}` - Get report status
  - `POST /api/v1/workflow/test` - Test endpoint with sample data
  - `GET /health` - Health check endpoint
- **Responsibilities**: Request validation, workflow invocation, response formatting

#### 2. **Configuration Layer** (`src/config.py`)
- **Settings Management**: Uses Pydantic Settings for environment-based configuration
- **Configuration Areas**:
  - OpenAI API credentials and model selection
  - Epic FHIR integration settings
  - PhenoML service configuration
  - SMTP notification settings
  - Database connection strings
- **Environment Loading**: Automatically loads from `.env` file

#### 3. **Data Models Layer** (`src/schemas/models.py`)
- **Pydantic Models**: Type-safe data structures for all entities
- **Core Models**:
  - `PathologyReport`: Structured pathology report data
  - `EpicUploadStatus`: Epic integration status tracking
  - `ClinicalPlan`: Treatment plans and follow-up actions
  - `PatientCommunication`: Patient messaging data
  - `WorkflowState`: LangGraph state management
- **Enums**: `DiagnosisType` for standardized diagnosis classification

#### 4. **Service Layer** (`src/services/`)

##### PhenoML Service (`phenoml_service.py`)
- **Purpose**: Extract structured data from unstructured pathology text
- **Capabilities**:
  - Diagnosis extraction
  - Medical code mapping (ICD, SNOMED)
  - Entity recognition
  - Data validation and enrichment
- **Note**: Currently boilerplate implementation; designed for PhenoML integration

##### Epic Service (`epic_service.py`)
- **Purpose**: Integration with Epic EHR via FHIR API
- **Capabilities**:
  - OAuth2 authentication with Epic
  - FHIR DiagnosticReport resource creation
  - Upload pathology reports to Epic
  - Clinician notification via Epic messaging
  - Patient data retrieval
- **FHIR Compliance**: Follows HL7 FHIR R4 DiagnosticReport specification

#### 5. **Agent Layer** (`src/agents/`)

All agents are powered by OpenAI's language models via LangChain.

##### Report Processor Agent (`report_processor.py`)
- **Model**: ChatOpenAI (GPT-4)
- **Temperature**: 0.1 (low variance for accuracy)
- **Purpose**: Analyze raw pathology reports
- **Tasks**:
  - Extract diagnosis type (benign, precancerous, cancerous, inconclusive)
  - Identify key findings
  - Extract recommendations
  - Structure unstructured text
- **Input**: Raw pathology report text
- **Output**: Structured `PathologyReport` object

##### Clinical Planner Agent (`clinical_planner.py`)
- **Model**: ChatOpenAI (GPT-4)
- **Temperature**: 0.2 (balanced creativity and consistency)
- **Purpose**: Generate evidence-based clinical plans
- **Tasks**:
  - Recommend treatment approaches
  - Define follow-up procedures and timelines
  - Assess urgency levels (routine, moderate, urgent)
  - Generate diagnosis-specific action plans
- **Decision Logic**:
  - Cancerous → Urgent oncology consultation, staging, surgical referral
  - Precancerous → Follow-up colonoscopy in 6 months, lifestyle education
  - Benign → Routine follow-up in 1 year
- **Input**: `PathologyReport` object
- **Output**: `ClinicalPlan` with treatment recommendations

##### Patient Communicator Agent (`patient_communicator.py`)
- **Model**: ChatOpenAI (GPT-4)
- **Temperature**: 0.3 (slightly more creative for natural communication)
- **Purpose**: Generate patient-friendly communications
- **Communication Style**:
  - Plain language (no medical jargon)
  - Empathetic and supportive tone
  - Clear next steps
  - Balanced transparency with reassurance
- **Channels**: Email, patient portal, phone
- **Input**: `PathologyReport` and `ClinicalPlan`
- **Output**: `PatientCommunication` with message content

#### 6. **Workflow Orchestration Layer** (`src/workflows/pathology_workflow.py`)

##### LangGraph Workflow
- **Framework**: LangGraph StateGraph for orchestration
- **State Management**: `PathologyWorkflowState` tracks workflow progression
- **Execution Model**: Asynchronous node-based graph execution

##### Workflow Steps

The workflow executes in the following sequence:

1. **Extract Data** (`extract_data`)
   - Uses PhenoML service to extract structured data
   - Updates state with extracted entities
   - Error handling with state error field

2. **Process Report** (`process_report`)
   - Report Processor Agent analyzes raw text
   - Enriches with PhenoML extracted data
   - Creates structured PathologyReport

3. **Upload to Epic** (`upload_to_epic`)
   - Converts to FHIR DiagnosticReport
   - Uploads to Epic EHR system
   - Tracks upload status

4. **Notify Clinician** (`notify_clinician`)
   - Sends notification via Epic messaging
   - Alerts clinician of new report availability

5. **Create Clinical Plan** (`create_clinical_plan`)
   - Clinical Planner Agent generates treatment plan
   - Defines follow-up actions and urgency

6. **Communicate with Patient** (`communicate_with_patient`)
   - Patient Communicator Agent generates message
   - Sends via patient portal/email/SMS
   - Tracks delivery status

7. **Schedule Follow-up** (`schedule_follow_up`)
   - Schedules appointments based on clinical plan
   - Marks workflow as completed

##### Workflow Graph Structure

```
START → extract_data → process_report → upload_to_epic → notify_clinician
          → create_clinical_plan → communicate_with_patient
          → schedule_follow_up → END
```

Each node can update the workflow state and handle errors independently. The graph ensures sequential execution with proper state propagation.

## Installation

### Prerequisites

- **Python**: >= 3.12
- **uv**: Fast Python package installer (recommended) or pip
- **OpenAI API Key**: Required for AI agents

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pathology-workflow-agent
   ```

2. **Create virtual environment**
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Or using standard Python
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Using uv
   uv pip install -e .

   # Or using pip
   pip install -e .
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Required environment variables** (edit `.env`):
   ```env
   # Minimum required configuration
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview

   # Optional: Epic integration
   EPIC_FHIR_BASE_URL=https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4
   EPIC_CLIENT_ID=your_epic_client_id
   EPIC_CLIENT_SECRET=your_epic_client_secret

   # Optional: PhenoML service
   PHENOML_API_URL=http://localhost:8001/api
   PHENOML_MODEL_PATH=/path/to/phenoml/models
   ```

## Running the Application

### Start the FastAPI Server

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage

### Submit a Pathology Report

```bash
curl -X POST "http://localhost:8000/api/v1/reports/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient_12345",
    "raw_report_text": "PATHOLOGY REPORT\n\nPatient: John Doe\nSpecimen: Colon biopsy\n\nDIAGNOSIS: High-grade dysplasia\nRECOMMENDATIONS: Follow-up colonoscopy in 3-6 months"
  }'
```

### Response Format

```json
{
  "workflow_id": "uuid",
  "status": "completed",
  "message": "Pathology report processed successfully",
  "data": {
    "report_id": "uuid",
    "current_step": "completed",
    "diagnosis": "precancerous",
    "epic_uploaded": true,
    "clinician_notified": true,
    "patient_communicated": true,
    "follow_up_scheduled": true
  }
}
```

### Test with Sample Data

```bash
curl -X POST "http://localhost:8000/api/v1/workflow/test"
```

## Dependencies

### Core Framework
- **FastAPI** (>=0.118.0): Modern web framework for building APIs
- **Uvicorn** (>=0.37.0): ASGI server for running FastAPI
- **Pydantic** (>=2.11.10): Data validation and settings management

### AI & Orchestration
- **LangChain-OpenAI** (>=0.3.34): OpenAI integration for LangChain
- **LangGraph** (>=0.6.8): Graph-based agent orchestration
- **OpenAI** (>=2.1.0): OpenAI API client

### HTTP & Utilities
- **httpx** (>=0.28.1): Async HTTP client for API calls
- **python-multipart** (>=0.0.20): Form data parsing

## Development

### Project Structure Explained

- **Configuration**: Centralized in `src/config.py` using environment variables
- **Type Safety**: All data structures use Pydantic models for validation
- **Service Layer**: External integrations (PhenoML, Epic) isolated in services
- **Agent Layer**: AI agents are independent, single-responsibility modules
- **Workflow Orchestration**: LangGraph manages complex multi-step workflows
- **API Layer**: FastAPI handles HTTP routing and validation

### Extension Points

1. **Add New Agents**: Create new agents in `src/agents/` following the existing pattern
2. **Extend Workflow**: Modify `pathology_workflow.py` to add/remove workflow steps
3. **Add Services**: Create new service integrations in `src/services/`
4. **Custom Models**: Define new data models in `src/schemas/models.py`

## How the Layers Interact

### Request Flow Example

1. **Client** sends POST request to `/api/v1/reports/submit`
2. **API Layer** (main.py) validates request using Pydantic models
3. **Workflow Layer** initiates `pathology_workflow.run()`
4. **Graph Orchestration**:
   - **Service Layer**: PhenoML extracts structured data
   - **Agent Layer**: Report Processor analyzes report
   - **Service Layer**: Epic Service uploads to EHR
   - **Service Layer**: Epic Service notifies clinician
   - **Agent Layer**: Clinical Planner creates treatment plan
   - **Agent Layer**: Patient Communicator generates message
   - **Service Layer**: Message delivery system sends communication
   - **Service Layer**: Scheduling system books follow-up
5. **State Management**: LangGraph tracks state through each step
6. **API Layer** returns final workflow state to client

### Data Flow

```
Raw Text → PhenoML Service → Structured Data
                ↓
         Report Processor Agent → PathologyReport
                ↓
         Epic Service → FHIR Upload → EpicUploadStatus
                ↓
         Clinical Planner Agent → ClinicalPlan
                ↓
         Patient Communicator Agent → PatientCommunication
                ↓
         Complete Workflow State → API Response
```

## Current Limitations & TODOs

### PhenoML Integration
- Currently boilerplate implementation
- Needs actual model loading and inference logic
- Medical ontology mapping (ICD, SNOMED) not implemented

### Epic Integration
- OAuth2 authentication flow needs completion
- Actual FHIR API calls are stubbed
- Epic In-Basket messaging not implemented

### Persistence
- No database persistence for workflow states
- Report status retrieval not implemented
- Workflow history not stored

### Scheduling
- Follow-up appointment scheduling is placeholder
- No integration with calendar systems

### Notifications
- SMTP email sending not implemented
- SMS notifications not implemented
- Patient portal integration needed

## Security Considerations

- Store API keys in environment variables, never in code
- Use `.gitignore` to prevent committing `.env` files
- Implement proper authentication for production API endpoints
- Follow HIPAA compliance guidelines for PHI handling
- Use secure connections (HTTPS) for all external API calls

## License

[Add your license information]

## Contributing

[Add contribution guidelines]

## Contact

[Add contact information]
