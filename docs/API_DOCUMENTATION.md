# Hawaii Business Intelligence System - API Documentation

## Overview

The Hawaii Business Intelligence System provides a comprehensive RESTful API built with FastAPI for managing Hawaii business data, AI analysis, and prospect management.

**Base URL**: `http://localhost:8000/api`  
**Documentation**: `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, the API is open for development. Production deployment should implement proper authentication.

## Data Models

### Company Model
```json
{
  "id": "uuid",
  "name": "string",
  "website": "string",
  "island": "Oahu|Maui|Big Island|Kauai", 
  "industry": "Healthcare|Tourism|Professional Services|Food Service|Real Estate|Other",
  "employee_count_estimate": "integer",
  "annual_revenue_estimate": "integer",
  "address": "string",
  "phone": "string",
  "description": "string",
  "source": "string",
  "source_url": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Prospect Model
```json
{
  "id": "uuid",
  "company_id": "uuid",
  "score": "integer (0-100)",
  "ai_analysis": "string",
  "pain_points": ["string"],
  "recommended_services": ["Data Analytics|Custom Chatbots|HubSpot Digital Marketing|Fractional CTO"],
  "estimated_deal_value": "integer",
  "growth_signals": ["string"],
  "technology_readiness": "Low|Medium|High",
  "priority_level": "Low|Medium|High",
  "last_analyzed": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Decision Maker Model
```json
{
  "id": "uuid",
  "company_id": "uuid",
  "name": "string",
  "title": "string",
  "email": "string",
  "phone": "string",
  "linkedin_url": "string",
  "notes": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Core API Endpoints

### Companies

#### List Companies
```http
GET /api/companies
```

**Query Parameters:**
- `island`: Filter by island (Oahu, Maui, Big-Island, Kauai)
- `industry`: Filter by industry
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "companies": [
    {
      "id": "uuid",
      "name": "Business Name",
      "website": "https://business.com",
      "island": "Oahu",
      "industry": "Healthcare",
      "employee_count_estimate": 25,
      "address": "123 Main St, Honolulu, HI 96814",
      "phone": "(808) 555-0123"
    }
  ],
  "total": 15,
  "limit": 50,
  "offset": 0
}
```

#### Get Company Details
```http
GET /api/companies/{company_id}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Business Name",
  "website": "https://business.com", 
  "island": "Oahu",
  "industry": "Healthcare",
  "employee_count_estimate": 25,
  "annual_revenue_estimate": 3750000,
  "address": "123 Main St, Honolulu, HI 96814",
  "phone": "(808) 555-0123",
  "description": "Leading dental practice...",
  "source": "Google Places API",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Create Company
```http
POST /api/companies
```

**Request Body:**
```json
{
  "name": "New Business",
  "website": "https://newbusiness.com",
  "island": "Oahu",
  "industry": "Healthcare",
  "employee_count_estimate": 15,
  "address": "456 Ala Moana Blvd, Honolulu, HI 96814",
  "phone": "(808) 555-9999",
  "description": "New healthcare practice"
}
```

### Prospects

#### List Prospects
```http
GET /api/prospects
```

**Query Parameters:**
- `min_score`: Minimum prospect score (0-100)
- `max_score`: Maximum prospect score (0-100)
- `island`: Filter by island
- `industry`: Filter by industry
- `technology_readiness`: Filter by tech readiness (Low, Medium, High)
- `priority_level`: Filter by priority (Low, Medium, High)
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "prospects": [
    {
      "id": "uuid",
      "company_id": "uuid",
      "company": {
        "name": "Business Name",
        "website": "https://business.com",
        "island": "Oahu",
        "industry": "Healthcare"
      },
      "score": 85,
      "ai_analysis": "This healthcare practice shows strong potential...",
      "pain_points": [
        "Manual appointment scheduling",
        "Limited patient data insights",
        "Customer service bottlenecks"
      ],
      "recommended_services": ["Data Analytics", "Custom Chatbots"],
      "estimated_deal_value": 75000,
      "technology_readiness": "Medium",
      "priority_level": "High",
      "last_analyzed": "2024-01-15T14:30:00Z"
    }
  ],
  "total": 15,
  "limit": 50,
  "offset": 0
}
```

#### Get Prospect Details
```http
GET /api/prospects/{prospect_id}
```

**Response:**
```json
{
  "id": "uuid",
  "company_id": "uuid", 
  "company": {
    "id": "uuid",
    "name": "Business Name",
    "website": "https://business.com",
    "island": "Oahu",
    "industry": "Healthcare",
    "employee_count_estimate": 25,
    "address": "123 Main St, Honolulu, HI 96814",
    "phone": "(808) 555-0123"
  },
  "decision_makers": [
    {
      "id": "uuid",
      "name": "Dr. John Smith",
      "title": "Owner & Lead Dentist",
      "email": "dr.smith@business.com",
      "phone": "(808) 555-0123"
    }
  ],
  "score": 85,
  "ai_analysis": "**Strategic Analysis for Business Name**\n\n**Business Assessment Score: 85/100**\n\nThis healthcare practice represents an excellent opportunity...",
  "pain_points": [
    "Manual appointment scheduling limiting efficiency",
    "Limited patient data insights for strategic decisions",
    "Customer service bottlenecks during peak hours"
  ],
  "recommended_services": ["Data Analytics", "Custom Chatbots"],
  "estimated_deal_value": 75000,
  "growth_signals": [
    "Established business with 25 employees",
    "Strong online presence with professional website"
  ],
  "technology_readiness": "Medium",
  "priority_level": "High",
  "last_analyzed": "2024-01-15T14:30:00Z"
}
```

#### Update Prospect
```http
PUT /api/prospects/{prospect_id}
```

**Request Body:**
```json
{
  "score": 90,
  "ai_analysis": "Updated analysis...",
  "pain_points": ["Updated pain point 1", "Updated pain point 2"],
  "recommended_services": ["Data Analytics", "Fractional CTO"],
  "estimated_deal_value": 85000,
  "technology_readiness": "High",
  "priority_level": "High"
}
```

### Decision Makers

#### List Decision Makers
```http
GET /api/decision-makers
```

**Query Parameters:**
- `company_id`: Filter by company
- `title`: Filter by title
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "decision_makers": [
    {
      "id": "uuid",
      "company_id": "uuid",
      "company_name": "Business Name",
      "name": "Dr. John Smith",
      "title": "Owner & Lead Dentist", 
      "email": "dr.smith@business.com",
      "phone": "(808) 555-0123",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 19,
  "limit": 50,
  "offset": 0
}
```

#### Get Company Decision Makers
```http
GET /api/companies/{company_id}/decision-makers
```

**Response:**
```json
{
  "decision_makers": [
    {
      "id": "uuid",
      "name": "Dr. John Smith", 
      "title": "Owner & Lead Dentist",
      "email": "dr.smith@business.com",
      "phone": "(808) 555-0123",
      "linkedin_url": null,
      "notes": null,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Decision Maker
```http
POST /api/companies/{company_id}/decision-makers
```

**Request Body:**
```json
{
  "name": "Jane Doe",
  "title": "Operations Manager",
  "email": "jane.doe@business.com", 
  "phone": "(808) 555-0124",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "notes": "Primary contact for operations decisions"
}
```

### Analytics

#### Dashboard Statistics
```http
GET /api/analytics/dashboard
```

**Response:**
```json
{
  "total_companies": 15,
  "total_prospects": 15,
  "total_decision_makers": 19,
  "average_prospect_score": 82.3,
  "high_priority_prospects": 8,
  "island_distribution": {
    "Oahu": 10,
    "Maui": 3,
    "Big Island": 1,
    "Kauai": 1
  },
  "industry_distribution": {
    "Healthcare": 4,
    "Professional Services": 3,
    "Tourism": 3,
    "Food Service": 2,
    "Hospitality": 2,
    "Real Estate": 1
  },
  "service_demand": {
    "Data Analytics": 15,
    "Custom Chatbots": 12,
    "HubSpot Digital Marketing": 8,
    "Fractional CTO": 5
  },
  "technology_readiness": {
    "High": 2,
    "Medium": 11,
    "Low": 2
  }
}
```

#### Island Distribution
```http
GET /api/analytics/islands
```

**Response:**
```json
{
  "islands": [
    {
      "island": "Oahu",
      "company_count": 10,
      "average_score": 83.5,
      "total_deal_value": 750000,
      "top_industry": "Healthcare"
    },
    {
      "island": "Maui", 
      "company_count": 3,
      "average_score": 81.7,
      "total_deal_value": 225000,
      "top_industry": "Tourism"
    }
  ]
}
```

#### Industry Breakdown
```http
GET /api/analytics/industries
```

**Response:**
```json
{
  "industries": [
    {
      "industry": "Healthcare",
      "company_count": 4,
      "average_score": 85.0,
      "total_deal_value": 300000,
      "avg_employee_count": 20,
      "primary_services": ["Data Analytics", "Custom Chatbots"]
    },
    {
      "industry": "Professional Services",
      "company_count": 3, 
      "average_score": 86.0,
      "total_deal_value": 255000,
      "avg_employee_count": 18,
      "primary_services": ["Data Analytics", "HubSpot Digital Marketing"]
    }
  ]
}
```

## Data Collection & Scraping

#### Trigger Data Collection
```http
POST /api/data-collection/trigger
```

**Request Body:**
```json
{
  "source": "google_places",
  "location": "Hawaii",
  "business_types": ["dentist", "restaurant", "cpa", "lawyer"]
}
```

**Response:**
```json
{
  "status": "started",
  "collection_id": "uuid",
  "estimated_completion": "2024-01-15T16:00:00Z"
}
```

#### Get Collection Status
```http
GET /api/data-collection/{collection_id}/status
```

**Response:**
```json
{
  "collection_id": "uuid",
  "status": "completed",
  "started_at": "2024-01-15T15:00:00Z",
  "completed_at": "2024-01-15T15:45:00Z",
  "businesses_found": 25,
  "businesses_imported": 15,
  "errors": []
}
```

## AI Analysis

#### Trigger AI Analysis
```http
POST /api/ai-analysis/analyze/{company_id}
```

**Response:**
```json
{
  "status": "completed",
  "prospect_id": "uuid",
  "analysis": {
    "score": 85,
    "analysis_length": 8500,
    "pain_points_identified": 3,
    "services_recommended": 2,
    "estimated_deal_value": 75000
  }
}
```

#### Bulk AI Analysis
```http
POST /api/ai-analysis/bulk-analyze
```

**Request Body:**
```json
{
  "company_ids": ["uuid1", "uuid2", "uuid3"],
  "force_reanalysis": false
}
```

**Response:**
```json
{
  "status": "started",
  "analysis_job_id": "uuid",
  "companies_to_analyze": 3,
  "estimated_completion": "2024-01-15T16:30:00Z"
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "island",
      "issue": "Must be one of: Oahu, Maui, Big Island, Kauai"
    }
  }
}
```

### Common Error Codes

- `400 BAD_REQUEST`: Invalid request parameters
- `404 NOT_FOUND`: Resource not found
- `422 VALIDATION_ERROR`: Request validation failed
- `429 RATE_LIMIT_EXCEEDED`: Too many requests
- `500 INTERNAL_SERVER_ERROR`: Server error

## Rate Limiting

- **General API**: 100 requests per minute per IP
- **AI Analysis**: 10 requests per minute per IP  
- **Data Collection**: 5 requests per hour per IP

## Usage Examples

### Python Client
```python
import requests

base_url = "http://localhost:8000/api"

# Get high-scoring prospects
response = requests.get(f"{base_url}/prospects?min_score=80")
prospects = response.json()

# Get company with decision makers
response = requests.get(f"{base_url}/companies/{company_id}")
company = response.json()

response = requests.get(f"{base_url}/companies/{company_id}/decision-makers")
decision_makers = response.json()

# Trigger AI analysis
response = requests.post(f"{base_url}/ai-analysis/analyze/{company_id}")
analysis = response.json()
```

### JavaScript Client
```javascript
const baseUrl = 'http://localhost:8000/api';

// Fetch prospects with high scores
const prospects = await fetch(`${baseUrl}/prospects?min_score=80`)
  .then(res => res.json());

// Get island-specific businesses
const oahuBusinesses = await fetch(`${baseUrl}/companies?island=Oahu`)
  .then(res => res.json());

// Get dashboard analytics
const analytics = await fetch(`${baseUrl}/analytics/dashboard`)
  .then(res => res.json());

// Create decision maker
const newDecisionMaker = await fetch(`${baseUrl}/companies/${companyId}/decision-makers`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Smith',
    title: 'CEO',
    email: 'john@company.com',
    phone: '(808) 555-0123'
  })
}).then(res => res.json());
```

## Webhooks (Future)

The system is designed to support webhooks for real-time notifications:

- `company.created`: New company added
- `prospect.analyzed`: AI analysis completed
- `prospect.score_changed`: Prospect score updated
- `decision_maker.added`: New decision maker identified

## Pagination

All list endpoints support pagination:

**Parameters:**
- `limit`: Number of results per page (default: 50, max: 100)
- `offset`: Number of results to skip (default: 0)

**Response includes:**
```json
{
  "data": [...],
  "total": 150,
  "limit": 50,
  "offset": 0,
  "has_next": true,
  "has_previous": false
}
```

## Filtering & Sorting

Most list endpoints support filtering and sorting:

**Filtering:**
- Use query parameters matching field names
- Multiple values: `?industry=Healthcare&industry=Tourism`
- Range queries: `?min_score=70&max_score=90`

**Sorting:**
- `?sort=score`: Ascending order
- `?sort=-score`: Descending order  
- `?sort=score,-created_at`: Multiple fields

## Data Validation

All requests are validated using Pydantic models:

- **Required fields**: Marked as required in schemas
- **Field types**: Strictly enforced (string, integer, datetime, etc.)
- **Enum values**: Limited to predefined choices
- **Format validation**: Email, phone, URL formats validated
- **Range validation**: Scores (0-100), employee counts (positive integers)

---

For additional API questions or feature requests, please create an issue in the repository.