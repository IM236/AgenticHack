import { useState } from 'react';
import { TopBar } from '@/components/dashboard/TopBar';
import { InboxNav } from '@/components/dashboard/InboxNav';
import { ReportList } from '@/components/dashboard/ReportList';
import { ReportDetails } from '@/components/dashboard/ReportDetails';
import { DashboardReport } from '@/types/pathology';
import { toast } from 'sonner';
import { useReports } from '@/hooks/usePathologyApi';
import { RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Index = () => {
  const [selectedCategory, setSelectedCategory] = useState('results');
  const [selectedReport, setSelectedReport] = useState<DashboardReport | null>(null);

  // Fetch reports from API
  const { data: apiReports, isLoading, isError, refetch } = useReports();

  const reports = apiReports || [];

  const handleRefresh = async () => {
    toast.info('Refreshing reports...');
    await refetch();
    toast.success('Reports refreshed');
  };

  const handleRegeneratePlan = () => {
    toast.info('Regenerating clinical plan...', {
      description: 'AI agent is creating a new treatment plan',
    });

    // TODO: Call API to regenerate plan
    setTimeout(() => {
      toast.success('Clinical plan regenerated', {
        description: 'Review the updated recommendations',
      });
    }, 2000);
  };

  const handleApprovePlan = () => {
    toast.success('Clinical plan approved', {
      description: 'Plan has been added to patient record',
    });

    // TODO: Update via API
    if (selectedReport) {
      const updatedReport = { ...selectedReport, status: 'message_sent' as const };
      setSelectedReport(updatedReport);
    }
  };

  const handleSendMessage = () => {
    toast.success('Message sent to patient', {
      description: 'Patient will receive notification',
    });

    // TODO: Send via API
    if (selectedReport) {
      const updatedReport = { ...selectedReport, status: 'completed' as const };
      setSelectedReport(updatedReport);
    }
  };

  // Update selected report when reports change
  useState(() => {
    if (selectedReport && reports) {
      const updated = reports.find(r => r.report_id === selectedReport.report_id);
      if (updated) {
        setSelectedReport(updated);
      }
    }
  });

  return (
    <div className="h-screen flex flex-col bg-background">
      <TopBar />
      <div className="flex-1 flex overflow-hidden">
        <InboxNav
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />
        <div className="flex flex-col flex-1">
          <div className="p-4 border-b flex items-center justify-between">
            <h2 className="text-lg font-semibold">Reports</h2>
            <Button onClick={handleRefresh} variant="outline" size="sm" disabled={isLoading}>
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
          {isLoading ? (
            <div className="flex-1 flex items-center justify-center text-muted-foreground">
              Loading reports...
            </div>
          ) : isError ? (
            <div className="flex-1 flex items-center justify-center text-destructive">
              Failed to load reports. Click refresh to try again.
            </div>
          ) : (
            <div className="flex-1 flex overflow-hidden">
              <ReportList
                reports={reports}
                selectedReport={selectedReport}
                onSelectReport={setSelectedReport}
              />
              {selectedReport ? (
                <ReportDetails
                  report={selectedReport}
                  onRegeneratePlan={handleRegeneratePlan}
                  onApprovePlan={handleApprovePlan}
                  onSendMessage={handleSendMessage}
                />
              ) : (
                <div className="flex-1 flex items-center justify-center text-muted-foreground">
                  Select a report to view details
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Index;
