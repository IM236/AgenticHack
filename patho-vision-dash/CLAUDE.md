# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Pathology Vision Dashboard** - a React-based medical application for managing and reviewing pathology reports. The application features AI-powered analysis of pathology reports, automated clinical plan generation, and patient communication drafting.

**Core Purpose:** Streamline the workflow for reviewing pathology reports by providing structured data extraction, automated clinical planning, and patient messaging assistance.

## Tech Stack

- **Frontend:** React 18 + TypeScript
- **Build Tool:** Vite
- **UI Framework:** shadcn/ui components + Radix UI primitives
- **Styling:** Tailwind CSS
- **Router:** React Router v6
- **State Management:** TanStack Query (React Query)
- **Forms:** React Hook Form + Zod validation
- **Date Handling:** date-fns
- **Charts:** Recharts

## Development Commands

```bash
# Start development server (runs on http://[::]:8080)
npm run dev

# Build for production
npm run build

# Build in development mode
npm run build:dev

# Run linter
npm run lint

# Preview production build
npm run preview
```

## Environment Configuration

Create a `.env` file in the root directory (see `.env.example`):

```env
VITE_API_BASE_URL=http://localhost:8000
```

**Note:** The frontend expects the FastAPI backend to be running on port 8000. If the backend is unavailable, the app will automatically fallback to mock data.

## Architecture

### Application Structure

- **Entry Point:** `src/main.tsx` → `src/App.tsx` → `src/pages/Index.tsx`
- **Router:** BrowserRouter with catch-all NotFound route
- **Global Providers:** QueryClient, TooltipProvider, Toast notifications (Sonner + shadcn)

### Key Components

**Dashboard Layout (`src/pages/Index.tsx`):**
- Main orchestrator of the dashboard experience
- Manages report selection and status workflows
- Coordinates three main sections: TopBar, InboxNav, ReportList, and ReportDetails

**Dashboard Components (`src/components/dashboard/`):**
- `TopBar`: Application header with branding
- `InboxNav`: Left sidebar for filtering reports by category
- `ReportList`: Middle panel showing list of pathology reports
- `ReportDetails`: Main detail view with tabbed interface (Overview, Report, Plan, Message, AI Agent)
- `StatusTracker`: Visual progress indicator for report processing stages
- `AgentChat`: AI agent interaction interface

**UI Components (`src/components/ui/`):**
- shadcn/ui component library (autoconfigured via `components.json`)
- Radix UI primitives with Tailwind styling
- All components follow shadcn conventions

### Data Model

The application uses a dual-layer data model:

**Backend Data Types** (`src/types/pathology.ts`):
- `PathologyReport`: Core backend report model matching Python FastAPI schema
- `WorkflowState`: Backend LangGraph workflow state
- `ClinicalPlan`: AI-generated clinical plan
- `EpicUploadStatus`: Epic EHR upload tracking
- `PatientCommunication`: Patient messaging data

**Frontend Display Types**:
- `DashboardReport`: Extended report type combining backend data with UI-specific fields
  - Includes all backend fields (report_id, diagnosis, findings, etc.)
  - Adds UI fields (patientName, patientMRN, category, status)
  - Merges clinical_plan and patient_communication data for display

**Diagnosis Types (Backend enum):**
`benign`, `precancerous`, `cancerous`, `inconclusive`

**Workflow Steps (Backend):**
`initialized` → `extracting_data` → `processing_report` → `uploading_to_epic` → `notifying_clinician` → `creating_clinical_plan` → `communicating_with_patient` → `scheduling_follow_up` → `completed`

**UI Report Statuses (Frontend):**
`new` → `analyzing` → `plan_ready` → `message_sent` → `completed`

### API Integration

**Backend:** Python FastAPI server running on `http://localhost:8000` (configurable via `VITE_API_BASE_URL`)

**API Client** (`src/services/api.ts`):
- `PathologyApi` class with REST client methods
- Endpoints:
  - `POST /api/v1/reports/submit` - Submit new pathology reports
  - `GET /api/v1/reports/{report_id}` - Get report status
  - `GET /api/v1/reports` - List all reports
  - `POST /api/v1/workflow/test` - Test workflow with sample data
  - `GET /health` - Health check

**React Query Hooks** (`src/hooks/usePathologyApi.ts`):
- `useReports()` - Fetch all reports with auto-refetch every 10s
- `useReportStatus(reportId)` - Get specific report with polling for incomplete reports
- `useSubmitReport()` - Submit new pathology report mutation
- `useTestWorkflow()` - Test workflow mutation
- `useHealthCheck()` - API health status

**Data Transformation:**
- `transformToDashboardReport()` converts backend `WorkflowState` to `DashboardReport`
- Maps backend diagnosis types to UI categories
- Maps workflow steps to UI status indicators
- Extracts clinical plan and patient communication for display

**Fallback Mode:**
- If API is unavailable, app uses mock data from `src/data/mockReports.ts`
- Toast notification informs user of offline/online status
- Seamless transition between mock and live data

### Path Aliases

The project uses `@/*` path alias mapping to `./src/*` (configured in both `tsconfig.json` and `vite.config.ts`).

### Styling

- **Tailwind Config:** `tailwind.config.ts` with custom theme variables
- **CSS Variables:** Uses shadcn's CSS variable system for theming (see `src/index.css`)
- **Theme:** Slate base color with dark mode support via `next-themes`

## TypeScript Configuration

- Strict mode is **relaxed** for rapid development:
  - `noImplicitAny: false`
  - `strictNullChecks: false`
  - `noUnusedLocals: false`
  - `noUnusedParameters: false`
- ESLint has `@typescript-eslint/no-unused-vars` turned off

## Adding New Features

### Adding a New UI Component

Use shadcn CLI to add components:
```bash
npx shadcn@latest add [component-name]
```

Components are automatically added to `src/components/ui/` with proper configuration from `components.json`.

### Adding New Report Statuses or Categories

1. Update type definitions in `src/types/pathology.ts`
2. Update `StatusTracker` component to handle new statuses
3. Update filtering logic in `InboxNav` if adding categories

### Extending the Dashboard

The dashboard is built with a three-panel layout:
1. Left sidebar (navigation/filtering)
2. Middle panel (list view)
3. Right panel (detail view with tabs)

When adding new sections, follow the tabbed interface pattern in `ReportDetails.tsx`.

## Known Patterns

- **Toast Notifications:** Use `toast` from `sonner` for user feedback
- **Status Updates:** Reports flow through defined status transitions; React Query handles cache invalidation
- **API Polling:** Reports in progress auto-refresh every 5 seconds using React Query's `refetchInterval`
- **Data Transformation:** Always transform backend data to `DashboardReport` format in hooks, not components
- **Error Handling:** API errors automatically trigger fallback to mock data with user notification
- **Date Formatting:** Use `date-fns` `format()` function consistently

## Working with the Backend API

### Starting the Backend

The backend is a separate Python FastAPI application. To run it:

```bash
cd ../pathology-workflow-agent  # Adjust path to your backend repo
python main.py
```

The backend will start on `http://localhost:8000` with:
- API docs at `http://localhost:8000/docs`
- Health check at `http://localhost:8000/health`

### Testing API Integration

1. **Health Check:** Visit `http://localhost:8000/health` to verify backend is running
2. **Frontend Connection:** Start the frontend with `npm run dev` - you'll see a toast notification indicating connection status
3. **Submit Test Report:** Use the test workflow endpoint:
   ```bash
   curl -X POST http://localhost:8000/api/v1/workflow/test
   ```
4. **Watch Real-time Updates:** The dashboard auto-refreshes as the backend workflow progresses through steps

### Backend Data Flow

1. Frontend submits report → `POST /api/v1/reports/submit`
2. Backend LangGraph workflow executes:
   - Extract structured data (PhenoML)
   - Process report (AI agent)
   - Upload to Epic FHIR
   - Notify clinician
   - Generate clinical plan (AI agent)
   - Draft patient communication (AI agent)
   - Schedule follow-up
3. Frontend polls `GET /api/v1/reports/{report_id}` to track progress
4. When workflow completes, frontend displays all generated content

### Adding New API Endpoints

1. **Add endpoint to backend** (FastAPI)
2. **Update API client:** Add method to `PathologyApi` class in `src/services/api.ts`
3. **Create React Query hook:** Add hook in `src/hooks/usePathologyApi.ts`
4. **Use in component:** Call hook in component and handle loading/error states
