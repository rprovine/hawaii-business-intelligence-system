// Vercel serverless function for analytics by island
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
    "Oahu": 6,
    "Maui": 3,
    "Big Island": 2,
    "Kauai": 2,
    "Molokai": 1,
    "Lanai": 1
  };

  res.status(200).json(analyticsData);
}