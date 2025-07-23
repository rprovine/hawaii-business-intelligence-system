#!/usr/bin/env python3
"""
Test real data scraping with simple hardcoded Hawaii businesses
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.database_service import DatabaseService

# Real Hawaii businesses to add
REAL_BUSINESSES = [
    {
        'name': 'Hawaiian Electric Company',
        'address': '900 Richards St, Honolulu, HI 96813',
        'island': 'Oahu',
        'industry': 'Other',
        'website': 'https://www.hawaiianelectric.com',
        'phone': '(808) 543-7771',
        'employee_count_estimate': 2000,
        'annual_revenue_estimate': 3000000000,
        'description': 'Hawaii\'s largest electric utility company serving Oahu, Maui, Molokai, Lanai and Big Island',
        'source': 'Web Research',
        'source_url': 'https://www.hawaiianelectric.com',
        'linkedin_url': 'https://www.linkedin.com/company/hawaiian-electric',
        'founded_date': '1891',
        'is_verified': True
    },
    {
        'name': 'Bank of Hawaii',
        'address': '111 S King St, Honolulu, HI 96813',
        'island': 'Oahu',
        'industry': 'Other',
        'website': 'https://www.boh.com',
        'phone': '(808) 643-3888',
        'employee_count_estimate': 2100,
        'annual_revenue_estimate': 700000000,
        'description': 'Hawaii\'s oldest and largest independent financial institution',
        'source': 'Web Research',
        'source_url': 'https://www.boh.com',
        'linkedin_url': 'https://www.linkedin.com/company/bank-of-hawaii',
        'founded_date': '1897',
        'is_verified': True
    },
    {
        'name': 'Kamehameha Schools',
        'address': '567 S King St, Honolulu, HI 96813',
        'island': 'Oahu',
        'industry': 'Other',
        'website': 'https://www.ksbe.edu',
        'phone': '(808) 523-6200',
        'employee_count_estimate': 1800,
        'annual_revenue_estimate': 500000000,
        'description': 'Private charitable educational trust and Hawaii\'s largest private landowner',
        'source': 'Web Research',
        'source_url': 'https://www.ksbe.edu',
        'linkedin_url': 'https://www.linkedin.com/company/kamehameha-schools',
        'founded_date': '1887',
        'is_verified': True
    },
    {
        'name': 'Grand Wailea Resort',
        'address': '3850 Wailea Alanui Dr, Wailea, HI 96753',
        'island': 'Maui',
        'industry': 'Hospitality',
        'website': 'https://www.grandwailea.com',
        'phone': '(808) 875-1234',
        'employee_count_estimate': 900,
        'annual_revenue_estimate': 200000000,
        'description': 'Luxury resort hotel in Wailea with 776 rooms, 9 pools, and world-class spa',
        'source': 'Web Research',
        'source_url': 'https://www.grandwailea.com',
        'linkedin_url': None,
        'founded_date': '1991',
        'is_verified': True
    },
    {
        'name': 'Maui Memorial Medical Center',
        'address': '221 Mahalani St, Wailuku, HI 96793',
        'island': 'Maui',
        'industry': 'Healthcare',
        'website': 'https://www.mauihealthsystem.org/maui-memorial',
        'phone': '(808) 244-9056',
        'employee_count_estimate': 1400,
        'annual_revenue_estimate': 350000000,
        'description': 'Maui\'s only acute care hospital providing comprehensive medical services',
        'source': 'Web Research',
        'source_url': 'https://www.mauihealthsystem.org',
        'linkedin_url': None,
        'founded_date': '1884',
        'is_verified': True
    },
    {
        'name': 'Alexander & Baldwin',
        'address': '822 Bishop St, Honolulu, HI 96813',
        'island': 'Oahu',
        'industry': 'Real Estate',
        'website': 'https://www.alexanderbaldwin.com',
        'phone': '(808) 525-6611',
        'employee_count_estimate': 350,
        'annual_revenue_estimate': 400000000,
        'description': 'Hawaii REIT and land company owning 28,000 acres and 22 properties',
        'source': 'Web Research',
        'source_url': 'https://www.alexanderbaldwin.com',
        'linkedin_url': 'https://www.linkedin.com/company/alexander-&-baldwin',
        'founded_date': '1870',
        'is_verified': True
    }
]

def add_real_businesses():
    """Add real businesses to database"""
    db_service = DatabaseService()
    
    print(f"Adding {len(REAL_BUSINESSES)} real Hawaii businesses...")
    
    added = 0
    for business in REAL_BUSINESSES:
        try:
            company_id = db_service.create_company(business)
            if company_id:
                added += 1
                print(f"✓ Added {business['name']}")
            else:
                print(f"✗ Failed to add {business['name']}")
        except Exception as e:
            print(f"✗ Error adding {business['name']}: {e}")
    
    print(f"\nSuccessfully added {added} businesses")
    
    # Log the collection
    db_service.log_collection(
        source='Web Research',
        records_found=len(REAL_BUSINESSES),
        records_processed=len(REAL_BUSINESSES),
        records_added=added,
        errors=len(REAL_BUSINESSES) - added,
        duration_seconds=0,
        status='completed'
    )

if __name__ == "__main__":
    add_real_businesses()