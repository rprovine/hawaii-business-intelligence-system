// Vercel serverless function for triggering workflows
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { action, source } = req.body;
  const timestamp = new Date().toISOString();

  // Simulate workflow trigger response
  const response = {
    success: true,
    workflow_id: Math.random().toString(36).substring(7),
    action: action,
    source: source || 'all',
    status: 'initiated',
    message: `Workflow ${action} for ${source || 'all sources'} has been triggered successfully`,
    started_at: timestamp,
    estimated_duration_minutes: action === 'scrape' ? 15 : action === 'analyze' ? 10 : 5
  };

  res.status(200).json(response);
}