import { useState } from 'react';
import { TopBar } from '@/components/dashboard/TopBar';
import { InboxNav } from '@/components/dashboard/InboxNav';
import { ReportList } from '@/components/dashboard/ReportList';
import { ReportDetails } from '@/components/dashboard/ReportDetails';
import { mockReports } from '@/data/mockReports';
import { DashboardReport } from '@/types/pathology';
import { toast } from 'sonner';
import { useReports } from '@/hooks/usePathologyApi';

const Index = () => {
  const [selectedCategory, setSelectedCategory] = useState('results');
  const [selectedReport, setSelectedReport] = useState<DashboardReport | null>(null);

  // Fetch reports from API with fallback to mock data
  const { data: apiReports, isLoading, isError } = useReports();

  // Use API data if available, otherwise fallback to mock data
  const reports = apiReports && apiReports.length > 0 ? apiReports : mockReports;

  // Show connection status on mount
  useState(() => {
    if (isError) {
      toast.warning('Using offline mode', {
        description: 'Could not connect to backend API. Showing demo data.',
      });
    } else if (apiReports && apiReports.length > 0) {
      toast.success('Connected to backend', {
        description: 'Real-time data loading enabled.',
      });
    }
  });

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
        {isLoading ? (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            Loading reports...
          </div>
        ) : (
          <>
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
          </>
        )}
      </div>
    </div>
  );
};

export default Index;
