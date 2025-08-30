// Vercel serverless function for workflow logs
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const now = Date.now();
  const logs = [
    {
      id: 1,
      timestamp: new Date(now - 1000 * 60 * 5).toISOString(),
      action: 'scrape',
      source: 'google',
      status: 'success',
      message: 'Successfully scraped 12 new businesses from Google Places',
      details: {
        records_found: 12,
        records_processed: 12,
        records_added: 8,
        records_updated: 4,
        duration_seconds: 45
      }
    },
    {
      id: 2,
      timestamp: new Date(now - 1000 * 60 * 30).toISOString(),
      action: 'analyze',
      source: 'all',
      status: 'success',
      message: 'AI analysis completed for 15 prospects',
      details: {
        prospects_analyzed: 15,
        high_priority_identified: 5,
        recommendations_generated: 45,
        duration_seconds: 120
      }
    },
    {
      id: 3,
      timestamp: new Date(now - 1000 * 60 * 60).toISOString(),
      action: 'scrape',
      source: 'pbn',
      status: 'success',
      message: 'Pacific Business News: Found 3 relevant articles',
      details: {
        articles_found: 3,
        companies_mentioned: 7,
        new_leads: 2,
        duration_seconds: 30
      }
    },
    {
      id: 4,
      timestamp: new Date(now - 1000 * 60 * 120).toISOString(),
      action: 'alert',
      source: 'email',
      status: 'success',
      message: 'Sent 5 high-priority prospect alerts',
      details: {
        alerts_sent: 5,
        email_recipients: 2,
        sms_recipients: 0,
        duration_seconds: 10
      }
    },
    {
      id: 5,
      timestamp: new Date(now - 1000 * 60 * 180).toISOString(),
      action: 'scrape',
      source: 'linkedin',
      status: 'partial',
      message: 'LinkedIn scraping partially successful (rate limited)',
      details: {
        profiles_attempted: 20,
        profiles_scraped: 15,
        rate_limited_at: 15,
        duration_seconds: 90
      }
    },
    {
      id: 6,
      timestamp: new Date(now - 1000 * 60 * 240).toISOString(),
      action: 'scrape',
      source: 'yelp',
      status: 'success',
      message: 'Yelp: Updated information for 18 businesses',
      details: {
        businesses_checked: 25,
        updates_found: 18,
        new_reviews: 42,
        rating_changes: 6,
        duration_seconds: 60
      }
    },
    {
      id: 7,
      timestamp: new Date(now - 1000 * 60 * 300).toISOString(),
      action: 'scrape',
      source: 'custom',
      status: 'failed',
      message: 'Custom webscrape failed: Invalid URL provided',
      details: {
        error: 'URL validation failed',
        url_provided: 'https://invalid-example',
        duration_seconds: 2
      }
    },
    {
      id: 8,
      timestamp: new Date(now - 1000 * 60 * 360).toISOString(),
      action: 'analyze',
      source: 'all',
      status: 'success',
      message: 'Overnight batch analysis completed',
      details: {
        prospects_analyzed: 45,
        scoring_updated: 45,
        new_insights: 123,
        duration_seconds: 300
      }
    }
  ];

  res.status(200).json(logs);
}