from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import Company, Prospect, IslandEnum, IndustryEnum
from datetime import datetime

router = APIRouter()

@router.post("/create-sample-data")
async def create_sample_data(db: Session = Depends(get_db)):
    """Create sample data for testing"""
    
    # Sample companies
    companies_data = [
        {
            "name": "Aloha Beach Resort",
            "address": "123 Kalakaua Ave, Honolulu, HI 96815",
            "island": "Oahu",
            "industry": "Hospitality",
            "website": "https://alohabeachresort.com",
            "phone": "(808) 555-0123",
            "employee_count_estimate": 150,
            "annual_revenue_estimate": 25000000,
            "description": "Premier beachfront resort in Waikiki offering luxury accommodations",
            "source": "Manual Entry"
        },
        {
            "name": "Maui Pineapple Company",
            "address": "456 Hana Highway, Kahului, HI 96732",
            "island": "Maui",
            "industry": "Agriculture",
            "website": "https://mauipineapple.com",
            "phone": "(808) 555-0456",
            "employee_count_estimate": 200,
            "annual_revenue_estimate": 15000000,
            "description": "Leading pineapple grower and exporter in Hawaii",
            "source": "Manual Entry"
        },
        {
            "name": "Kona Coffee Roasters",
            "address": "789 Ali'i Drive, Kailua-Kona, HI 96740",
            "island": "Big Island",
            "industry": "Agriculture",
            "website": "https://konacoffeeroasters.com",
            "phone": "(808) 555-0789",
            "employee_count_estimate": 75,
            "annual_revenue_estimate": 8000000,
            "description": "Premium Kona coffee producer and distributor",
            "source": "Manual Entry"
        },
        {
            "name": "Pacific Healthcare Center",
            "address": "321 Ala Moana Blvd, Honolulu, HI 96813",
            "island": "Oahu",
            "industry": "Healthcare",
            "website": "https://pacifichealthcare.com",
            "phone": "(808) 555-0321",
            "employee_count_estimate": 500,
            "annual_revenue_estimate": 75000000,
            "description": "Multi-specialty medical center serving Oahu residents",
            "source": "Manual Entry"
        },
        {
            "name": "Island Adventures Tours",
            "address": "567 Front St, Lahaina, HI 96761",
            "island": "Maui",
            "industry": "Tourism",
            "website": "https://islandadventures.com",
            "phone": "(808) 555-0567",
            "employee_count_estimate": 50,
            "annual_revenue_estimate": 5000000,
            "description": "Adventure tour operator offering snorkeling, hiking, and helicopter tours",
            "source": "Manual Entry"
        }
    ]
    
    created_companies = []
    
    for company_data in companies_data:
        # Check if company already exists
        existing = db.query(Company).filter(
            Company.name == company_data["name"],
            Company.island == company_data["island"]
        ).first()
        
        if not existing:
            company = Company(**company_data)
            db.add(company)
            db.commit()
            db.refresh(company)
            
            # Create prospect with mock scores
            prospect = Prospect(
                company_id=company.id,
                score=75 + (company.id % 25),  # Score between 75-99
                ai_analysis="This company shows strong potential for our services based on their growth trajectory and current technology needs.",
                pain_points=["Outdated technology infrastructure", "Manual processes", "Limited data insights"],
                recommended_services=["Data Analytics", "Custom Chatbots"],
                estimated_deal_value=50000 + (company.id * 10000),
                growth_signals=["Expanding operations", "Hiring new staff"],
                technology_readiness="Medium",
                priority_level="High" if (75 + (company.id % 25)) >= 80 else "Medium",
                last_analyzed=datetime.utcnow()
            )
            db.add(prospect)
            db.commit()
            
            created_companies.append(company.name)
    
    return {
        "message": f"Created {len(created_companies)} sample companies with prospects",
        "companies": created_companies
    }