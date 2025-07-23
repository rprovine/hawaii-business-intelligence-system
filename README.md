# Hawaii Business Intelligence System

A comprehensive AI-powered business intelligence platform designed specifically for Hawaii's unique market, built for LeniLani Consulting to identify, analyze, and qualify potential clients across all Hawaiian islands.

## 🌺 Overview

The Hawaii Business Intelligence System combines real-time web scraping, Google Places API integration, and advanced Claude AI analysis to provide actionable insights for AI consulting opportunities in Hawaii's business ecosystem.

### Key Features

- **Comprehensive Business Discovery**: Automated scraping from Google Places API across all Hawaiian islands
- **AI-Powered Analysis**: Claude AI provides detailed strategic analysis with Hawaii market context
- **Decision Maker Identification**: Intelligent extraction of key contacts from business websites
- **Geographic Intelligence**: Island-specific business categorization and market insights
- **Real-time Data**: Live data collection from verified business websites
- **Lead Scoring**: Intelligent ranking based on AI potential and market fit
- **Cultural Context**: Hawaii-specific business culture and relationship considerations

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.9+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Integration**: Anthropic Claude API for business analysis
- **Web Scraping**: BeautifulSoup + Google Places API
- **APIs**: RESTful endpoints with automatic OpenAPI documentation

### Frontend (React)
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with responsive design
- **Data Fetching**: React Query for efficient API management
- **Visualization**: Recharts for analytics dashboards
- **UI Components**: Custom components with mobile-first design

### Data Sources
- **Google Places API**: Business discovery and verification
- **Live Web Scraping**: Real business website content
- **Claude AI**: Strategic analysis and insights
- **Hawaii Market Data**: Island-specific business intelligence

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)
- Google Places API key
- Anthropic Claude API key

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hawaii-business-intelligence-system.git
   cd hawaii-business-intelligence-system
   ```

2. **Environment Variables**
   
   Create `.env` file in the backend directory:
   ```env
   # Database
   DATABASE_URL=postgresql://postgres:password@localhost:5432/hawaii_business_db
   
   # API Keys
   CLAUDE_API_KEY=sk-ant-api03-your-claude-key
   ANTHROPIC_API_KEY=sk-ant-api03-your-claude-key
   GOOGLE_PLACES_API_KEY=your-google-places-key
   
   # Application
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3002
   ```

3. **Docker Deployment (Recommended)**
   ```bash
   docker-compose up -d
   ```

4. **Manual Setup** (Alternative)
   
   Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn main:app --reload --port 8000
   ```
   
   Frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Initial Data Collection

```bash
# Run comprehensive business scraping
cd backend
python comprehensive_scraper.py

# Enhance with AI analysis
python enhanced_ai_analysis.py
```

## 📊 Core Functionality

### Business Discovery Pipeline

1. **Google Places Search**: Discovers businesses across Hawaiian islands
2. **Website Scraping**: Extracts detailed business information
3. **AI Analysis**: Claude AI provides strategic insights
4. **Decision Maker Extraction**: Identifies key contacts
5. **Lead Scoring**: Ranks prospects by AI consulting potential

### Analysis Capabilities

- **Strategic Opportunity Assessment**: Market position and growth potential
- **Hawaii Market Context**: Tourism dependency, inter-island logistics
- **Pain Point Identification**: Specific operational challenges
- **Technology Readiness**: Digital transformation opportunities
- **ROI Projections**: Conservative and optimistic scenarios
- **Cultural Considerations**: Aloha spirit and relationship-first approach

### Data Management

- **Real-time Verification**: Live website connectivity checks
- **Duplicate Prevention**: Intelligent deduplication across data sources
- **Data Quality Scoring**: Comprehensive business information validation
- **Geographic Categorization**: Accurate island and region mapping

## 🏝️ Hawaii-Specific Features

### Island Coverage
- **Oahu**: Honolulu, Waikiki, Pearl City, Kaneohe
- **Maui**: Kahului, Lahaina, Kihei, Wailea
- **Big Island**: Kona, Hilo, Waimea
- **Kauai**: Lihue, Kapaa, Princeville, Poipu

### Industry Focus
- Healthcare (Dental, Medical)
- Tourism & Hospitality
- Professional Services (CPA, Legal)
- Food Service & Restaurants
- Real Estate
- Local Retail

### Cultural Intelligence
- Relationship-first business approach
- Aloha spirit considerations
- Local vs. mainland competition dynamics
- Sustainability and environmental consciousness
- Community-focused business strategies

## 🛠️ Services Offered Analysis

The system analyzes businesses for four key LeniLani Consulting services:

1. **Data Analytics**: Transform business data into actionable insights
2. **Custom Chatbots**: 24/7 AI-powered customer service
3. **HubSpot Digital Marketing**: Marketing automation and CRM
4. **Fractional CTO**: Strategic technology leadership

## 📈 Dashboard Features

### Analytics Overview
- Business distribution across islands
- Industry breakdown and trends
- Lead scoring distribution
- Data collection status

### Prospect Management
- Detailed business profiles
- Decision maker contact information
- AI analysis summaries
- Engagement tracking
- Priority scoring

### Geographic Intelligence
- Island-based business mapping
- Regional market insights
- Competitive landscape analysis
- Growth opportunity identification

## 🔌 API Documentation

### Core Endpoints

#### Business Discovery
- `GET /api/companies` - List all companies
- `GET /api/companies/{id}` - Company details
- `POST /api/companies/scrape` - Trigger new scraping

#### Prospect Analysis
- `GET /api/prospects` - List prospects with analysis
- `GET /api/prospects/{id}` - Detailed prospect view
- `PUT /api/prospects/{id}` - Update prospect data

#### Decision Makers
- `GET /api/decision-makers` - List all contacts
- `GET /api/companies/{id}/decision-makers` - Company contacts

#### Analytics
- `GET /api/analytics/dashboard` - Dashboard statistics
- `GET /api/analytics/islands` - Island distribution
- `GET /api/analytics/industries` - Industry breakdown

### Data Models

#### Company
```json
{
  "id": "uuid",
  "name": "Business Name",
  "website": "https://business.com",
  "island": "Oahu",
  "industry": "Healthcare",
  "employee_count_estimate": 25,
  "address": "123 Main St, Honolulu, HI 96814",
  "phone": "(808) 555-0123",
  "description": "Business description..."
}
```

#### Prospect Analysis
```json
{
  "id": "uuid",
  "company_id": "uuid",
  "score": 85,
  "ai_analysis": "Comprehensive analysis text...",
  "pain_points": ["Point 1", "Point 2"],
  "recommended_services": ["Data Analytics", "Custom Chatbots"],
  "estimated_deal_value": 75000,
  "technology_readiness": "Medium"
}
```

## 🔧 Development

### Project Structure
```
hawaii-business-intelligence-system/
├── backend/
│   ├── models/          # SQLAlchemy models
│   ├── api/            # FastAPI routes
│   ├── services/       # Business logic
│   ├── scrapers/       # Web scraping modules
│   └── main.py         # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   └── types/      # TypeScript definitions
│   └── public/         # Static assets
├── docker-compose.yml  # Container orchestration
└── docs/              # Additional documentation
```

### Database Schema

#### Core Tables
- `companies`: Business information
- `prospects`: AI analysis and scoring
- `decision_makers`: Contact information
- `data_sources`: Scraping source tracking

#### Enums
- `IslandEnum`: Oahu, Maui, Big Island, Kauai
- `IndustryEnum`: Healthcare, Tourism, Professional Services, etc.
- `ServiceEnum`: Data Analytics, Custom Chatbots, HubSpot Digital Marketing, Fractional CTO

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests  
cd frontend
npm test
```

## 🚢 Deployment

### Production Deployment

1. **Environment Configuration**
   ```bash
   cp .env.example .env.production
   # Edit with production values
   ```

2. **Database Migration**
   ```bash
   alembic upgrade head
   ```

3. **Docker Production**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Variables (Production)

```env
# Database (Production)
DATABASE_URL=postgresql://user:password@db-host:5432/hawaii_business_db

# API Keys (Required)
CLAUDE_API_KEY=sk-ant-api03-production-key
GOOGLE_PLACES_API_KEY=production-google-key

# Security
SECRET_KEY=secure-production-secret
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com

# Optional
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

## 📝 Usage Examples

### Scraping New Businesses
```python
from backend.comprehensive_scraper import import_scraped_businesses

# Discover and import new Hawaii businesses
import_scraped_businesses()
```

### AI Analysis Enhancement
```python
from backend.enhanced_ai_analysis import enhance_all_data

# Enhance existing businesses with comprehensive AI analysis
enhance_all_data()
```

### API Usage
```javascript
// Fetch prospects with high scores
const prospects = await fetch('/api/prospects?min_score=80')
  .then(res => res.json());

// Get island-specific businesses
const oahuBusinesses = await fetch('/api/companies?island=Oahu')
  .then(res => res.json());
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a Pull Request

### Development Guidelines

- Follow Python PEP 8 for backend code
- Use TypeScript for all frontend components
- Write comprehensive tests for new features
- Update documentation for API changes
- Respect rate limits for external APIs

## 📄 License

This project is proprietary software developed for LeniLani Consulting. All rights reserved.

## 🏢 About LeniLani Consulting

**Address**: 1050 Queen Street, Suite 100, Honolulu, Hawaii 96814

**Services**:
- Data Analytics & Business Intelligence
- Custom AI Chatbot Development  
- HubSpot Digital Marketing Automation
- Fractional CTO Services

**Mission**: Empowering Hawaii businesses with cutting-edge AI solutions tailored to the unique challenges and opportunities of island commerce.

## 🆘 Support

For technical support or business inquiries:

- **Technical Issues**: Create an issue in this repository
- **Business Development**: Contact LeniLani Consulting
- **API Questions**: See API documentation or create an issue

## 🔄 Changelog

### v1.0.0 (Current)
- Initial release with comprehensive business discovery
- Claude AI integration for strategic analysis
- Google Places API integration
- Decision maker extraction
- Hawaii-specific market intelligence
- Responsive React dashboard
- Docker containerization
- Complete API documentation

---

*Built with ❤️ for Hawaii's business community*