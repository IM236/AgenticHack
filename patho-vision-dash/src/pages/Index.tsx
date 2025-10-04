import { useState } from 'react';
import { TopBar } from '@/components/dashboard/TopBar';
import { InboxNav } from '@/components/dashboard/InboxNav';
import { ReportList } from '@/components/dashboard/ReportList';
import { ReportDetails } from '@/components/dashboard/ReportDetails';
import { mockReports } from '@/data/mockReports';
import { PathologyReport } from '@/types/pathology';
import { toast } from 'sonner';

const Index = () => {
  const [selectedCategory, setSelectedCategory] = useState('results');
  const [selectedReport, setSelectedReport] = useState<PathologyReport | null>(mockReports[0]);
  const [reports, setReports] = useState<PathologyReport[]>(mockReports);

  const handleRegeneratePlan = () => {
    toast.info('Regenerating clinical plan...', {
      description: 'AI agent is creating a new treatment plan',
    });
    
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
    
    if (selectedReport) {
      setReports(prev =>
        prev.map(r =>
          r.id === selectedReport.id
            ? { ...r, status: 'message_sent' as const }
            : r
        )
      );
      setSelectedReport(prev =>
        prev ? { ...prev, status: 'message_sent' as const } : null
      );
    }
  };

  const handleSendMessage = () => {
    toast.success('Message sent to patient', {
      description: 'Patient will receive notification',
    });
    
    if (selectedReport) {
      setReports(prev =>
        prev.map(r =>
          r.id === selectedReport.id
            ? { ...r, status: 'completed' as const }
            : r
        )
      );
      setSelectedReport(prev =>
        prev ? { ...prev, status: 'completed' as const } : null
      );
    }
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <TopBar />
      <div className="flex-1 flex overflow-hidden">
        <InboxNav
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />
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
    </div>
  );
};

export default Index;
