#!/usr/bin/env python3
"""
Fix prospects with empty recommended services arrays
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Prospect, ServiceEnum

def fix_empty_services():
    """Fix prospects with empty service arrays"""
    db = SessionLocal()
    
    try:
        # Get all prospects
        prospects = db.query(Prospect).all()
        print(f"Checking {len(prospects)} prospects for empty services...")
        
        fixed_count = 0
        for prospect in prospects:
            # Check if services is empty (not None, but empty array)
            if prospect.recommended_services is not None and len(prospect.recommended_services) == 0:
                company = prospect.company
                services = []
                
                # Assign services based on industry and score
                if company.industry in ['Technology', 'Healthcare', 'Retail']:
                    services.append(ServiceEnum.DATA_ANALYTICS)
                    if prospect.score >= 80:
                        services.append(ServiceEnum.CUSTOM_CHATBOTS)
                    
                elif company.industry in ['Hospitality', 'Tourism']:
                    services.append(ServiceEnum.HUBSPOT_MARKETING)
                    if company.employee_count_estimate and company.employee_count_estimate > 100:
                        services.append(ServiceEnum.DATA_ANALYTICS)
                        
                elif company.industry in ['Construction', 'Real Estate']:
                    services.append(ServiceEnum.DATA_ANALYTICS)
                    if prospect.score >= 85:
                        services.append(ServiceEnum.FRACTIONAL_CTO)
                        
                else:  # Agriculture, Other
                    services.append(ServiceEnum.DATA_ANALYTICS)
                    if prospect.technology_readiness == 'Low':
                        services.append(ServiceEnum.FRACTIONAL_CTO)
                    else:
                        services.append(ServiceEnum.CUSTOM_CHATBOTS)
                
                # Update the prospect with enum values
                prospect.recommended_services = list(set(services))
                fixed_count += 1
                print(f"  Fixed {company.name}: {[s.value for s in services]}")
        
        db.commit()
        print(f"\n✓ Fixed {fixed_count} prospects with empty services")
        
        # Verify the fix
        print("\nVerification:")
        empty_count = 0
        for prospect in db.query(Prospect).all():
            if not prospect.recommended_services or len(prospect.recommended_services) == 0:
                empty_count += 1
        
        print(f"Prospects with services: {len(prospects) - empty_count}")
        print(f"Prospects without services: {empty_count}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Fixing empty recommended services...")
    print("="*60)
    fix_empty_services()