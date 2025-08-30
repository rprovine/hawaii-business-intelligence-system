// Vercel serverless function for interactions
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const { prospect_id } = req.query;

  // Generate interactions based on prospect_id or return all
  const interactions = [
    {
      id: 1,
      prospect_id: prospect_id || 1,
      type: 'email',
      date: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(),
      subject: 'Introduction to AI Solutions',
      status: 'sent',
      notes: 'Sent initial outreach email with case studies',
      performed_by: 'John Smith'
    },
    {
      id: 2,
      prospect_id: prospect_id || 1,
      type: 'call',
      date: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
      subject: 'Follow-up Call',
      status: 'completed',
      notes: 'Spoke with CEO, very interested in scheduling demo',
      performed_by: 'Sarah Johnson',
      duration_minutes: 15
    },
    {
      id: 3,
      prospect_id: prospect_id || 1,
      type: 'meeting',
      date: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
      subject: 'Product Demo',
      status: 'scheduled',
      notes: 'Demo scheduled for next week Tuesday',
      performed_by: 'Mike Chen',
      attendees: ['CEO', 'CTO', 'Operations Manager']
    },
    {
      id: 4,
      prospect_id: prospect_id || 1,
      type: 'note',
      date: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
      subject: 'Research Note',
      status: 'completed',
      notes: 'Company recently received Series A funding, good timing for expansion',
      performed_by: 'System'
    }
  ];

  if (req.method === 'POST') {
    // Handle creating new interaction
    const newInteraction = {
      id: interactions.length + 1,
      ...req.body,
      date: new Date().toISOString(),
      status: 'completed'
    };
    interactions.push(newInteraction);
    return res.status(201).json(newInteraction);
  }

  // Filter by prospect_id if provided
  const filteredInteractions = prospect_id 
    ? interactions.filter(i => i.prospect_id == prospect_id)
    : interactions;

  res.status(200).json(filteredInteractions);
}