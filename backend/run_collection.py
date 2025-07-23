#!/usr/bin/env python3
"""
Direct data collection runner that bypasses the broken imports
"""

import os
import sys
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal, engine
from models.models import Company, Prospect, DataCollectionLog
# AI service will be added later

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_sample_businesses():
    """Add sample Hawaii businesses directly"""
    db = SessionLocal()
    
    sample_businesses = [
        {
            'name': 'Aloha Analytics Group',
            'address': '2155 Kalakaua Ave, Suite 420, Honolulu, HI 96815',
            'island': 'Oahu',
            'industry': 'Technology',
            'description': 'Data analytics and business intelligence consulting for Hawaii businesses',
            'employee_count_estimate': 35,
            'website': 'https://example.com/aloha-analytics',
            'phone': '(808) 555-0123'
        },
        {
            'name': 'Pacific Retail Solutions',
            'address': '333 Seaside Ave, Honolulu, HI 96815',
            'island': 'Oahu', 
            'industry': 'Retail',
            'description': 'Multi-location retail chain specializing in Hawaiian products',
            'employee_count_estimate': 85,
            'website': 'https://example.com/pacific-retail',
            'phone': '(808) 555-0124'
        },
        {
            'name': 'Maui Medical Center',
            'address': '221 Mahalani Street, Wailuku, HI 96793',
            'island': 'Maui',
            'industry': 'Healthcare',
            'description': 'Full-service medical facility serving Central Maui',
            'employee_count_estimate': 450,
            'website': 'https://example.com/maui-medical',
            'phone': '(808) 555-0125'
        },
        {
            'name': 'Big Island Solar Co',
            'address': '74-5565 Luhia St, Kailua-Kona, HI 96740',
            'island': 'Big Island',
            'industry': 'Energy',
            'description': 'Renewable energy installations and consulting',
            'employee_count_estimate': 25,
            'website': 'https://example.com/big-island-solar',
            'phone': '(808) 555-0126'
        },
        {
            'name': 'Kauai Adventure Tours',
            'address': '3-4280 Kuhio Hwy, Lihue, HI 96766',
            'island': 'Kauai',
            'industry': 'Tourism',
            'description': 'Eco-tourism and adventure activities across Kauai',
            'employee_count_estimate': 40,
            'website': 'https://example.com/kauai-adventures',
            'phone': '(808) 555-0127'
        }
    ]
    
    added_count = 0
    
    try:
        for biz_data in sample_businesses:
            # Check if company already exists
            existing = db.query(Company).filter_by(name=biz_data['name']).first()
            if existing:
                logger.info(f"Company {biz_data['name']} already exists")
                continue
                
            # Create new company
            company = Company(
                name=biz_data['name'],
                address=biz_data['address'],
                island=biz_data['island'],
                industry=biz_data['industry'],
                website=biz_data.get('website'),
                phone=biz_data.get('phone'),
                employee_count_estimate=biz_data.get('employee_count_estimate'),
                description=biz_data.get('description'),
                source='Sample Data',
                source_url='manual_entry'
            )
            
            db.add(company)
            db.flush()  # Get the ID
            
            # Create prospect with mock AI analysis
            logger.info(f"Creating prospect for {company.name}...")
            
            # Mock AI analysis based on industry
            score = 85 if company.industry in ['Technology', 'Healthcare'] else 75
            if company.employee_count_estimate > 100:
                score += 10
                
            priority = 'High' if score >= 80 else 'Medium'
            deal_value = company.employee_count_estimate * 2000  # Mock calculation
            
            prospect = Prospect(
                company_id=company.id,
                score=score,
                ai_analysis=f"{company.name} is a {company.industry} company in {company.island} with strong potential for digital transformation. Their current size of {company.employee_count_estimate} employees indicates opportunity for scalable solutions.",
                pain_points=['Manual processes', 'Limited data insights', 'Scalability challenges'],
                recommended_services=['Data Analytics', 'Custom Chatbots'] if company.industry == 'Technology' else ['HubSpot Digital Marketing', 'Fractional CTO'],
                estimated_deal_value=deal_value,
                growth_signals=['Expanding operations', 'Growing employee count'],
                technology_readiness='Medium' if company.industry == 'Technology' else 'Low',
                priority_level=priority,
                last_analyzed=datetime.now()
            )
            
            db.add(prospect)
            added_count += 1
            logger.info(f"Added {company.name} with score {score}")
            
        db.commit()
        
        # Log the collection
        log_entry = DataCollectionLog(
            source='Sample Data',
            run_date=datetime.now(),
            records_found=len(sample_businesses),
            records_processed=len(sample_businesses),
            records_added=added_count,
            errors=0,
            duration_seconds=0,
            status='success'
        )
        db.add(log_entry)
        db.commit()
        
        logger.info(f"Successfully added {added_count} new businesses")
        
    except Exception as e:
        logger.error(f"Error adding sample businesses: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Running direct data collection...")
    add_sample_businesses()
    
    # Show current totals
    db = SessionLocal()
    print(f"\nCurrent totals:")
    print(f"Companies: {db.query(Company).count()}")
    print(f"Prospects: {db.query(Prospect).count()}")
    print(f"Collection logs: {db.query(DataCollectionLog).count()}")
    db.close()
    
    print("\n✓ Data collection completed!")
    print("Check your dashboard at http://localhost:3002")