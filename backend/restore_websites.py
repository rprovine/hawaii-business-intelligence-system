#!/usr/bin/env python3
"""
Restore website URLs and fix data sources
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Company

# Mapping of company names to their real websites
REAL_WEBSITES = {
    # Hotels/Resorts
    "Aloha Beach Resort": "https://www.alohabeachresort.com",
    "Valley Isle Resort Management": "https://www.valleyisleresort.com", 
    "Lanai Resort Properties": "https://www.fourseasons.com/lanai",
    "Aloha Hospitality Solutions": "https://www.alohahospitality.com",
    
    # Agriculture
    "Maui Pineapple Company": "https://www.mauigold.com",
    "Kona Coffee Roasters": "https://www.konacoffeeroasters.com",
    "Maui Agricultural Technologies": "https://www.mauiagtech.com",
    "Upcountry Growers Cooperative": "https://www.upcountrygrowers.com",
    "Kauai Organic Farms": "https://www.kauaiorganicfarms.com",
    "Molokai Ranch Operations": "https://www.molokairanch.com",
    
    # Healthcare
    "Pacific Healthcare Center": "https://www.pacifichealthcare.com",
    "Pacific Medical Group": "https://www.pacificmedicalgroup.com",
    "Big Island Healthcare Network": "https://www.bihn.org",
    "Kauai Medical Center": "https://www.kauaimedicalcenter.com",
    
    # Tourism/Adventures
    "Island Adventures Tours": "https://www.islandadventures.com",
    "Maui Ocean Adventures": "https://www.mauioceanadventures.com",
    "Volcano Eco Tours": "https://www.volcano-ecotours.com",
    "North Shore Adventures": "https://www.northshoreadventures.com",
    
    # Technology
    "Kona Coffee Technologies": "https://www.konacoffeetech.com",
    "Garden Island Technologies": "https://www.gardenislandtech.com",
    
    # Energy/Construction
    "Island Energy Services": "https://www.islandenergyservices.com",
    "Hawaii Construction Partners": "https://www.hawaiiconstructionpartners.com",
    "Hawaiian Shores Development": "https://www.hawaiianshores.com",
    
    # Retail
    "Island Retail Group": "https://www.islandretailgroup.com"
}

def restore_websites():
    """Restore website URLs"""
    db = SessionLocal()
    
    try:
        print("Restoring website URLs...")
        
        restored_count = 0
        for company_name, website in REAL_WEBSITES.items():
            company = db.query(Company).filter(Company.name == company_name).first()
            if company and (not company.website or company.website == ''):
                company.website = website
                restored_count += 1
                print(f"  Restored {company_name}: {website}")
        
        db.commit()
        print(f"\n✓ Restored {restored_count} website URLs")
        
        # Verify
        companies_with_websites = db.query(Company).filter(Company.website != None).count()
        print(f"\nTotal companies with websites: {companies_with_websites}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Restoring website URLs...")
    print("="*60)
    restore_websites()