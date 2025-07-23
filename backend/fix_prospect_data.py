#!/usr/bin/env python3
"""
Fix prospect data issues:
1. Remove placeholder websites
2. Add recommended services
3. Update data sources
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Company, Prospect

def fix_prospect_data():
    """Fix various data issues in prospects"""
    db = SessionLocal()
    
    try:
        # 1. Fix website URLs - remove example.com placeholders
        print("Fixing website URLs...")
        companies = db.query(Company).filter(Company.website.like('%example.com%')).all()
        for company in companies:
            company.website = None  # Better to have no website than a fake one
        print(f"  Fixed {len(companies)} placeholder websites")
        
        # 2. Fix data sources
        print("\nUpdating data sources...")
        source_updates = {
            'Sample Data Generator': 'Demo Data',
            'Sample Data': 'Demo Data'
        }
        
        for old_source, new_source in source_updates.items():
            companies = db.query(Company).filter(Company.source == old_source).all()
            for company in companies:
                company.source = new_source
            print(f"  Updated {len(companies)} companies from '{old_source}' to '{new_source}'")
        
        # 3. Add recommended services to prospects that have none
        print("\nAdding recommended services...")
        prospects = db.query(Prospect).all()
        fixed_count = 0
        
        for prospect in prospects:
            # Check if recommended_services is empty or null
            if not prospect.recommended_services or len(prospect.recommended_services) == 0:
                # Assign services based on industry and score
                company = prospect.company
                services = []
                
                if company.industry in ['Technology', 'Healthcare', 'Retail']:
                    services.append('Data Analytics')
                    if prospect.score >= 80:
                        services.append('Custom Chatbots')
                    
                elif company.industry in ['Hospitality', 'Tourism']:
                    services.append('HubSpot Digital Marketing')
                    if company.employee_count_estimate > 100:
                        services.append('Data Analytics')
                        
                elif company.industry in ['Construction', 'Real Estate']:
                    services.append('Data Analytics')
                    if prospect.score >= 85:
                        services.append('Fractional CTO')
                        
                else:  # Agriculture, Other
                    services.append('Data Analytics')
                    if prospect.technology_readiness == 'Low':
                        services.append('Fractional CTO')
                    else:
                        services.append('Custom Chatbots')
                
                # Ensure unique services
                prospect.recommended_services = list(set(services))
                fixed_count += 1
        
        print(f"  Added services to {fixed_count} prospects")
        
        # 4. Update pain points for prospects without them
        print("\nUpdating pain points...")
        pain_point_count = 0
        for prospect in prospects:
            if not prospect.pain_points or len(prospect.pain_points) == 0:
                # Default pain points based on industry
                if prospect.company.industry == 'Technology':
                    prospect.pain_points = [
                        'Scaling technology infrastructure',
                        'Data silos across departments',
                        'Manual processes slowing growth'
                    ]
                elif prospect.company.industry in ['Hospitality', 'Tourism']:
                    prospect.pain_points = [
                        'Seasonal demand fluctuations',
                        'Guest experience consistency',
                        'Manual booking and customer service processes'
                    ]
                elif prospect.company.industry == 'Healthcare':
                    prospect.pain_points = [
                        'Patient data management',
                        'Appointment scheduling inefficiencies',
                        'Limited patient engagement tools'
                    ]
                else:
                    prospect.pain_points = [
                        'Limited data visibility',
                        'Manual business processes',
                        'Difficulty scaling operations'
                    ]
                pain_point_count += 1
        
        print(f"  Added pain points to {pain_point_count} prospects")
        
        # Commit all changes
        db.commit()
        print("\n✓ All fixes applied successfully!")
        
        # Show summary
        print("\n" + "="*60)
        print("SUMMARY:")
        print(f"Total companies: {db.query(Company).count()}")
        print(f"Companies with websites: {db.query(Company).filter(Company.website != None).count()}")
        print(f"Prospects with services: {db.query(Prospect).filter(Prospect.recommended_services != None).count()}")
        print(f"Demo data sources: {db.query(Company).filter(Company.source == 'Demo Data').count()}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Fixing prospect data issues...")
    print("="*60)
    fix_prospect_data()