// Vercel serverless function for workflow status
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const workflowStatus = {
    active: 3,
    completed: 42,
    failed: 2,
    pending: 5,
    total_runs: 52,
    success_rate: 0.808,
    average_duration_minutes: 12.5,
    recent_workflows: [
      {
        id: 1,
        name: "Data Collection - Tourism Sector",
        status: "active",
        started_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
        progress: 65
      },
      {
        id: 2,
        name: "Prospect Analysis - Healthcare",
        status: "completed",
        started_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
        completed_at: new Date(Date.now() - 1000 * 60 * 18).toISOString(),
        progress: 100
      },
      {
        id: 3,
        name: "Email Campaign - High Priority",
        status: "active",
        started_at: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
        progress: 30
      },
      {
        id: 4,
        name: "AI Analysis - Tech Companies",
        status: "pending",
        scheduled_for: new Date(Date.now() + 1000 * 60 * 15).toISOString(),
        progress: 0
      },
      {
        id: 5,
        name: "Market Research - Food Service",
        status: "completed",
        started_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
        completed_at: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
        progress: 100
      }
    ]
  };

  res.status(200).json(workflowStatus);
}