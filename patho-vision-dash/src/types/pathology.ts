export type ReportStatus = 'new' | 'analyzing' | 'plan_ready' | 'message_sent' | 'completed';

export interface PathologyReport {
  id: string;
  patientName: string;
  patientMRN: string;
  patientDOB: string;
  diagnosis: string;
  category: 'Normal' | 'Abnormal' | 'Precancerous' | 'Cancerous';
  receivedDate: string;
  status: ReportStatus;
  priority: 'routine' | 'urgent' | 'stat';
  specimenType: string;
  rawReport: string;
  structuredData?: {
    findings: string[];
    recommendations: string[];
  };
  clinicalPlan?: string;
  patientMessage?: string;
}

export interface AgentMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
}
