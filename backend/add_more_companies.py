#!/usr/bin/env python3
"""
Add more real Hawaii companies from the finder
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data-collectors'))

from models.database import SessionLocal
from models.models import Company
from scrapers.hawaii_business_finder import HawaiiBusinessFinder

def add_companies():
    """Add companies from finder to database"""
    db = SessionLocal()
    finder = HawaiiBusinessFinder()
    
    try:
        companies = finder.scrape()
        print(f"Found {len(companies)} companies to add")
        
        added = 0
        for company_data in companies:
            # Check if already exists
            existing = db.query(Company).filter(
                Company.name == company_data['name'],
                Company.island == company_data.get('island', 'Oahu')
            ).first()
            
            if not existing:
                company = Company(
                    name=company_data['name'],
                    address=company_data.get('address', ''),
                    island=company_data.get('island', 'Oahu'),
                    industry=company_data.get('industry', 'Other'),
                    website=company_data.get('website'),
                    phone=company_data.get('phone'),
                    employee_count_estimate=company_data.get('employee_count_estimate'),
                    annual_revenue_estimate=company_data.get('annual_revenue_estimate'),
                    description=company_data.get('description', ''),
                    source=company_data.get('source', 'Web Research'),
                    source_url=company_data.get('source_url')
                )
                db.add(company)
                added += 1
                print(f"✓ Added {company_data['name']}")
            else:
                print(f"- Skipped {company_data['name']} (already exists)")
        
        db.commit()
        print(f"\n✓ Added {added} new companies")
        
        # Show total
        total = db.query(Company).count()
        print(f"Total companies in database: {total}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding more Hawaii companies...")
    print("="*60)
    add_companies()