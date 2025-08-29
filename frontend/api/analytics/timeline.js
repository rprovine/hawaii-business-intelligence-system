// Vercel serverless function for analytics timeline
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Generate timeline data for the last 30 days
  const timeline = [];
  const today = new Date();
  
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    
    timeline.push({
      date: date.toISOString().split('T')[0],
      prospects_created: Math.floor(Math.random() * 3) + 1,
      interactions: Math.floor(Math.random() * 5) + 2,
      workflows_triggered: Math.floor(Math.random() * 2),
      conversion_rate: Math.random() * 0.3 + 0.1 // 10-40% conversion rate
    });
  }

  res.status(200).json(timeline);
}