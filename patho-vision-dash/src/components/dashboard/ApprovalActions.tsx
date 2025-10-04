import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { CheckCircle, XCircle, MessageSquare } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { useApproveReport, useRejectReport } from '@/hooks/usePathologyApi';
import { toast } from 'sonner';

interface ApprovalActionsProps {
  reportId: string;
  hasClinicalPlan: boolean;
  hasPatientMessage: boolean;
}

export const ApprovalActions = ({ reportId, hasClinicalPlan, hasPatientMessage }: ApprovalActionsProps) => {
  const [approveClinicalPlan, setApproveClinicalPlan] = useState(false);
  const [approvePatientMessage, setApprovePatientMessage] = useState(false);
  const [revisionNotes, setRevisionNotes] = useState('');
  const [showRevisionBox, setShowRevisionBox] = useState(false);

  const approveMutation = useApproveReport();
  const rejectMutation = useRejectReport();

  const handleApprove = () => {
    if (!approveClinicalPlan && !approvePatientMessage) {
      toast.error('Please select at least one item to approve');
      return;
    }

    approveMutation.mutate(
      {
        report_id: reportId,
        approve_clinical_plan: approveClinicalPlan,
        approve_patient_message: approvePatientMessage,
        revision_notes: revisionNotes || undefined,
      },
      {
        onSuccess: () => {
          toast.success('Report approved successfully');
          setApproveClinicalPlan(false);
          setApprovePatientMessage(false);
          setRevisionNotes('');
          setShowRevisionBox(false);
        },
        onError: (error) => {
          toast.error(`Approval failed: ${error.message}`);
        },
      }
    );
  };

  const handleReject = () => {
    if (!revisionNotes.trim()) {
      toast.error('Please provide revision notes');
      return;
    }

    rejectMutation.mutate(
      { reportId, revisionNotes },
      {
        onSuccess: () => {
          toast.success('Report rejected with revision notes');
          setRevisionNotes('');
          setShowRevisionBox(false);
        },
        onError: (error) => {
          toast.error(`Rejection failed: ${error.message}`);
        },
      }
    );
  };

  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>Physician Review</CardTitle>
        <CardDescription>Approve or request revisions for AI-generated content</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          {hasClinicalPlan && (
            <div className="flex items-center space-x-2">
              <Checkbox
                id="approve-plan"
                checked={approveClinicalPlan}
                onCheckedChange={(checked) => setApproveClinicalPlan(checked as boolean)}
              />
              <Label htmlFor="approve-plan" className="text-sm font-medium cursor-pointer">
                Approve Clinical Plan
              </Label>
            </div>
          )}

          {hasPatientMessage && (
            <div className="flex items-center space-x-2">
              <Checkbox
                id="approve-message"
                checked={approvePatientMessage}
                onCheckedChange={(checked) => setApprovePatientMessage(checked as boolean)}
              />
              <Label htmlFor="approve-message" className="text-sm font-medium cursor-pointer">
                Approve Patient Message
              </Label>
            </div>
          )}
        </div>

        {showRevisionBox && (
          <div className="space-y-2">
            <Label htmlFor="revision-notes">Revision Notes</Label>
            <Textarea
              id="revision-notes"
              placeholder="Provide specific feedback for the AI agent..."
              value={revisionNotes}
              onChange={(e) => setRevisionNotes(e.target.value)}
              rows={4}
            />
          </div>
        )}

        <div className="flex gap-2">
          <Button
            onClick={handleApprove}
            disabled={(!approveClinicalPlan && !approvePatientMessage) || approveMutation.isPending}
            className="flex-1"
          >
            <CheckCircle className="h-4 w-4 mr-2" />
            {approveMutation.isPending ? 'Approving...' : 'Approve'}
          </Button>

          <Button
            variant="outline"
            onClick={() => setShowRevisionBox(!showRevisionBox)}
            className="flex-1"
          >
            <MessageSquare className="h-4 w-4 mr-2" />
            Request Revision
          </Button>

          <Button
            variant="destructive"
            onClick={handleReject}
            disabled={!revisionNotes.trim() || rejectMutation.isPending}
            className="flex-1"
          >
            <XCircle className="h-4 w-4 mr-2" />
            {rejectMutation.isPending ? 'Rejecting...' : 'Reject'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
