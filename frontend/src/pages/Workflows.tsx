import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { 
  Workflow, 
  PlayCircle, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Database,
  Brain,
  Bell,
  Calendar,
  RefreshCw,
  Activity,
  FileText
} from 'lucide-react';
import { fetchWorkflowStatus, fetchDataCollectionLogs, triggerWorkflow } from '../services/api';
import { format } from 'date-fns';
import { cn } from '../utils/cn';

const Workflows: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState<'overview' | 'logs' | 'schedule'>('overview');
  const queryClient = useQueryClient();

  // Fetch data
  const { data: workflowStatus, refetch: refetchStatus } = useQuery(
    'workflow-status',
    fetchWorkflowStatus,
    { refetchInterval: 5000 } // Refresh every 5 seconds
  );

  const { data: collectionLogs } = useQuery(
    'collection-logs',
    fetchDataCollectionLogs
  );

  // Mutations
  const triggerMutation = useMutation(triggerWorkflow, {
    onSuccess: () => {
      queryClient.invalidateQueries('workflow-status');
      queryClient.invalidateQueries('collection-logs');
    }
  });

  const handleTriggerWorkflow = (action: string, source?: string) => {
    if (window.confirm(`Are you sure you want to trigger ${action} workflow?`)) {
      triggerMutation.mutate({ action, source });
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'text-green-600 bg-green-100';
      case 'running': return 'text-blue-600 bg-blue-100';
      case 'failed': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return <CheckCircle className="h-4 w-4" />;
      case 'running': return <RefreshCw className="h-4 w-4 animate-spin" />;
      case 'failed': return <XCircle className="h-4 w-4" />;
      default: return <AlertCircle className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              <Workflow className="h-6 w-6 mr-2 text-ocean-600" />
              Workflows
            </h2>
            <p className="text-gray-600 mt-1">
              Manage data collection and automation workflows
            </p>
          </div>
          <button
            onClick={() => refetchStatus()}
            className="mt-4 sm:mt-0 px-4 py-2 bg-ocean-600 text-white rounded-lg hover:bg-ocean-700 flex items-center gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh Status
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setSelectedTab('overview')}
            className={cn(
              'py-2 px-1 border-b-2 font-medium text-sm',
              selectedTab === 'overview'
                ? 'border-ocean-500 text-ocean-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            )}
          >
            Overview
          </button>
          <button
            onClick={() => setSelectedTab('logs')}
            className={cn(
              'py-2 px-1 border-b-2 font-medium text-sm',
              selectedTab === 'logs'
                ? 'border-ocean-500 text-ocean-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            )}
          >
            Collection Logs
          </button>
          <button
            onClick={() => setSelectedTab('schedule')}
            className={cn(
              'py-2 px-1 border-b-2 font-medium text-sm',
              selectedTab === 'schedule'
                ? 'border-ocean-500 text-ocean-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            )}
          >
            Schedule
          </button>
        </nav>
      </div>

      {/* Content */}
      {selectedTab === 'overview' && (
        <div className="space-y-6">
          {/* Workflow Actions */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Scraping Workflow */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center">
                    <Database className="h-6 w-6 text-ocean-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">Data Collection</h3>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    Collect business data from configured sources
                  </p>
                  <div className="mt-4 space-y-2">
                    <button
                      onClick={() => handleTriggerWorkflow('scrape', 'all')}
                      disabled={triggerMutation.isLoading}
                      className="w-full px-4 py-2 bg-ocean-600 text-white rounded-lg hover:bg-ocean-700 disabled:opacity-50 flex items-center justify-center gap-2"
                    >
                      <PlayCircle className="h-4 w-4" />
                      Run All Sources
                    </button>
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        onClick={() => handleTriggerWorkflow('scrape', 'yelp')}
                        disabled={triggerMutation.isLoading}
                        className="px-3 py-1 bg-white text-ocean-600 border border-ocean-600 rounded text-sm hover:bg-ocean-50"
                      >
                        Yelp
                      </button>
                      <button
                        onClick={() => handleTriggerWorkflow('scrape', 'google')}
                        disabled={triggerMutation.isLoading}
                        className="px-3 py-1 bg-white text-ocean-600 border border-ocean-600 rounded text-sm hover:bg-ocean-50"
                      >
                        Google
                      </button>
                      <button
                        onClick={() => handleTriggerWorkflow('scrape', 'linkedin')}
                        disabled={triggerMutation.isLoading}
                        className="px-3 py-1 bg-white text-ocean-600 border border-ocean-600 rounded text-sm hover:bg-ocean-50"
                      >
                        LinkedIn
                      </button>
                      <button
                        onClick={() => handleTriggerWorkflow('scrape', 'news')}
                        disabled={triggerMutation.isLoading}
                        className="px-3 py-1 bg-white text-ocean-600 border border-ocean-600 rounded text-sm hover:bg-ocean-50"
                      >
                        News
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Analysis Workflow */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center">
                    <Brain className="h-6 w-6 text-palm-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">AI Analysis</h3>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    Analyze prospects with Claude AI
                  </p>
                  <button
                    onClick={() => handleTriggerWorkflow('analyze')}
                    disabled={triggerMutation.isLoading}
                    className="mt-4 w-full px-4 py-2 bg-palm-600 text-white rounded-lg hover:bg-palm-700 disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    <PlayCircle className="h-4 w-4" />
                    Run Analysis
                  </button>
                </div>
              </div>
            </div>

            {/* Alert Workflow */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center">
                    <Bell className="h-6 w-6 text-coral-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">Alerts</h3>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    Send alerts for high-priority prospects
                  </p>
                  <button
                    onClick={() => handleTriggerWorkflow('alert')}
                    disabled={triggerMutation.isLoading}
                    className="mt-4 w-full px-4 py-2 bg-coral-600 text-white rounded-lg hover:bg-coral-700 disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    <PlayCircle className="h-4 w-4" />
                    Send Alerts
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Running Workflows */}
          {workflowStatus?.running_workflows?.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Running Workflows</h3>
              <div className="space-y-3">
                {workflowStatus.running_workflows.map((workflow: any) => (
                  <div key={workflow.id} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center">
                      <RefreshCw className="h-5 w-5 text-blue-600 animate-spin mr-3" />
                      <div>
                        <p className="font-medium text-gray-900">{workflow.name}</p>
                        <p className="text-sm text-gray-500">Started {workflow.started_at}</p>
                      </div>
                    </div>
                    <span className="text-sm text-blue-600">Running...</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Runs */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Recent Runs</h3>
            </div>
            <div className="divide-y divide-gray-200">
              {workflowStatus?.recent_runs?.map((run: any) => (
                <div key={run.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={cn('p-2 rounded-lg', getStatusColor(run.status))}>
                        {getStatusIcon(run.status)}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{run.source}</p>
                        <p className="text-sm text-gray-500">
                          {format(new Date(run.run_date), 'MMM d, yyyy h:mm a')}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {run.records_found} found, {run.records_added} added
                      </p>
                      <p className="text-xs text-gray-500">
                        {run.duration_seconds}s
                      </p>
                    </div>
                  </div>
                </div>
              )) || (
                <div className="px-6 py-8 text-center text-gray-500">
                  No recent runs
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {selectedTab === 'logs' && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Collection Logs</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Records
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Duration
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Errors
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {collectionLogs?.map((log: any) => (
                  <tr key={log.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {log.source}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {format(new Date(log.run_date), 'MMM d, yyyy h:mm a')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={cn(
                        'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                        getStatusColor(log.status)
                      )}>
                        {getStatusIcon(log.status)}
                        <span className="ml-1">{log.status}</span>
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {log.records_found} / {log.records_processed} / {log.records_added}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {log.duration_seconds}s
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {log.errors || 0}
                    </td>
                  </tr>
                )) || (
                  <tr>
                    <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                      No collection logs available
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {selectedTab === 'schedule' && (
        <div className="grid grid-cols-1 gap-6">
          {/* Schedule Overview */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Calendar className="h-5 w-5 mr-2 text-ocean-600" />
              Workflow Schedule
            </h3>
            <div className="space-y-4">
              <div className="border-l-4 border-ocean-500 pl-4 py-2">
                <h4 className="font-medium text-gray-900">Daily Collection</h4>
                <p className="text-sm text-gray-600">6:00 AM & 6:00 PM HST</p>
                <p className="text-xs text-gray-500 mt-1">Full data collection from all configured sources</p>
              </div>
              <div className="border-l-4 border-palm-500 pl-4 py-2">
                <h4 className="font-medium text-gray-900">Hourly Quick Scan</h4>
                <p className="text-sm text-gray-600">Every hour</p>
                <p className="text-xs text-gray-500 mt-1">Quick scan of high-priority sources for new listings</p>
              </div>
              <div className="border-l-4 border-coral-500 pl-4 py-2">
                <h4 className="font-medium text-gray-900">Weekly Analytics</h4>
                <p className="text-sm text-gray-600">Every Monday at 9:00 AM HST</p>
                <p className="text-xs text-gray-500 mt-1">Generate and send weekly performance report</p>
              </div>
              <div className="border-l-4 border-sand-500 pl-4 py-2">
                <h4 className="font-medium text-gray-900">Monthly Deep Analysis</h4>
                <p className="text-sm text-gray-600">First day of each month at 10:00 AM HST</p>
                <p className="text-xs text-gray-500 mt-1">Comprehensive re-analysis of all prospects</p>
              </div>
            </div>
          </div>

          {/* Schedule Configuration */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Configuration</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Automatic Scheduling</p>
                  <p className="text-sm text-gray-500">Run workflows according to the schedule</p>
                </div>
                <div className="flex items-center">
                  <span className="text-sm text-gray-500 mr-3">Enabled</span>
                  <div className="w-12 h-6 bg-ocean-600 rounded-full relative">
                    <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow"></div>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Error Notifications</p>
                  <p className="text-sm text-gray-500">Send alerts when workflows fail</p>
                </div>
                <div className="flex items-center">
                  <span className="text-sm text-gray-500 mr-3">Enabled</span>
                  <div className="w-12 h-6 bg-ocean-600 rounded-full relative">
                    <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow"></div>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Rate Limiting</p>
                  <p className="text-sm text-gray-500">Respect API rate limits for external sources</p>
                </div>
                <div className="flex items-center">
                  <span className="text-sm text-gray-500 mr-3">Enabled</span>
                  <div className="w-12 h-6 bg-ocean-600 rounded-full relative">
                    <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Notification for triggered workflows */}
      {triggerMutation.isSuccess && (
        <div className="fixed bottom-4 right-4 bg-green-50 border border-green-200 rounded-lg p-4 shadow-lg">
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            <p className="text-sm text-green-800">Workflow triggered successfully!</p>
          </div>
        </div>
      )}

      {triggerMutation.isError && (
        <div className="fixed bottom-4 right-4 bg-red-50 border border-red-200 rounded-lg p-4 shadow-lg">
          <div className="flex items-center">
            <XCircle className="h-5 w-5 text-red-600 mr-2" />
            <p className="text-sm text-red-800">Failed to trigger workflow</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Workflows;