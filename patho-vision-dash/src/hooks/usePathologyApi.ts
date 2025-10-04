/**
 * React Query hooks for pathology API
 */
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { pathologyApi } from '@/services/api';
import {
  SubmitReportRequest,
  GetReportStatusResponse,
  DashboardReport,
  ApproveRequest,
} from '@/types/pathology';

/**
 * Transform backend WorkflowState to DashboardReport for UI
 */
function transformToDashboardReport(
  response: GetReportStatusResponse
): DashboardReport | null {
  const { workflow_state } = response;
  const report = workflow_state.pathology_report;

  if (!report) return null;

  // Map diagnosis to category
  const categoryMap = {
    benign: 'Normal',
    precancerous: 'Precancerous',
    cancerous: 'Cancerous',
    inconclusive: 'Abnormal',
  } as const;

  // Map workflow step to UI status
  const getStatus = (step: string) => {
    if (step === 'completed') return 'completed';
    if (step === 'communicating_with_patient' || step === 'scheduling_follow_up')
      return 'message_sent';
    if (step === 'creating_clinical_plan') return 'plan_ready';
    if (step === 'processing_report' || step === 'uploading_to_epic') return 'analyzing';
    return 'new';
  };

  // Extract patient info from patient_id (in real app, fetch from patient service)
  const patientInfo = extractPatientInfo(workflow_state.patient_id);

  return {
    // Backend fields
    report_id: report.report_id,
    patient_id: report.patient_id,
    pathologist_id: report.pathologist_id,
    tissue_sample_id: report.tissue_sample_id,
    diagnosis: report.diagnosis,
    findings: report.findings,
    recommendations: report.recommendations,
    created_at: report.created_at,
    raw_text: report.raw_text,
    extracted_data: report.extracted_data,

    // Workflow state
    current_step: workflow_state.current_step,
    epic_status: workflow_state.epic_status,
    clinical_plan: workflow_state.clinical_plan,
    patient_communication: undefined, // Not in workflow state yet

    // UI fields
    patientName: patientInfo.name,
    patientMRN: patientInfo.mrn,
    patientDOB: patientInfo.dob,
    category: categoryMap[report.diagnosis],
    status: getStatus(workflow_state.current_step),
    priority: workflow_state.clinical_plan?.urgency_level === 'emergency'
      ? 'stat'
      : workflow_state.clinical_plan?.urgency_level === 'urgent'
      ? 'urgent'
      : 'routine',
    specimenType: report.tissue_sample_id.split('_')[0] || 'Specimen',
    receivedDate: report.created_at,
    structuredData: {
      findings: parseFindingsToArray(report.findings),
      recommendations: report.recommendations
        ? parseRecommendationsToArray(report.recommendations)
        : [],
    },
    clinicalPlanText: workflow_state.clinical_plan?.treatment_plan,
    patientMessageText: undefined, // Will be added when communication is tracked
  };
}

// Helper to extract patient info (placeholder - should call patient service)
function extractPatientInfo(patientId: string) {
  return {
    name: `Patient ${patientId.slice(-6)}`,
    mrn: `MRN-${patientId.slice(-5)}`,
    dob: '1970-01-01',
  };
}

// Helper to parse findings string to array
function parseFindingsToArray(findings: string): string[] {
  return findings
    .split(/\n|;/)
    .map((f) => f.trim())
    .filter(Boolean);
}

// Helper to parse recommendations string to array
function parseRecommendationsToArray(recommendations: string): string[] {
  return recommendations
    .split(/\n|;/)
    .map((r) => r.trim())
    .filter(Boolean);
}

/**
 * Hook to submit a new pathology report
 */
export function useSubmitReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: SubmitReportRequest) => pathologyApi.submitReport(data),
    onSuccess: () => {
      // Invalidate reports list to refetch
      queryClient.invalidateQueries({ queryKey: ['reports'] });
    },
  });
}

/**
 * Hook to get a specific report by ID
 * No auto-refetch - only manual refresh
 */
export function useReportStatus(reportId: string | null) {
  return useQuery({
    queryKey: ['report', reportId],
    queryFn: () => pathologyApi.getReportStatus(reportId!),
    enabled: !!reportId,
    refetchInterval: false, // Disabled auto-refetch
    refetchOnWindowFocus: false,
  });
}

/**
 * Hook to get all reports (transforms to DashboardReport format)
 * No auto-refetch - only manual refresh via button
 */
export function useReports() {
  return useQuery({
    queryKey: ['reports'],
    queryFn: async () => {
      const reports = await pathologyApi.listReports();
      return reports
        .map(transformToDashboardReport)
        .filter((r): r is DashboardReport => r !== null);
    },
    refetchInterval: false, // Disabled auto-refetch
    refetchOnWindowFocus: false, // Don't refetch on window focus
  });
}

/**
 * Hook to test workflow
 */
export function useTestWorkflow() {
  return useMutation({
    mutationFn: () => pathologyApi.testWorkflow(),
  });
}

/**
 * Hook to check API health
 */
export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => pathologyApi.healthCheck(),
    refetchInterval: 30000, // Check every 30 seconds
  });
}

/**
 * Hook to approve clinical plan and patient message
 */
export function useApproveReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ApproveRequest) => pathologyApi.approveReport(data),
    onSuccess: (_, variables) => {
      // Invalidate reports list and specific report
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      queryClient.invalidateQueries({ queryKey: ['report', variables.report_id] });
    },
  });
}

/**
 * Hook to reject report with revision notes
 */
export function useRejectReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ reportId, revisionNotes }: { reportId: string; revisionNotes: string }) =>
      pathologyApi.rejectReport(reportId, revisionNotes),
    onSuccess: (_, variables) => {
      // Invalidate reports list and specific report
      queryClient.invalidateQueries({ queryKey: ['reports'] });
      queryClient.invalidateQueries({ queryKey: ['report', variables.reportId] });
    },
  });
}
