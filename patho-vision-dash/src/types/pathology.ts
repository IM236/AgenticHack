/**
 * Frontend types matching backend schemas
 */

// Backend DiagnosisType enum
export type DiagnosisType = 'benign' | 'precancerous' | 'cancerous' | 'inconclusive';

// Workflow status types (derived from backend workflow steps)
export type WorkflowStep =
  | 'initialized'
  | 'extracting_data'
  | 'processing_report'
  | 'uploading_to_epic'
  | 'notifying_clinician'
  | 'creating_clinical_plan'
  | 'communicating_with_patient'
  | 'scheduling_follow_up'
  | 'completed'
  | 'error';

// UI-specific status for display
export type ReportStatus = 'new' | 'analyzing' | 'plan_ready' | 'message_sent' | 'completed';

// Backend PathologyReport model
export interface PathologyReport {
  report_id: string;
  patient_id: string;
  pathologist_id: string;
  tissue_sample_id: string;
  diagnosis: DiagnosisType;
  findings: string;
  recommendations?: string;
  created_at: string; // ISO datetime string
  raw_text?: string;
  extracted_data?: Record<string, unknown>;
}

// Backend EpicUploadStatus model
export interface EpicUploadStatus {
  report_id: string;
  epic_document_id?: string;
  status: 'uploaded' | 'failed' | 'pending';
  uploaded_at?: string; // ISO datetime string
  error_message?: string;
}

// Backend ClinicalPlan model
export interface ClinicalPlan {
  plan_id: string;
  report_id: string;
  patient_id: string;
  clinician_id: string;
  diagnosis: DiagnosisType;
  treatment_plan: string;
  follow_up_actions: string[];
  urgency_level: 'routine' | 'urgent' | 'emergency';
  created_at: string; // ISO datetime string
}

// Backend PatientCommunication model
export interface PatientCommunication {
  communication_id: string;
  patient_id: string;
  report_id: string;
  message_type: 'email' | 'portal' | 'phone';
  message_content: string;
  sent_at?: string; // ISO datetime string
  delivery_status: 'sent' | 'delivered' | 'failed';
}

// Backend WorkflowState model
export interface WorkflowState {
  report_id: string;
  patient_id: string;
  pathology_report?: PathologyReport;
  epic_status?: EpicUploadStatus;
  notification_sent: boolean;
  clinical_plan?: ClinicalPlan;
  patient_notified: boolean;
  follow_up_scheduled: boolean;
  error?: string;
  current_step: WorkflowStep;
}

// UI-specific extended report type for dashboard display
export interface DashboardReport {
  // Core backend data
  report_id: string;
  patient_id: string;
  pathologist_id: string;
  tissue_sample_id: string;
  diagnosis: DiagnosisType;
  findings: string;
  recommendations?: string;
  created_at: string;
  raw_text?: string;
  extracted_data?: Record<string, unknown>;

  // Workflow state
  current_step: WorkflowStep;
  epic_status?: EpicUploadStatus;
  clinical_plan?: ClinicalPlan;
  patient_communication?: PatientCommunication;

  // UI-specific fields
  patientName: string;
  patientMRN: string;
  patientDOB: string;
  category: 'Normal' | 'Abnormal' | 'Precancerous' | 'Cancerous';
  status: ReportStatus;
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

// API Request/Response types
export interface SubmitReportRequest {
  patient_id: string;
  raw_report_text: string;
}

export interface SubmitReportResponse {
  workflow_id: string;
  status: string;
  message: string;
  data: {
    report_id: string;
    current_step: WorkflowStep;
    diagnosis?: DiagnosisType;
    epic_uploaded: boolean;
    clinician_notified: boolean;
    patient_communicated: boolean;
    follow_up_scheduled: boolean;
  };
}

export interface GetReportStatusResponse {
  report_id: string;
  workflow_state: WorkflowState;
}

export interface AgentMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
}

// Physician approval workflow
export type ApprovalStatus = 'pending' | 'approved' | 'rejected' | 'needs_revision';

export interface PhysicianReview {
  review_id: string;
  report_id: string;
  physician_id: string;
  physician_name: string;
  approval_status: ApprovalStatus;
  clinical_plan_approved: boolean;
  patient_message_approved: boolean;
  revision_notes?: string;
  reviewed_at: string;
}

export interface ApproveRequest {
  report_id: string;
  approve_clinical_plan: boolean;
  approve_patient_message: boolean;
  revision_notes?: string;
}

export interface ApproveResponse {
  success: boolean;
  review: PhysicianReview;
  message: string;
}
