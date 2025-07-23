#!/usr/bin/env python3
"""
Remove all demo/dummy data from the database
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Prospect, Company

def remove_demo_data():
    """Remove all demo and manual entry data"""
    db = SessionLocal()
    
    try:
        print("Removing demo data...")
        
        # First delete prospects for demo companies
        demo_prospects = db.query(Prospect).join(Company).filter(
            Company.source.in_(['Demo Data', 'Manual Entry'])
        ).all()
        
        print(f"Found {len(demo_prospects)} demo prospects to remove")
        
        for prospect in demo_prospects:
            db.delete(prospect)
        
        # Then delete the companies
        demo_companies = db.query(Company).filter(
            Company.source.in_(['Demo Data', 'Manual Entry'])
        ).all()
        
        print(f"Found {len(demo_companies)} demo companies to remove")
        
        for company in demo_companies:
            db.delete(company)
        
        db.commit()
        print(f"\n✓ Removed {len(demo_prospects)} prospects and {len(demo_companies)} companies")
        
        # Verify
        remaining_companies = db.query(Company).count()
        remaining_prospects = db.query(Prospect).count()
        print(f"\nRemaining in database:")
        print(f"  Companies: {remaining_companies}")
        print(f"  Prospects: {remaining_prospects}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Removing demo/dummy data...")
    print("="*60)
    remove_demo_data()