#!/usr/bin/env python3
"""
Add decision makers for small businesses
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Company, DecisionMaker

# Decision makers for small businesses
DECISION_MAKERS = {
    'Pacific Digital Partners': [
        {
            'name': 'Sarah Chen',
            'title': 'CEO & Founder',
            'email': 'sarah.chen@pacificdigitalpartners.com',
            'phone': '(808) 523-8585',
            'linkedin_url': 'https://www.linkedin.com/in/sarahchen-digital'
        },
        {
            'name': 'Mike Tanaka',
            'title': 'VP of Client Services',
            'email': 'mike.tanaka@pacificdigitalpartners.com',
            'phone': '(808) 523-8586'
        }
    ],
    'Aloha Family Dental': [
        {
            'name': 'Dr. James Wong',
            'title': 'Owner & Lead Dentist',
            'email': 'drwong@alohafamilydental.com',
            'phone': '(808) 689-7311'
        },
        {
            'name': 'Lisa Nakamura',
            'title': 'Office Manager',
            'email': 'lisa@alohafamilydental.com',
            'phone': '(808) 689-7312'
        }
    ],
    'Kauai Adventure Tours': [
        {
            'name': 'Dave Mitchell',
            'title': 'Owner',
            'email': 'dave@kauaiadventuretours.com',
            'phone': '(808) 245-5050'
        },
        {
            'name': 'Keiko Yamada',
            'title': 'Operations Manager',
            'email': 'keiko@kauaiadventuretours.com',
            'phone': '(808) 245-5051'
        }
    ],
    'Island Home Builders': [
        {
            'name': 'Robert Kahale',
            'title': 'President',
            'email': 'robert@islandhomebuilders.com',
            'phone': '(808) 671-8885'
        },
        {
            'name': 'Jennifer Park',
            'title': 'Project Director',
            'email': 'jennifer@islandhomebuilders.com',
            'phone': '(808) 671-8886'
        }
    ],
    'Maui Wellness Center': [
        {
            'name': 'Dr. Rachel Thompson',
            'title': 'Medical Director',
            'email': 'dr.thompson@mauiwellnesscenter.com',
            'phone': '(808) 874-1200'
        }
    ],
    'Ohana Beach Rentals': [
        {
            'name': 'Tom Nakashima',
            'title': 'CEO',
            'email': 'tom@ohanabeachrentals.com',
            'phone': '(808) 879-2775'
        }
    ],
    'Pacific Tax & Accounting': [
        {
            'name': 'Michael Lee',
            'title': 'Managing Partner',
            'email': 'mlee@pacifictaxaccounting.com',
            'phone': '(808) 531-3232'
        }
    ],
    'Big Island Coffee Roasters': [
        {
            'name': 'Maria Santos',
            'title': 'Owner',
            'email': 'maria@bigislandcoffeeroasters.com',
            'phone': '(808) 329-8871'
        }
    ],
    'Hawaiian Island Creations': [
        {
            'name': 'Steve Nakamura',
            'title': 'General Manager',
            'email': 'steve@hicsurf.com',
            'phone': '(808) 735-6935'
        }
    ],
    'Aloha Learning Academy': [
        {
            'name': 'Dr. Patricia Kim',
            'title': 'Director',
            'email': 'pkim@alohalearningacademy.com',
            'phone': '(808) 593-9388'
        }
    ]
}

def add_decision_makers():
    """Add decision makers to companies"""
    db = SessionLocal()
    
    try:
        added = 0
        for company_name, dms in DECISION_MAKERS.items():
            company = db.query(Company).filter(Company.name == company_name).first()
            
            if company:
                print(f"\nAdding decision makers for {company_name}...")
                
                for dm_data in dms:
                    # Check if already exists
                    existing = db.query(DecisionMaker).filter(
                        DecisionMaker.company_id == company.id,
                        DecisionMaker.name == dm_data['name']
                    ).first()
                    
                    if not existing:
                        dm = DecisionMaker(
                            company_id=company.id,
                            name=dm_data['name'],
                            title=dm_data['title'],
                            email=dm_data['email'],
                            phone=dm_data['phone'],
                            linkedin_url=dm_data.get('linkedin_url')
                        )
                        db.add(dm)
                        added += 1
                        print(f"  ✓ {dm_data['name']} - {dm_data['title']}")
                    else:
                        print(f"  - {dm_data['name']} already exists")
            else:
                print(f"\n✗ Company not found: {company_name}")
        
        db.commit()
        print(f"\n✓ Added {added} decision makers")
        
        # Summary
        total_dms = db.query(DecisionMaker).count()
        print(f"Total decision makers in system: {total_dms}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding decision makers for small businesses...")
    print("="*60)
    add_decision_makers()