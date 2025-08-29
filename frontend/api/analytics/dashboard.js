// Vercel serverless function for dashboard data
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const dashboardData = {
    total_companies: 15,
    total_prospects: 15,
    high_priority_count: 5,
    total_pipeline_value: 125000,
    active_workflows: 3,
    recent_interactions: 8,
    high_score_prospects: 8,
    average_score: 85,
    by_island: [
      { island: 'Oahu', prospect_count: 6 },
      { island: 'Maui', prospect_count: 3 },
      { island: 'Big Island', prospect_count: 2 },
      { island: 'Kauai', prospect_count: 2 },
      { island: 'Molokai', prospect_count: 1 },
      { island: 'Lanai', prospect_count: 1 }
    ],
    by_industry: [
      { industry: 'Tourism', prospect_count: 5 },
      { industry: 'Healthcare', prospect_count: 3 },
      { industry: 'Technology', prospect_count: 3 },
      { industry: 'Food Service', prospect_count: 2 },
      { industry: 'Real Estate', prospect_count: 2 }
    ],
    recent_high_scores: [
      {
        id: 1,
        score: 92,
        company: {
          name: 'Aloha Medical Center',
          island: 'Oahu',
          industry: 'Healthcare'
        },
        recommended_services: ['AI Scheduling System', 'Predictive Analytics', 'Patient Chatbot']
      },
      {
        id: 2,
        score: 88,
        company: {
          name: 'Pacific Paradise Resort',
          island: 'Maui',
          industry: 'Tourism'
        },
        recommended_services: ['Dynamic Pricing AI', 'Guest Experience Bot']
      },
      {
        id: 4,
        score: 95,
        company: {
          name: 'Island Tech Solutions',
          island: 'Oahu',
          industry: 'Technology'
        },
        recommended_services: ['AI Development Tools', 'Automated Testing']
      }
    ]
  };

  res.status(200).json(dashboardData);
}