# Hawaii Business Intelligence - Data Collection Guide

## Overview

The system now supports both **demo data** (for demonstrations) and **real data** collection from multiple sources.

## Quick Start

### 1. Load Demo Data (For Testing/Demos)
```bash
cd data-collectors
python collect_data.py demo
```
This loads 20 sample Hawaii businesses across all islands.

### 2. Collect Real Data

#### Option A: Collect from All Real Sources
```bash
python collect_data.py real
```

#### Option B: Collect from Specific Sources
```bash
# Yelp data (no API key required)
python collect_data.py yelp

# Hawaii Business News
python collect_data.py news

# Google Places (requires API key)
export GOOGLE_PLACES_API_KEY='your-api-key-here'
python collect_data.py google
```

### 3. Run Continuous Collection
```bash
# Run scheduled collection continuously
python collect_data.py real --continuous
```

## Data Sources

### Currently Active

1. **Demo Data** (`sample_businesses`)
   - 20 realistic Hawaii businesses
   - Covers all islands and industries
   - Perfect for demos and testing

2. **Hawaii Business News** (`hawaii_business_news`)
   - Scrapes recent business news
   - Finds companies mentioned in growth stories
   - No API key required

3. **Yelp** (`yelp`)
   - Real business listings from Yelp
   - Covers restaurants, hotels, medical, services
   - No API key required
   - Rate limited to be respectful

4. **Google Places** (`google_places`)
   - Most comprehensive business data
   - Requires Google Places API key
   - Get key from: https://console.cloud.google.com/

### Coming Soon

- Chamber of Commerce directories
- LinkedIn company data
- Hawaii state business registrations
- Industry association directories

## Setting Up Google Places API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Places API"
4. Create credentials (API Key)
5. Set the key:
   ```bash
   export GOOGLE_PLACES_API_KEY='your-key-here'
   ```
   Or add to `.env` file:
   ```
   GOOGLE_PLACES_API_KEY=your-key-here
   ```

## Best Practices

1. **For Demos**: Always have demo data loaded
   ```bash
   python collect_data.py demo
   ```

2. **For Production**: Run real data collection daily
   ```bash
   python collect_data.py real
   ```

3. **API Limits**: 
   - Yelp: Respectful scraping with delays
   - Google Places: 150,000 requests/month free tier
   - Adjust collection frequency based on your needs

4. **Data Quality**:
   - The system automatically filters out chains/franchises
   - Focuses on local Hawaii businesses
   - Estimates employee counts and industries

## Monitoring Collection

Check the logs:
```bash
tail -f data_collection_*.log
```

View in dashboard:
- http://localhost:3002
- See total prospects, by island, by industry

## Troubleshooting

**"No module named 'schedule'"**
```bash
pip install -r requirements.txt
```

**"Google Places API key not found"**
```bash
export GOOGLE_PLACES_API_KEY='your-key-here'
```

**Rate limiting errors**
- Reduce the number of locations/categories in scraper config
- Add longer delays between requests

## Database Management

View current data:
```bash
# Connect to PostgreSQL
psql -U postgres -d hawaii_business_intel

# Check prospect count
SELECT COUNT(*) FROM prospects;

# View by source
SELECT source, COUNT(*) FROM companies GROUP BY source;
```

Clear data if needed:
```bash
# Clear all prospects (keeps companies)
DELETE FROM prospects;

# Clear everything and start fresh
DELETE FROM prospects;
DELETE FROM companies;
```