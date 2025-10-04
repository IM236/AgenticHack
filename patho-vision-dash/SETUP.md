# Quick Setup Guide

## Prerequisites

- Node.js >= 18
- npm or yarn
- Python 3.12+ (for backend)
- FastAPI backend running on port 8000

## Frontend Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

Frontend will be available at: `http://[::]:8080`

## Backend Setup

The frontend expects the FastAPI backend to be running.

### 1. Navigate to Backend Directory

```bash
cd ../pathology-workflow-agent
```

### 2. Activate Virtual Environment

```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### 3. Start Backend

```bash
python main.py
```

Backend will be available at: `http://localhost:8000`

- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Verify Integration

1. Open frontend in browser: `http://[::]:8080`
2. Check for toast notification:
   - ✅ **Green:** "Connected to backend" - API is working
   - ⚠️ **Yellow:** "Using offline mode" - API unavailable, showing demo data

## Testing the API

### Health Check

```bash
curl http://localhost:8000/health
```

### Submit Test Report

```bash
curl -X POST http://localhost:8000/api/v1/workflow/test
```

### Submit Custom Report

```bash
curl -X POST http://localhost:8000/api/v1/reports/submit \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "patient_test_001",
    "raw_report_text": "SPECIMEN: Colon biopsy\nDIAGNOSIS: Normal mucosa"
  }'
```

## Development Workflow

1. Start backend: `cd ../pathology-workflow-agent && python main.py`
2. Start frontend: `npm run dev`
3. Open browser: `http://[::]:8080`
4. Make changes - hot reload is enabled
5. Submit reports via API or UI

## Troubleshooting

### "Using offline mode" message

**Problem:** Frontend can't connect to backend

**Solutions:**
1. Verify backend is running on port 8000
2. Check `.env` file has correct API URL
3. Verify no firewall blocking localhost:8000
4. Check backend logs for startup errors

### Type errors during build

**Problem:** TypeScript type mismatches

**Solutions:**
1. Run `npm run lint` to see errors
2. Check backend schema matches frontend types
3. Update `src/types/pathology.ts` if backend changed

### Reports not updating

**Problem:** Dashboard not showing new reports

**Solutions:**
1. Check browser console for errors
2. Verify backend `/api/v1/reports` endpoint exists
3. Check React Query DevTools (if installed)
4. Hard refresh browser (Cmd/Ctrl + Shift + R)

## Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

Build output will be in `dist/` directory.

## Environment Variables

### Development
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Production
```env
VITE_API_BASE_URL=https://api.your-domain.com
```

**Note:** Environment variables must be prefixed with `VITE_` to be accessible in the frontend.

## Next Steps

- [ ] Implement `GET /api/v1/reports` endpoint in backend
- [ ] Add report submission UI
- [ ] Implement authentication
- [ ] Add WebSocket for real-time updates
- [ ] Configure production deployment

## Documentation

- **CLAUDE.md** - Development guide for future Claude Code sessions
- **API_INTEGRATION.md** - Detailed API integration documentation
- **README.md** - Project overview and Lovable deployment info
