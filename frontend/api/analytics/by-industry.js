// Vercel serverless function for analytics by industry
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const analyticsData = {
    "Tourism": 5,
    "Healthcare": 3,
    "Technology": 3,
    "Food Service": 2,
    "Real Estate": 2
  };

  res.status(200).json(analyticsData);
}