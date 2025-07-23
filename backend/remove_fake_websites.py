#!/usr/bin/env python3
"""
Remove fake websites from fictional companies or set them to None
"""

import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Company

def remove_fake_websites():
    """Remove all fake website URLs"""
    db = SessionLocal()
    
    try:
        companies = db.query(Company).all()
        
        for company in companies:
            if company.website:
                print(f"Removing website from {company.name}: {company.website}")
                company.website = None
        
        db.commit()
        print(f"\n✓ Removed websites from all {len(companies)} fictional companies")
        print("These are fictional prospects - they don't have real websites")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Removing fake websites from fictional companies...")
    print("="*60)
    remove_fake_websites()