import { DashboardReport } from '@/types/pathology';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { formatDistanceToNow } from 'date-fns';
import { Clock, AlertCircle } from 'lucide-react';

interface ReportListProps {
  reports: DashboardReport[];
  selectedReport: DashboardReport | null;
  onSelectReport: (report: DashboardReport) => void;
}

const getStatusBadge = (status: DashboardReport['status']) => {
  const statusConfig = {
    new: { label: 'New', className: 'bg-primary text-primary-foreground' },
    analyzing: { label: 'Analyzing', className: 'bg-warning text-warning-foreground' },
    plan_ready: { label: 'Plan Ready', className: 'bg-success text-success-foreground' },
    message_sent: { label: 'Message Sent', className: 'bg-accent text-accent-foreground' },
    completed: { label: 'Completed', className: 'bg-muted text-muted-foreground' },
  };
  
  const config = statusConfig[status];
  return <Badge className={config.className}>{config.label}</Badge>;
};

const getCategoryColor = (category: DashboardReport['category']) => {
  const colors = {
    Normal: 'text-success',
    Abnormal: 'text-warning',
    Precancerous: 'text-destructive',
    Cancerous: 'text-destructive font-semibold',
  };
  return colors[category];
};

export const ReportList = ({ reports, selectedReport, onSelectReport }: ReportListProps) => {
  return (
    <div className="w-96 border-r bg-background h-full overflow-y-auto">
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-foreground">Recent Reports</h2>
          <span className="text-xs text-muted-foreground">{reports.length} items</span>
        </div>
        
        <div className="space-y-2">
          {reports.map((report) => (
            <button
              key={report.report_id}
              onClick={() => onSelectReport(report)}
              className={cn(
                'w-full text-left p-3 rounded-lg border transition-all',
                selectedReport?.report_id === report.report_id
                  ? 'bg-accent border-primary shadow-sm'
                  : 'bg-card hover:bg-accent hover:border-border'
              )}
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <div>
                  <h3 className="font-semibold text-sm text-foreground">{report.patientName}</h3>
                  <p className="text-xs text-muted-foreground">MRN: {report.patientMRN}</p>
                </div>
                {getStatusBadge(report.status)}
              </div>
              
              <div className="space-y-1">
                <p className={cn('text-sm font-medium', getCategoryColor(report.category))}>
                  {report.diagnosis}
                </p>
                <p className="text-xs text-muted-foreground">{report.specimenType}</p>
              </div>
              
              <div className="flex items-center justify-between mt-2 pt-2 border-t">
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Clock className="h-3 w-3" />
                  {formatDistanceToNow(new Date(report.receivedDate), { addSuffix: true })}
                </div>
                {report.priority === 'stat' || report.priority === 'urgent' ? (
                  <div className="flex items-center gap-1 text-xs text-destructive">
                    <AlertCircle className="h-3 w-3" />
                    {report.priority.toUpperCase()}
                  </div>
                ) : null}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
