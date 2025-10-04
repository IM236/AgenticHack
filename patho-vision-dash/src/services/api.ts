/**
 * API client for pathology workflow backend
 */
import { env } from '@/config/env';
import {
  SubmitReportRequest,
  SubmitReportResponse,
  GetReportStatusResponse,
  WorkflowState,
  ApproveRequest,
  ApproveResponse,
} from '@/types/pathology';

class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

class PathologyApi {
  private baseUrl: string;

  constructor(baseUrl: string = env.apiBaseUrl) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new ApiError(
        errorData?.message || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    return response.json();
  }

  /**
   * Submit a new pathology report for processing
   */
  async submitReport(data: SubmitReportRequest): Promise<SubmitReportResponse> {
    return this.request<SubmitReportResponse>('/api/v1/reports/submit', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Get report status by report ID
   */
  async getReportStatus(reportId: string): Promise<GetReportStatusResponse> {
    return this.request<GetReportStatusResponse>(`/api/v1/reports/${reportId}`);
  }

  /**
   * Test workflow with sample data
   */
  async testWorkflow(): Promise<WorkflowState> {
    return this.request<WorkflowState>('/api/v1/workflow/test', {
      method: 'POST',
    });
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>('/health');
  }

  /**
   * List all reports (if backend implements this endpoint)
   */
  async listReports(): Promise<GetReportStatusResponse[]> {
    return this.request<GetReportStatusResponse[]>('/api/v1/reports');
  }

  /**
   * Approve or reject clinical plan and patient message
   */
  async approveReport(data: ApproveRequest): Promise<ApproveResponse> {
    return this.request<ApproveResponse>(`/api/v1/reports/${data.report_id}/approve`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Reject report with revision notes
   */
  async rejectReport(reportId: string, revisionNotes: string): Promise<ApproveResponse> {
    return this.request<ApproveResponse>(`/api/v1/reports/${reportId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ revision_notes: revisionNotes }),
    });
  }
}

// Export singleton instance
export const pathologyApi = new PathologyApi();
export { ApiError };
