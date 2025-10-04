import { FileText, Phone, MessageSquare, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  count?: number;
}

interface InboxNavProps {
  selectedCategory: string;
  onSelectCategory: (category: string) => void;
}

const navItems: NavItem[] = [
  { id: 'results', label: 'Results', icon: <FileText className="h-4 w-4" />, count: 4 },
  { id: 'patient-calls', label: 'Patient Calls', icon: <Phone className="h-4 w-4" />, count: 2 },
  { id: 'messages', label: 'Case Messages', icon: <MessageSquare className="h-4 w-4" /> },
  { id: 'urgent', label: 'Urgent', icon: <AlertCircle className="h-4 w-4" />, count: 1 },
  { id: 'pending', label: 'Pending Review', icon: <Clock className="h-4 w-4" />, count: 3 },
  { id: 'completed', label: 'Completed', icon: <CheckCircle className="h-4 w-4" /> },
];

export const InboxNav = ({ selectedCategory, onSelectCategory }: InboxNavProps) => {
  return (
    <div className="w-60 border-r bg-card h-full overflow-y-auto">
      <div className="p-4">
        <h2 className="text-sm font-semibold text-foreground mb-3">Inbox</h2>
        <nav className="space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onSelectCategory(item.id)}
              className={cn(
                'w-full flex items-center justify-between px-3 py-2 rounded-md text-sm transition-colors',
                selectedCategory === item.id
                  ? 'bg-primary text-primary-foreground font-medium'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground'
              )}
            >
              <div className="flex items-center gap-2">
                {item.icon}
                <span>{item.label}</span>
              </div>
              {item.count !== undefined && item.count > 0 && (
                <span
                  className={cn(
                    'px-2 py-0.5 rounded-full text-xs font-medium',
                    selectedCategory === item.id
                      ? 'bg-primary-foreground text-primary'
                      : 'bg-muted text-muted-foreground'
                  )}
                >
                  {item.count}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
};
