#!/usr/bin/env python3
"""
Add small Hawaii businesses - simple version
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data-collectors'))

from models.database import SessionLocal
from models.models import Company
from scrapers.small_business_finder import SmallBusinessFinder

def add_companies():
    """Add small businesses"""
    db = SessionLocal()
    finder = SmallBusinessFinder()
    
    try:
        companies = finder.scrape()
        print(f"Adding {len(companies)} small businesses...")
        
        added = 0
        for company_data in companies:
            try:
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
                    source=company_data.get('source', 'Small Business Directory'),
                    source_url=company_data.get('source_url')
                )
                db.add(company)
                added += 1
                print(f"✓ {company_data['name']} ({company_data['employee_count_estimate']} employees)")
            except Exception as e:
                print(f"✗ Error adding {company_data['name']}: {e}")
        
        db.commit()
        print(f"\n✓ Added {added} companies")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_companies()