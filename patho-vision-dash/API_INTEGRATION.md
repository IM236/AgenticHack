# API Integration Guide

This document explains how the frontend integrates with the Python FastAPI backend.

## Overview

The frontend is now fully integrated with your `pathology-workflow-agent` FastAPI backend. It can:
- Fetch reports from the backend API
- Submit new pathology reports
- Track workflow progress in real-time
- Display backend-generated clinical plans and patient messages
- Fallback to mock data if backend is unavailable

## Architecture

### Backend (Python FastAPI)
- **Location:** `../pathology-workflow-agent/`
- **Port:** `http://localhost:8000`
- **Tech:** FastAPI + LangGraph + OpenAI + PhenoML

### Frontend (React + TypeScript)
- **Location:** Current directory
- **Port:** `http://[::]:8080`
- **Tech:** React + Vite + TanStack Query

## Data Model Mapping

### Backend → Frontend Type Mapping

| Backend Type (Python) | Frontend Type (TypeScript) | Purpose |
|----------------------|---------------------------|---------|
| `PathologyReport` | `PathologyReport` | Core report data from backend |
| `WorkflowState` | `WorkflowState` | LangGraph workflow tracking |
| `ClinicalPlan` | `ClinicalPlan` | AI-generated clinical plan |
| `EpicUploadStatus` | `EpicUploadStatus` | Epic EHR integration status |
| `PatientCommunication` | `PatientCommunication` | Patient messaging |
| N/A | `DashboardReport` | **UI-specific** extended type |

### DashboardReport Structure

The `DashboardReport` type combines backend data with UI-specific fields:

```typescript
interface DashboardReport {
  // Backend fields (from PathologyReport)
  report_id: string;
  patient_id: string;
  pathologist_id: string;
  tissue_sample_id: string;
  diagnosis: 'benign' | 'precancerous' | 'cancerous' | 'inconclusive';
  findings: string;
  recommendations?: string;
  created_at: string;
  raw_text?: string;

  // Backend workflow state
  current_step: WorkflowStep;
  clinical_plan?: ClinicalPlan;
  epic_status?: EpicUploadStatus;

  // UI-specific fields
  patientName: string;
  patientMRN: string;
  patientDOB: string;
  category: 'Normal' | 'Abnormal' | 'Precancerous' | 'Cancerous';
  status: 'new' | 'analyzing' | 'plan_ready' | 'message_sent' | 'completed';
  priority: 'routine' | 'urgent' | 'stat';
  specimenType: string;
  receivedDate: string;
  structuredData?: {
    findings: string[];
    recommendations: string[];
  };
  clinicalPlanText?: string;
  patientMessageText?: string;
}
```

## API Endpoints

### Implemented Endpoints

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| POST | `/api/v1/reports/submit` | Submit new report | ✅ Implemented |
| GET | `/api/v1/reports/{report_id}` | Get report status | ✅ Implemented |
| GET | `/api/v1/reports` | List all reports | ⚠️ Needs backend implementation |
| POST | `/api/v1/workflow/test` | Test workflow | ✅ Implemented |
| GET | `/health` | Health check | ✅ Implemented |

### Missing Backend Endpoints

The frontend is ready to consume these endpoints, but they need to be implemented in the backend:

1. **`GET /api/v1/reports`** - List all reports
   - Should return array of `GetReportStatusResponse`
   - Frontend will poll this every 10 seconds for updates

## React Query Hooks

### Available Hooks

```typescript
// Fetch all reports (auto-refetch every 10s)
const { data: reports, isLoading, isError } = useReports();

// Fetch specific report (auto-refetch every 5s if not completed)
const { data: report } = useReportStatus(reportId);

// Submit new report
const submitMutation = useSubmitReport();
submitMutation.mutate({
  patient_id: 'patient_123',
  raw_report_text: 'SPECIMEN: ...'
});

// Test workflow
const testMutation = useTestWorkflow();
testMutation.mutate();

// Health check (auto-refetch every 30s)
const { data: health } = useHealthCheck();
```

## Setup Instructions

### 1. Configure Environment

Create `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 2. Start Backend

```bash
cd ../pathology-workflow-agent
source .venv/bin/activate  # or activate your venv
python main.py
```

Backend should start on `http://localhost:8000`

### 3. Start Frontend

```bash
npm run dev
```

Frontend will start on `http://[::]:8080`

### 4. Verify Connection

1. Open frontend in browser
2. Check for toast notification:
   - ✅ Green: "Connected to backend" - API is working
   - ⚠️ Yellow: "Using offline mode" - API unavailable, using mock data

## Data Flow

### Report Submission Flow

```
1. User action (frontend)
   ↓
2. useSubmitReport() hook
   ↓
3. POST /api/v1/reports/submit
   ↓
4. Backend LangGraph workflow starts
   ↓
5. Frontend polls GET /api/v1/reports/{id} every 5s
   ↓
6. Backend workflow progresses through steps:
   - extracting_data
   - processing_report
   - uploading_to_epic
   - notifying_clinician
   - creating_clinical_plan
   - communicating_with_patient
   - scheduling_follow_up
   - completed
   ↓
7. Frontend updates UI in real-time
   ↓
8. Workflow completes, polling stops
```

### Workflow Step → UI Status Mapping

| Backend Workflow Step | Frontend Status | UI Label |
|----------------------|-----------------|----------|
| `initialized` | `new` | New |
| `extracting_data`, `processing_report`, `uploading_to_epic` | `analyzing` | Analyzing |
| `notifying_clinician`, `creating_clinical_plan` | `plan_ready` | Plan Ready |
| `communicating_with_patient` | `message_sent` | Message Sent |
| `scheduling_follow_up`, `completed` | `completed` | Completed |

### Diagnosis → Category Mapping

| Backend Diagnosis | Frontend Category |
|------------------|-------------------|
| `benign` | Normal |
| `precancerous` | Precancerous |
| `cancerous` | Cancerous |
| `inconclusive` | Abnormal |

## Fallback Behavior

The frontend gracefully handles backend unavailability:

1. **On mount:** Frontend tries to fetch reports from API
2. **If API fails:**
   - Shows warning toast: "Using offline mode"
   - Falls back to mock data from `src/data/mockReports.ts`
   - All UI features remain functional
3. **If API succeeds:**
   - Shows success toast: "Connected to backend"
   - Uses real-time data
   - Enables auto-refresh polling

## Development Workflow

### Adding a New Feature

1. **Define Backend Schema** (Python Pydantic models)
2. **Update Frontend Types** (`src/types/pathology.ts`)
3. **Add API Client Method** (`src/services/api.ts`)
4. **Create React Query Hook** (`src/hooks/usePathologyApi.ts`)
5. **Use in Component** (call hook, handle states)

### Example: Adding Report Approval

**Backend (FastAPI):**
```python
@app.post("/api/v1/reports/{report_id}/approve")
async def approve_report(report_id: str):
    # Implementation
    return {"status": "approved"}
```

**Frontend Types:**
```typescript
// src/types/pathology.ts
export interface ApproveReportResponse {
  status: string;
}
```

**API Client:**
```typescript
// src/services/api.ts
async approveReport(reportId: string): Promise<ApproveReportResponse> {
  return this.request(`/api/v1/reports/${reportId}/approve`, {
    method: 'POST',
  });
}
```

**React Query Hook:**
```typescript
// src/hooks/usePathologyApi.ts
export function useApproveReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (reportId: string) => pathologyApi.approveReport(reportId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports'] });
    },
  });
}
```

**Component Usage:**
```typescript
// In component
const approveMutation = useApproveReport();

const handleApprove = () => {
  approveMutation.mutate(reportId);
};
```

## Troubleshooting

### Issue: "Using offline mode" toast appears

**Causes:**
1. Backend not running
2. Wrong API URL in `.env`
3. CORS issues
4. Network connectivity

**Solutions:**
1. Start backend: `cd ../pathology-workflow-agent && python main.py`
2. Verify `.env`: `VITE_API_BASE_URL=http://localhost:8000`
3. Check backend CORS settings (should allow `http://[::]:8080`)
4. Check browser console for errors

### Issue: Reports not updating

**Causes:**
1. Polling stopped (report marked as completed)
2. Backend workflow stuck
3. API rate limiting

**Solutions:**
1. Check `current_step` in backend response
2. Check backend logs for errors
3. Adjust `refetchInterval` in hooks if needed

### Issue: Type mismatches

**Causes:**
1. Backend schema changed
2. Frontend types out of sync

**Solutions:**
1. Review backend Pydantic models
2. Update TypeScript types in `src/types/pathology.ts`
3. Update transformation logic in `usePathologyApi.ts`

## Production Considerations

### Environment Variables

Development:
```env
VITE_API_BASE_URL=http://localhost:8000
```

Production:
```env
VITE_API_BASE_URL=https://api.your-domain.com
```

### CORS Configuration

Backend must allow frontend origin:
```python
# In FastAPI backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://[::]:8080", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication

Currently, the API has no authentication. For production:

1. Add auth to backend (OAuth2, JWT, API keys)
2. Update API client to include auth headers
3. Implement token refresh logic
4. Add login/logout flows

## Next Steps

1. **Implement Missing Backend Endpoint:**
   - Add `GET /api/v1/reports` to list all reports

2. **Add Real-time Updates:**
   - Consider WebSocket connection for live updates
   - Replace polling with push notifications

3. **Implement Report Submission UI:**
   - Add form to submit new pathology reports
   - Use `useSubmitReport()` hook

4. **Add Error Handling:**
   - Display user-friendly error messages
   - Implement retry logic for failed requests

5. **Add Authentication:**
   - Implement login system
   - Secure API endpoints
   - Handle token management

6. **Optimize Performance:**
   - Implement virtual scrolling for large report lists
   - Add pagination to API endpoints
   - Cache transformed data
