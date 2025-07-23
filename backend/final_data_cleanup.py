#!/usr/bin/env python3
"""
Final cleanup - remove businesses with broken websites and ensure data quality
"""

import os
import sys
import requests
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal

def test_website_and_cleanup():
    """Remove businesses with non-working websites"""
    db = SessionLocal()
    
    try:
        # Get all companies
        companies = db.execute(text("""
            SELECT c.id, c.name, c.website, c.phone, c.description,
                   COUNT(p.id) as prospect_count
            FROM companies c
            LEFT JOIN prospects p ON c.id = p.company_id
            GROUP BY c.id, c.name, c.website, c.phone, c.description
        """)).fetchall()
        
        print("Testing all websites for final cleanup...")
        
        working_businesses = []
        broken_businesses = []
        
        for company in companies:
            company_id, name, website, phone, description, prospect_count = company
            
            if not website:
                broken_businesses.append((company_id, name, "No website"))
                continue
            
            try:
                response = requests.head(website, timeout=10, allow_redirects=True)
                if response.status_code < 400:
                    working_businesses.append((company_id, name, website, phone))
                    print(f"✅ {name}: {website}")
                else:
                    broken_businesses.append((company_id, name, f"HTTP {response.status_code}"))
                    print(f"❌ {name}: {website} (Status: {response.status_code})")
            except Exception as e:
                broken_businesses.append((company_id, name, str(e)[:50]))
                print(f"❌ {name}: {website} (Error: {str(e)[:50]})")
        
        print(f"\nResults:")
        print(f"  Working: {len(working_businesses)}")
        print(f"  Broken: {len(broken_businesses)}")
        
        # Remove broken businesses
        if broken_businesses:
            print(f"\nRemoving {len(broken_businesses)} businesses with broken websites...")
            
            for company_id, name, reason in broken_businesses:
                # Delete in order: decision_makers, prospects, companies
                db.execute(text("DELETE FROM decision_makers WHERE company_id = :id"), {'id': company_id})
                db.execute(text("DELETE FROM prospects WHERE company_id = :id"), {'id': company_id})
                db.execute(text("DELETE FROM companies WHERE id = :id"), {'id': company_id})
                print(f"  ❌ Removed {name} ({reason})")
            
            db.commit()
        
        # Final count
        final_count = db.execute(text("SELECT COUNT(*) FROM companies")).fetchone()[0]
        print(f"\n✅ Final database contains {final_count} verified Hawaii businesses")
        
        # Show final business list
        final_businesses = db.execute(text("""
            SELECT name, website, phone, island, industry 
            FROM companies 
            ORDER BY name
        """)).fetchall()
        
        print(f"\n📋 Final Business List:")
        for name, website, phone, island, industry in final_businesses:
            print(f"  • {name}")
            print(f"    Website: {website}")
            print(f"    Phone: {phone}")
            print(f"    Location: {island} | Industry: {industry}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Final data quality cleanup...")
    print("="*60)
    test_website_and_cleanup()