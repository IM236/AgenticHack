import { Button } from '@/components/ui/button';
import { Mail, RefreshCw, Settings, Paperclip, Zap } from 'lucide-react';

export const TopBar = () => {
  return (
    <div className="h-14 border-b bg-card flex items-center justify-between px-4 shadow-sm">
      <div className="flex items-center gap-2">
        <h1 className="text-lg font-semibold text-foreground">Pathology Workflow</h1>
        <span className="text-xs text-muted-foreground">Epic Integration</span>
      </div>
      
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="sm">
          <Mail className="h-4 w-4 mr-2" />
          New Msg
        </Button>
        <Button variant="ghost" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
        <Button variant="ghost" size="sm">
          <Paperclip className="h-4 w-4 mr-2" />
          Attach
        </Button>
        <Button variant="default" size="sm">
          <Zap className="h-4 w-4 mr-2" />
          Quick Actions
        </Button>
        <Button variant="ghost" size="icon">
          <Settings className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
};
