# Backend Requirements for Frontend Integration

## Summary

The frontend now has:
1. ✅ API client methods for approval/rejection
2. ✅ React Query hooks for approval workflow
3. ✅ UI component (`ApprovalActions`) with checkboxes for approval
4. ✅ TypeScript types matching expected backend schema

## Required Backend Endpoints

### 1. Physician Approval Endpoint

**POST `/api/v1/reports/{report_id}/approve`**

Request body:
```json
{
  "report_id": "string",
  "approve_clinical_plan": boolean,
  "approve_patient_message": boolean,
  "revision_notes": "string (optional)"
}
```

Response:
```json
{
  "success": true,
  "review": {
    "review_id": "uuid",
    "report_id": "uuid",
    "physician_id": "string",
    "physician_name": "string",
    "approval_status": "approved" | "pending" | "rejected" | "needs_revision",
    "clinical_plan_approved": boolean,
    "patient_message_approved": boolean,
    "revision_notes": "string (optional)",
    "reviewed_at": "ISO datetime"
  },
  "message": "Report approved successfully"
}
```

### 2. Rejection Endpoint

**POST `/api/v1/reports/{report_id}/reject`**

Request body:
```json
{
  "revision_notes": "string (required)"
}
```

Response: Same as approve endpoint but with `approval_status: "rejected"`

### 3. DeepL Translation Integration

The backend should:
1. **Translate patient messages to Spanish** after generation
2. **Simplify text for patient-friendly language** using DeepL Write API

Expected workflow:
```python
# After generating patient message with GPT-5
message = patient_communicator.generate_patient_message(...)

# Translate to Spanish
spanish_message = deepl_service.translate(
    text=message.message_content,
    target_lang="ES",
    formality="less"  # Informal tone for patients
)

# Simplify English version for readability
simplified_message = deepl_service.simplify(
    text=message.message_content,
    target_lang="EN-US"
)

# Store both versions
message.message_content_english = simplified_message
message.message_content_spanish = spanish_message
```

### 4. Update PatientCommunication Model

Add fields to `src/schemas/models.py`:

```python
class PatientCommunication(BaseModel):
    communication_id: str
    patient_id: str
    report_id: str
    message_type: str
    message_content: str  # Original GPT-5 output
    message_content_english: Optional[str] = None  # DeepL simplified
    message_content_spanish: Optional[str] = None  # DeepL translated
    sent_at: Optional[datetime] = None
    delivery_status: str
```

### 5. Create DeepL Service

Create `src/services/deepl_service.py`:

```python
import deepl
from src.config import settings

class DeepLService:
    def __init__(self):
        self.client = deepl.Translator(settings.deepl_api_key)

    def translate_to_spanish(self, text: str) -> str:
        """Translate text to Spanish."""
        result = self.client.translate_text(
            text,
            target_lang="ES",
            formality="less"
        )
        return result.text

    def simplify_text(self, text: str) -> str:
        """Simplify text for patient readability."""
        result = self.client.rephrase_text(
            text,
            target_lang="EN-US",
            style=deepl.WritingStyle.SIMPLE.value
        )
        return result.text

deepl_service = DeepLService()
```

### 6. Update Workflow to Include DeepL

In `src/workflows/pathology_workflow.py`, update `_communicate_with_patient`:

```python
async def _communicate_with_patient(self, state):
    # Generate message with GPT-5
    communication = await patient_communicator.generate_patient_message(...)

    # Simplify and translate
    from src.services.deepl_service import deepl_service

    communication.message_content_english = await asyncio.to_thread(
        deepl_service.simplify_text,
        communication.message_content
    )

    communication.message_content_spanish = await asyncio.to_thread(
        deepl_service.translate_to_spanish,
        communication.message_content
    )

    state["patient_communication"] = communication.model_dump()
    return state
```

## Frontend Display Updates Needed

Once backend adds DeepL translations, update frontend to show both versions:

```typescript
// In ReportDetails.tsx "Patient Message" tab
<Tabs>
  <TabsList>
    <TabsTrigger value="english">English (Simplified)</TabsTrigger>
    <TabsTrigger value="spanish">Spanish</TabsTrigger>
  </TabsList>
  <TabsContent value="english">
    {report.patient_communication?.message_content_english}
  </TabsContent>
  <TabsContent value="spanish">
    {report.patient_communication?.message_content_spanish}
  </TabsContent>
</Tabs>
```

## Environment Variables

Add to `.env`:
```env
DEEPL_API_KEY=your-deepl-api-key
```

Add to `src/config.py`:
```python
class Settings(BaseSettings):
    deepl_api_key: str
    # ... other settings
```

## Testing Checklist

- [ ] Backend: Implement approval endpoints
- [ ] Backend: Create DeepL service
- [ ] Backend: Update PatientCommunication model
- [ ] Backend: Integrate DeepL into workflow
- [ ] Backend: Add deepl library (`uv add deepl`)
- [ ] Frontend: Test approval workflow UI
- [ ] Frontend: Add language tabs for patient messages
- [ ] Integration: Test end-to-end physician approval flow
- [ ] Integration: Verify Spanish translations display correctly
