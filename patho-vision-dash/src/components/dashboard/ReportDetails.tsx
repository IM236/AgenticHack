import { useState } from 'react';
import { DashboardReport } from '@/types/pathology';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { FileText, User, Calendar, Activity, CheckCircle, Send, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';
import { StatusTracker } from './StatusTracker';
import { AgentChat } from './AgentChat';

interface ReportDetailsProps {
  report: DashboardReport;
  onRegeneratePlan: () => void;
  onApprovePlan: () => void;
  onSendMessage: () => void;
}

export const ReportDetails = ({ report, onRegeneratePlan, onApprovePlan, onSendMessage }: ReportDetailsProps) => {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="flex-1 h-full overflow-hidden flex flex-col">
      {/* Header */}
      <div className="p-6 border-b bg-card">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold text-foreground mb-1">{report.patientName}</h2>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <User className="h-4 w-4" />
                MRN: {report.patientMRN}
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                DOB: {format(new Date(report.patientDOB), 'MM/dd/yyyy')}
              </span>
              <span className="flex items-center gap-1">
                <Activity className="h-4 w-4" />
                {report.specimenType}
              </span>
            </div>
          </div>
          <Badge variant={report.category === 'Normal' ? 'default' : 'destructive'}>
            {report.category}
          </Badge>
        </div>
        
        <StatusTracker status={report.status} className="mt-4" />
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="mb-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="report">Report Details</TabsTrigger>
            <TabsTrigger value="plan">Clinical Plan</TabsTrigger>
            <TabsTrigger value="message">Patient Message</TabsTrigger>
            <TabsTrigger value="agent">AI Agent</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Diagnosis Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg font-semibold text-foreground mb-2">{report.diagnosis}</p>
                <p className="text-sm text-muted-foreground">
                  Received: {format(new Date(report.receivedDate), 'PPpp')}
                </p>
              </CardContent>
            </Card>

            {report.structuredData && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Key Findings</CardTitle>
                    <CardDescription>AI-extracted pathology findings</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {report.structuredData.findings.map((finding, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-sm">
                          <CheckCircle className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                          <span>{finding}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {report.structuredData.recommendations.map((rec, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-sm">
                          <CheckCircle className="h-4 w-4 text-success mt-0.5 flex-shrink-0" />
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          <TabsContent value="report">
            <Card>
              <CardHeader>
                <CardTitle>Raw Pathology Report</CardTitle>
                <CardDescription>Original report from pathology lab</CardDescription>
              </CardHeader>
              <CardContent>
                <pre className="text-sm font-mono whitespace-pre-wrap text-foreground bg-muted p-4 rounded-md">
                  {report.raw_text || 'No raw report available'}
                </pre>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="plan">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>AI-Generated Clinical Plan</CardTitle>
                    <CardDescription>Recommended management strategy</CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={onRegeneratePlan}>
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Regenerate
                    </Button>
                    <Button size="sm" onClick={onApprovePlan}>
                      <CheckCircle className="h-4 w-4 mr-2" />
                      Approve Plan
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {report.clinicalPlanText || report.clinical_plan?.treatment_plan ? (
                  <div className="prose prose-sm max-w-none">
                    <pre className="whitespace-pre-wrap font-sans text-sm">
                      {report.clinicalPlanText || report.clinical_plan?.treatment_plan}
                    </pre>
                  </div>
                ) : (
                  <p className="text-muted-foreground">Clinical plan is being generated...</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="message">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Patient Communication Draft</CardTitle>
                    <CardDescription>AI-generated patient-friendly message</CardDescription>
                  </div>
                  <Button size="sm" onClick={onSendMessage}>
                    <Send className="h-4 w-4 mr-2" />
                    Send to Patient
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                {report.patientMessageText || report.patient_communication?.message_content ? (
                  <div className="bg-muted p-4 rounded-md">
                    <pre className="whitespace-pre-wrap font-sans text-sm">
                      {report.patientMessageText || report.patient_communication?.message_content}
                    </pre>
                  </div>
                ) : (
                  <p className="text-muted-foreground">Patient message is being drafted...</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="agent">
            <AgentChat reportId={report.report_id} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};
