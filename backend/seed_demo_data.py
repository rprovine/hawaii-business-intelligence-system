#!/usr/bin/env python3
"""
Seed database with demo data for Hawaii Business Intelligence System
"""

import os
import sys
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.database import Base
from models.models import Company, Prospect, DecisionMaker, DataCollectionLog, IndustryEnum, IslandEnum, ServiceEnum

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hbi_user:your_secure_password@localhost:5432/hawaii_business_intel")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Demo companies data - realistic Hawaii businesses
DEMO_COMPANIES = [
    {
        "name": "Aloha Medical Center",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.HEALTHCARE,
        "website": "https://alohamedicalcenter.com",
        "address": "1380 Lusitana Street, Suite 808, Honolulu, HI 96813",
        "phone": "(808) 555-4200",
        "employee_count_estimate": 450,
        "description": "Premier healthcare facility serving Oahu with comprehensive medical services including emergency care, surgical services, and specialized treatments.",
        "services_offered": "Emergency Care, Surgery, Cardiology, Oncology, Pediatrics, Imaging Services"
    },
    {
        "name": "Pacific Paradise Resort & Spa",
        "island": IslandEnum.MAUI,
        "industry": IndustryEnum.TOURISM,
        "website": "https://pacificparadiseresort.com",
        "address": "3900 Wailea Alanui Drive, Wailea, HI 96753",
        "phone": "(808) 555-7800",
        "employee_count_estimate": 320,
        "description": "Luxury beachfront resort featuring world-class amenities, spa services, and multiple dining options on Maui's pristine shores.",
        "services_offered": "Luxury Accommodations, Spa Services, Fine Dining, Event Hosting, Water Sports"
    },
    {
        "name": "Kona Coffee Collective",
        "island": IslandEnum.BIG_ISLAND,
        "industry": IndustryEnum.FOOD_SERVICE,
        "website": "https://konacoffeecollective.com",
        "address": "75-5799 Alii Drive, Kailua-Kona, HI 96740",
        "phone": "(808) 555-3600",
        "employee_count_estimate": 85,
        "description": "Award-winning coffee roaster and distributor specializing in authentic Kona coffee, with farm tours and tasting experiences.",
        "services_offered": "Coffee Roasting, Wholesale Distribution, Farm Tours, Coffee Tasting, Online Sales"
    },
    {
        "name": "Island Tech Solutions",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.PROFESSIONAL_SERVICES,
        "website": "https://islandtechsolutions.com",
        "address": "1001 Bishop Street, Suite 2800, Honolulu, HI 96813",
        "phone": "(808) 555-9100",
        "employee_count_estimate": 150,
        "description": "Leading IT consulting firm providing cloud solutions, cybersecurity, and digital transformation services to Hawaii businesses.",
        "services_offered": "Cloud Migration, Cybersecurity, IT Consulting, Software Development, Managed Services"
    },
    {
        "name": "Kauai Adventure Tours",
        "island": IslandEnum.KAUAI,
        "industry": IndustryEnum.TOURISM,
        "website": "https://kauaiadventuretours.com",
        "address": "3-4280 Kuhio Highway, Lihue, HI 96766",
        "phone": "(808) 555-2400",
        "employee_count_estimate": 65,
        "description": "Premier adventure tour operator offering helicopter tours, snorkeling, hiking, and zip-lining experiences across the Garden Isle.",
        "services_offered": "Helicopter Tours, Snorkeling Expeditions, Hiking Tours, Zip-lining, Kayaking"
    },
    {
        "name": "Honolulu Construction Group",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.REAL_ESTATE,
        "website": "https://honoluluconstruction.com",
        "address": "91-110 Hanua Street, Kapolei, HI 96707",
        "phone": "(808) 555-6700",
        "employee_count_estimate": 280,
        "description": "Full-service construction company specializing in commercial development, residential projects, and infrastructure improvements.",
        "services_offered": "Commercial Construction, Residential Development, Infrastructure, Project Management"
    },
    {
        "name": "Ohana Dental Care",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.HEALTHCARE,
        "website": "https://ohanadentalcare.com",
        "address": "1441 Kapiolani Boulevard, Suite 1700, Honolulu, HI 96814",
        "phone": "(808) 555-3200",
        "employee_count_estimate": 45,
        "description": "Family-friendly dental practice offering comprehensive dental services with a focus on preventive care and patient comfort.",
        "services_offered": "General Dentistry, Cosmetic Dentistry, Orthodontics, Oral Surgery, Pediatric Care"
    },
    {
        "name": "Maui Ocean Center Marine Institute",
        "island": IslandEnum.MAUI,
        "industry": IndustryEnum.TOURISM,
        "website": "https://mauioceancenter.com",
        "address": "192 Ma'alaea Road, Wailuku, HI 96793",
        "phone": "(808) 555-8900",
        "employee_count_estimate": 120,
        "description": "Hawaii's premier aquarium and marine science center featuring native Hawaiian marine life and educational programs.",
        "services_offered": "Marine Exhibits, Educational Programs, Conservation Research, Event Hosting"
    },
    {
        "name": "Rainbow Drive-In",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.FOOD_SERVICE,
        "website": "https://rainbowdrivein.com",
        "address": "3308 Kanaina Avenue, Honolulu, HI 96815",
        "phone": "(808) 555-1500",
        "employee_count_estimate": 35,
        "description": "Iconic local plate lunch restaurant serving traditional Hawaiian comfort food since 1961.",
        "services_offered": "Plate Lunches, Catering, Takeout, Local Hawaiian Cuisine"
    },
    {
        "name": "Big Island Legal Associates",
        "island": IslandEnum.BIG_ISLAND,
        "industry": IndustryEnum.PROFESSIONAL_SERVICES,
        "website": "https://bigislandlegal.com",
        "address": "75-170 Hualalai Road, Suite B204, Kailua-Kona, HI 96740",
        "phone": "(808) 555-4800",
        "employee_count_estimate": 28,
        "description": "Full-service law firm specializing in real estate, business law, and estate planning for Big Island residents and businesses.",
        "services_offered": "Real Estate Law, Business Law, Estate Planning, Litigation, Contract Services"
    },
    {
        "name": "Aloha Fitness & Wellness",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.HEALTHCARE,
        "website": "https://alohafitnesswellness.com",
        "address": "4211 Waialae Avenue, Suite 305, Honolulu, HI 96816",
        "phone": "(808) 555-7300",
        "employee_count_estimate": 55,
        "description": "Comprehensive fitness center offering personal training, group classes, nutrition counseling, and wellness programs.",
        "services_offered": "Personal Training, Group Fitness, Nutrition Counseling, Spa Services, Wellness Programs"
    },
    {
        "name": "Kauai Fresh Farms",
        "island": IslandEnum.KAUAI,
        "industry": IndustryEnum.FOOD_SERVICE,
        "website": "https://kauaifreshfarms.com",
        "address": "4-1345 Kuhio Highway, Kapaa, HI 96746",
        "phone": "(808) 555-6200",
        "employee_count_estimate": 40,
        "description": "Organic farm and farmers market supplier providing fresh local produce to restaurants and retailers across Kauai.",
        "services_offered": "Organic Farming, Wholesale Distribution, Farmers Markets, Farm Tours"
    },
    {
        "name": "Pacific Accounting Partners",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.PROFESSIONAL_SERVICES,
        "website": "https://pacificaccounting.com",
        "address": "999 Bishop Street, Suite 1800, Honolulu, HI 96813",
        "phone": "(808) 555-5500",
        "employee_count_estimate": 75,
        "description": "Leading CPA firm providing tax preparation, audit services, and financial consulting to Hawaii businesses.",
        "services_offered": "Tax Preparation, Audit Services, Financial Consulting, Bookkeeping, Business Advisory"
    },
    {
        "name": "Maui Solar Solutions",
        "island": IslandEnum.MAUI,
        "industry": IndustryEnum.REAL_ESTATE,
        "website": "https://mauisolarsolutions.com",
        "address": "444 Hana Highway, Suite 210, Kahului, HI 96732",
        "phone": "(808) 555-8100",
        "employee_count_estimate": 95,
        "description": "Renewable energy company specializing in solar panel installation and energy storage solutions for residential and commercial properties.",
        "services_offered": "Solar Installation, Energy Storage, Maintenance, Energy Consulting"
    },
    {
        "name": "Island Imports & Gifts",
        "island": IslandEnum.OAHU,
        "industry": IndustryEnum.RETAIL,
        "website": "https://islandimportsgifts.com",
        "address": "2330 Kalakaua Avenue, Honolulu, HI 96815",
        "phone": "(808) 555-2900",
        "employee_count_estimate": 25,
        "description": "Specialty retail store featuring authentic Hawaiian crafts, jewelry, and gifts from local artisans.",
        "services_offered": "Retail Sales, Online Shopping, Custom Orders, Gift Wrapping, Shipping Services"
    }
]

# AI-generated analysis templates
AI_ANALYSIS_TEMPLATES = [
    {
        "score": 85,
        "analysis": """Strategic AI Opportunity Assessment:

This business represents a HIGH-VALUE opportunity for LeniLani Consulting's AI solutions. Key indicators:

1. OPERATIONAL COMPLEXITY: Multiple service lines and locations create data silos perfect for AI integration
2. CUSTOMER VOLUME: High daily customer interactions ideal for chatbot implementation
3. DATA RICHNESS: Extensive operational data suitable for predictive analytics
4. COMPETITIVE PRESSURE: Industry competition demands innovation for differentiation

Recommended Approach:
- Lead with Custom Chatbot solution for immediate ROI (24/7 customer service)
- Follow with Data Analytics platform for operational insights
- Position Fractional CTO services for long-term digital transformation

Hawaii Market Context: Strong local reputation provides trust foundation for AI adoption. Inter-island operations could benefit from centralized AI-driven coordination.""",
        "pain_points": [
            "Manual customer service causing response delays",
            "Inconsistent data across multiple systems",
            "Limited predictive capabilities for demand forecasting",
            "Inefficient resource allocation"
        ],
        "recommended_services": ["Custom Chatbots", "Data Analytics"],
        "estimated_deal_value": 125000
    },
    {
        "score": 72,
        "analysis": """Strategic AI Opportunity Assessment:

This business shows MODERATE-TO-HIGH potential for AI implementation with clear pain points:

1. CUSTOMER ENGAGEMENT: Current manual processes limit scalability
2. OPERATIONAL EFFICIENCY: Multiple inefficiencies in daily operations
3. MARKET POSITION: Mid-tier player could leverage AI for competitive advantage
4. GROWTH TRAJECTORY: Expansion plans align with digital transformation needs

Immediate Opportunities:
- HubSpot Digital Marketing for automated customer journeys
- Data Analytics for business intelligence and KPI tracking
- Custom Chatbot for lead qualification and customer support

Cultural Fit: Family-owned business values align with LeniLani's relationship-first approach. Emphasize local success stories and gradual implementation.""",
        "pain_points": [
            "Limited marketing automation capabilities",
            "Manual lead tracking and follow-up",
            "Lack of customer behavior insights",
            "Time-consuming administrative tasks"
        ],
        "recommended_services": ["HubSpot Digital Marketing", "Data Analytics"],
        "estimated_deal_value": 75000
    },
    {
        "score": 68,
        "analysis": """Strategic AI Opportunity Assessment:

MODERATE opportunity with specific AI use cases that deliver measurable ROI:

1. SERVICE DELIVERY: Current processes could be enhanced with AI automation
2. CUSTOMER RETENTION: Lack of predictive analytics for customer churn
3. OPERATIONAL DATA: Underutilized data assets with analytics potential
4. STAFF PRODUCTIVITY: Manual tasks consuming valuable employee time

Strategic Recommendations:
- Start with Data Analytics for quick wins in operational efficiency
- Implement Custom Chatbot for customer FAQs and appointment scheduling
- Consider Fractional CTO for technology strategy development

Local Market Advantage: Understanding of Hawaii business culture and 'Aloha Spirit' provides trust advantage over mainland competitors.""",
        "pain_points": [
            "Reactive rather than proactive customer service",
            "Limited visibility into business metrics",
            "Manual scheduling and coordination",
            "Difficulty tracking customer satisfaction"
        ],
        "recommended_services": ["Data Analytics", "Custom Chatbots"],
        "estimated_deal_value": 55000
    }
]

# Decision maker templates
DECISION_MAKERS = [
    {"first_name": "James", "last_name": "Tanaka", "title": "CEO", "email_suffix": "ceo"},
    {"first_name": "Maria", "last_name": "Santos", "title": "President", "email_suffix": "president"},
    {"first_name": "David", "last_name": "Kim", "title": "COO", "email_suffix": "operations"},
    {"first_name": "Sarah", "last_name": "Johnson", "title": "CFO", "email_suffix": "cfo"},
    {"first_name": "Michael", "last_name": "Lee", "title": "VP Operations", "email_suffix": "vp.ops"},
    {"first_name": "Lisa", "last_name": "Chen", "title": "Director of Technology", "email_suffix": "tech"},
    {"first_name": "Robert", "last_name": "Yamamoto", "title": "General Manager", "email_suffix": "gm"},
    {"first_name": "Jennifer", "last_name": "Park", "title": "Marketing Director", "email_suffix": "marketing"},
]

def seed_data():
    """Seed the database with demo data"""
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(DecisionMaker).delete()
        db.query(Prospect).delete()
        db.query(Company).delete()
        db.commit()
        
        # Seed companies and related data
        print("Seeding companies...")
        for i, company_data in enumerate(DEMO_COMPANIES):
            # Create company
            company = Company(
                name=company_data["name"],
                website=company_data["website"],
                island=company_data["island"],
                industry=company_data["industry"],
                address=company_data["address"],
                phone=company_data["phone"],
                employee_count_estimate=company_data["employee_count_estimate"],
                description=company_data["description"],
                source="Demo Seed",
                source_url=company_data["website"],
                annual_revenue_estimate=random.randint(1000000, 50000000),
                created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
                updated_at=datetime.now()
            )
            db.add(company)
            db.commit()
            
            # Create prospect analysis
            analysis = random.choice(AI_ANALYSIS_TEMPLATES)
            prospect = Prospect(
                company_id=company.id,
                score=analysis["score"] + random.randint(-5, 5),  # Add some variation
                ai_analysis=analysis["analysis"],
                pain_points=analysis["pain_points"],
                recommended_services=analysis["recommended_services"],
                estimated_deal_value=analysis["estimated_deal_value"] + random.randint(-10000, 20000),
                technology_readiness=random.choice(["Low", "Medium", "High"]),
                created_at=datetime.now() - timedelta(days=random.randint(1, 15)),
                updated_at=datetime.now(),
                priority_level="High" if analysis["score"] >= 80 else "Medium",
                growth_signals=["Digital transformation initiative", "Recent funding", "Expanding operations"]
            )
            db.add(prospect)
            
            # Create 1-3 decision makers per company
            num_decision_makers = random.randint(1, 3)
            selected_dms = random.sample(DECISION_MAKERS, num_decision_makers)
            
            for dm_template in selected_dms:
                # Extract domain from website
                domain = company_data["website"].replace("https://", "").replace("http://", "")
                
                decision_maker = DecisionMaker(
                    company_id=company.id,
                    name=f"{dm_template['first_name']} {dm_template['last_name']}",
                    title=dm_template["title"],
                    email=f"{dm_template['email_suffix']}@{domain}",
                    phone=company_data["phone"],
                    linkedin_url=f"https://linkedin.com/in/{dm_template['first_name'].lower()}-{dm_template['last_name'].lower()}-hawaii",
                    is_primary=dm_template["title"] in ["CEO", "President", "Owner"]
                )
                db.add(decision_maker)
            
            db.commit()
            print(f"  ✓ Added {company.name} with prospect analysis and {num_decision_makers} decision makers")
        
        # Get summary stats
        total_companies = db.query(Company).count()
        total_prospects = db.query(Prospect).count()
        total_decision_makers = db.query(DecisionMaker).count()
        high_score_prospects = db.query(Prospect).filter(Prospect.score >= 80).count()
        
        print("\n" + "="*50)
        print("DEMO DATA SEEDED SUCCESSFULLY!")
        print("="*50)
        print(f"✓ Companies: {total_companies}")
        print(f"✓ Prospects: {total_prospects}")
        print(f"✓ Decision Makers: {total_decision_makers}")
        print(f"✓ High-Score Prospects (80+): {high_score_prospects}")
        print("\nYour dashboard should now show this data!")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting demo data seed...")
    seed_data()