import { ReportStatus } from '@/types/pathology';
import { cn } from '@/lib/utils';
import { CheckCircle, Circle, Clock, MessageCircle, FileCheck } from 'lucide-react';

interface StatusTrackerProps {
  status: ReportStatus;
  className?: string;
}

const statusSteps = [
  { id: 'new', label: 'Received', icon: Circle },
  { id: 'analyzing', label: 'Analyzing', icon: Clock },
  { id: 'plan_ready', label: 'Plan Created', icon: FileCheck },
  { id: 'message_sent', label: 'Message Sent', icon: MessageCircle },
  { id: 'completed', label: 'Completed', icon: CheckCircle },
] as const;

export const StatusTracker = ({ status, className }: StatusTrackerProps) => {
  const currentIndex = statusSteps.findIndex(step => step.id === status);

  return (
    <div className={cn('flex items-center gap-2', className)}>
      {statusSteps.map((step, index) => {
        const Icon = step.icon;
        const isActive = index <= currentIndex;
        const isCurrent = index === currentIndex;

        return (
          <div key={step.id} className="flex items-center">
            <div className="flex flex-col items-center gap-1">
              <div
                className={cn(
                  'flex items-center justify-center w-8 h-8 rounded-full transition-colors',
                  isActive
                    ? isCurrent
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-success text-success-foreground'
                    : 'bg-muted text-muted-foreground'
                )}
              >
                <Icon className="h-4 w-4" />
              </div>
              <span
                className={cn(
                  'text-xs font-medium',
                  isActive ? 'text-foreground' : 'text-muted-foreground'
                )}
              >
                {step.label}
              </span>
            </div>
            {index < statusSteps.length - 1 && (
              <div
                className={cn(
                  'h-0.5 w-12 mx-2 transition-colors',
                  index < currentIndex ? 'bg-success' : 'bg-muted'
                )}
              />
            )}
          </div>
        );
      })}
    </div>
  );
};
