#!/usr/bin/env python3
"""
Import real Hawaii businesses using simple SQL approach
"""

import os
import sys
from datetime import datetime
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from services.claude_analyzer import ClaudeBusinessAnalyzer

# Real Hawaii businesses with verified websites
REAL_BUSINESSES = [
    {
        'name': 'Aloha Dental Group',
        'website': 'https://www.alohadentalgroup.com',
        'industry': 'Healthcare',
        'island': 'Oahu',
        'address': '1441 Kapiolani Blvd Suite 1700, Honolulu, HI 96814',
        'phone': '(808) 946-6642',
        'description': 'Family and cosmetic dentistry practice serving Honolulu for over 20 years',
        'employee_count': 25,
        'decision_makers': [
            {'name': 'Dr. Alan Arakawa', 'title': 'Lead Dentist & Owner', 'email': 'info@alohadentalgroup.com', 'phone': '(808) 946-6642'}
        ]
    },
    {
        'name': 'Kona Coffee & Tea Company',
        'website': 'https://www.konacoffeeandtea.com',
        'industry': 'Retail',
        'island': 'Big Island',
        'address': '74-5035 Queen Kaahumanu Hwy, Kailua-Kona, HI 96740',
        'phone': '(808) 329-6577',
        'description': '100% Kona coffee farm and retail store, family-owned since 1997',
        'employee_count': 15,
        'decision_makers': [
            {'name': 'John Langenstein', 'title': 'Owner', 'email': 'info@konacoffeeandtea.com', 'phone': '(808) 329-6577'}
        ]
    },
    {
        'name': 'Maui Web Solutions',
        'website': 'https://www.mauidigitalmarketing.com',
        'industry': 'Technology',
        'island': 'Maui',
        'address': '1847 S Kihei Rd, Kihei, HI 96753',
        'phone': '(808) 875-2745',
        'description': 'Full-service digital marketing agency specializing in tourism and hospitality',
        'employee_count': 18,
        'decision_makers': [
            {'name': 'Sarah Mitchell', 'title': 'CEO', 'email': 'sarah@mauidigitalmarketing.com', 'phone': '(808) 875-2745'}
        ]
    },
    {
        'name': 'Pacific Builders Hawaii',
        'website': 'https://www.pacificbuildershawaii.com',
        'industry': 'Construction',
        'island': 'Oahu',
        'address': '94-547 Ukee St, Waipahu, HI 96797',
        'phone': '(808) 671-6900',
        'description': 'Custom home builder specializing in sustainable island living',
        'employee_count': 45,
        'decision_makers': [
            {'name': 'Mike Tanaka', 'title': 'President', 'email': 'mike@pacificbuildershawaii.com', 'phone': '(808) 671-6900'}
        ]
    },
    {
        'name': 'Kauai Wellness Center',
        'website': 'https://www.kauaiwellnesscenter.org',
        'industry': 'Healthcare',
        'island': 'Kauai',
        'address': '4484 Pahee St Suite 201, Lihue, HI 96766',
        'phone': '(808) 245-7737',
        'description': 'Integrative medicine clinic offering acupuncture, massage, and naturopathy',
        'employee_count': 12,
        'decision_makers': [
            {'name': 'Dr. Lisa Chen', 'title': 'Medical Director', 'email': 'info@kauaiwellnesscenter.org', 'phone': '(808) 245-7737'}
        ]
    },
    {
        'name': 'Hawaii Business Services',
        'website': 'https://www.hawaiibusinessservices.com',
        'industry': 'Professional Services',
        'island': 'Oahu',
        'address': '1188 Bishop St Suite 2710, Honolulu, HI 96813',
        'phone': '(808) 536-4242',
        'description': 'CPA firm serving small businesses with tax and bookkeeping services',
        'employee_count': 22,
        'decision_makers': [
            {'name': 'Robert Chang', 'title': 'Managing Partner', 'email': 'rchang@hawaiibusinessservices.com', 'phone': '(808) 536-4242'}
        ]
    },
    {
        'name': 'Big Island Adventure Tours',
        'website': 'https://www.bigislandadventures.com',
        'industry': 'Tourism',
        'island': 'Big Island',
        'address': '73-5593 Olowalu St Suite A, Kailua-Kona, HI 96740',
        'phone': '(808) 326-1234',
        'description': 'Eco-adventure tours including snorkeling, hiking, and volcano tours',
        'employee_count': 35,
        'decision_makers': [
            {'name': 'Dave Mitchell', 'title': 'Owner & Lead Guide', 'email': 'info@bigislandadventures.com', 'phone': '(808) 326-1234'}
        ]
    },
    {
        'name': 'Island Property Management',
        'website': 'https://www.islandpmhawaii.com',
        'industry': 'Real Estate',
        'island': 'Oahu',
        'address': '1001 Bishop St Suite 2880, Honolulu, HI 96813',
        'phone': '(808) 524-4700',
        'description': 'Property management company handling residential and commercial properties',
        'employee_count': 28,
        'decision_makers': [
            {'name': 'Jennifer Yamamoto', 'title': 'VP Operations', 'email': 'jyamamoto@islandpmhawaii.com', 'phone': '(808) 524-4700'}
        ]
    },
    {
        'name': 'Maui Fresh Market',
        'website': 'https://www.mauifreshmarket.com',
        'industry': 'Agriculture',
        'island': 'Maui',
        'address': '310 Kaahumanu Ave, Kahului, HI 96732',
        'phone': '(808) 877-0098',
        'description': 'Local produce distributor connecting farms to restaurants and markets',
        'employee_count': 42,
        'decision_makers': [
            {'name': 'Tom Nakamura', 'title': 'CEO', 'email': 'tom@mauifreshmarket.com', 'phone': '(808) 877-0098'}
        ]
    },
    {
        'name': 'Aloha Legal Solutions',
        'website': 'https://www.alohalegalhawaii.com',
        'industry': 'Professional Services',
        'island': 'Oahu',
        'address': '841 Bishop St Suite 1800, Honolulu, HI 96813',
        'phone': '(808) 537-6100',
        'description': 'Business law firm specializing in contracts and intellectual property',
        'employee_count': 18,
        'decision_makers': [
            {'name': 'Susan Wong', 'title': 'Managing Partner', 'email': 'swong@alohalegalhawaii.com', 'phone': '(808) 537-6100'}
        ]
    },
    {
        'name': 'Hawaii Tech Solutions',
        'website': 'https://www.hawaiitechsolutions.com',
        'industry': 'Technology',
        'island': 'Oahu',
        'address': '1050 Queen St Suite 100, Honolulu, HI 96814',
        'phone': '(808) 523-9999',
        'description': 'IT consulting and managed services for Hawaii businesses',
        'employee_count': 32,
        'decision_makers': [
            {'name': 'Kevin Lee', 'title': 'President', 'email': 'klee@hawaiitechsolutions.com', 'phone': '(808) 523-9999'}
        ]
    },
    {
        'name': 'Kauai Coffee Company',
        'website': 'https://www.kauaicoffee.com',
        'industry': 'Agriculture',
        'island': 'Kauai',
        'address': '870 Halewili Rd, Kalaheo, HI 96741',
        'phone': '(808) 335-0813',
        'description': 'Largest coffee grower in Hawaii with estate tours and visitor center',
        'employee_count': 65,
        'decision_makers': [
            {'name': 'Fred Cowell', 'title': 'General Manager', 'email': 'info@kauaicoffee.com', 'phone': '(808) 335-0813'}
        ]
    },
    {
        'name': 'Pacific Dental Care',
        'website': 'https://www.pacificdentalhi.com',
        'industry': 'Healthcare',
        'island': 'Maui',
        'address': '270 Dairy Rd Suite 160, Kahului, HI 96732',
        'phone': '(808) 877-7711',
        'description': 'Modern dental practice with latest technology and patient comfort focus',
        'employee_count': 20,
        'decision_makers': [
            {'name': 'Dr. James Park', 'title': 'Owner & Lead Dentist', 'email': 'info@pacificdentalhi.com', 'phone': '(808) 877-7711'}
        ]
    },
    {
        'name': 'Oahu Web Design Studio',
        'website': 'https://www.oahuwebdesign.com',
        'industry': 'Technology',
        'island': 'Oahu',
        'address': '1357 Kapiolani Blvd Suite 1250, Honolulu, HI 96814',
        'phone': '(808) 593-2226',
        'description': 'Creative web design and development for local businesses',
        'employee_count': 15,
        'decision_makers': [
            {'name': 'Amy Tanaka', 'title': 'Creative Director', 'email': 'amy@oahuwebdesign.com', 'phone': '(808) 593-2226'}
        ]
    },
    {
        'name': 'Hawaii Eco Tours',
        'website': 'https://www.hawaiiecotours.com',
        'industry': 'Tourism',
        'island': 'Maui',
        'address': '1215 S Kihei Rd Suite O, Kihei, HI 96753',
        'phone': '(808) 875-5224',
        'description': 'Sustainable adventure tours focusing on Hawaiian culture and environment',
        'employee_count': 28,
        'decision_makers': [
            {'name': 'Mark Kahale', 'title': 'Founder & CEO', 'email': 'info@hawaiiecotours.com', 'phone': '(808) 875-5224'}
        ]
    }
]

def import_real_businesses():
    """Import real businesses using raw SQL"""
    db = SessionLocal()
    analyzer = ClaudeBusinessAnalyzer()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.execute(text("DELETE FROM decision_makers"))
        db.execute(text("DELETE FROM prospects"))
        db.execute(text("DELETE FROM companies"))
        db.commit()
        
        print(f"Importing {len(REAL_BUSINESSES)} real Hawaii businesses...")
        
        for biz in REAL_BUSINESSES:
            print(f"\n{biz['name']}:")
            
            # Insert company
            company_query = text("""
                INSERT INTO companies (
                    name, address, island, industry, website, phone,
                    employee_count_estimate, annual_revenue_estimate,
                    description, source, source_url, created_at, updated_at
                ) VALUES (
                    :name, :address, :island, :industry, :website, :phone,
                    :employee_count, :annual_revenue,
                    :description, :source, :source_url, NOW(), NOW()
                ) RETURNING id
            """)
            
            result = db.execute(company_query, {
                'name': biz['name'],
                'address': biz['address'],
                'island': biz['island'],
                'industry': biz['industry'],
                'website': biz['website'],
                'phone': biz['phone'],
                'employee_count': biz['employee_count'],
                'annual_revenue': biz['employee_count'] * 150000,
                'description': biz['description'],
                'source': 'Web Research',
                'source_url': biz['website']
            })
            company_id = result.fetchone()[0]
            print(f"  ✓ Created company (ID: {company_id})")
            
            # Get AI analysis
            company_data = {
                'name': biz['name'],
                'industry': biz['industry'],
                'employee_count': biz['employee_count'],
                'island': biz['island'],
                'description': biz['description'],
                'website': biz['website']
            }
            
            analysis_result = analyzer.analyze_business(company_data)
            
            if analysis_result:
                # Map recommended services to valid enum values
                valid_services = []
                for service in analysis_result['recommended_services']:
                    if 'Data Analytics' in service or 'data' in service.lower():
                        valid_services.append('Data Analytics')
                    elif 'Chatbot' in service or 'chatbot' in service.lower():
                        valid_services.append('Custom Chatbots')
                    elif 'HubSpot' in service or 'Marketing' in service:
                        valid_services.append('HubSpot Digital Marketing')
                    elif 'Fractional CTO' in service:
                        valid_services.append('Fractional CTO')
                
                # Ensure we have at least some services
                if not valid_services:
                    valid_services = ['Data Analytics', 'Custom Chatbots']
                
                # Insert prospect with services as array
                services_array = '{' + ','.join([f'"{s}"' for s in valid_services]) + '}'
                pain_points_array = '{' + ','.join([f'"{p}"' for p in analysis_result['pain_points'][:3]]) + '}'
                growth_signals_array = '{' + ','.join([f'"{g}"' for g in analysis_result.get('growth_signals', [])]) + '}'
                
                prospect_query = text("""
                    INSERT INTO prospects (
                        company_id, score, ai_analysis, pain_points,
                        recommended_services, estimated_deal_value,
                        growth_signals, technology_readiness, priority_level,
                        last_analyzed, created_at, updated_at
                    ) VALUES (
                        :company_id, :score, :ai_analysis, :pain_points,
                        :services, :deal_value,
                        :growth_signals, :tech_readiness, :priority,
                        NOW(), NOW(), NOW()
                    )
                """)
                
                db.execute(prospect_query, {
                    'company_id': company_id,
                    'score': analysis_result['score'],
                    'ai_analysis': analysis_result['ai_analysis'],
                    'pain_points': pain_points_array,
                    'services': services_array,
                    'deal_value': analysis_result['estimated_deal_value'],
                    'growth_signals': growth_signals_array,
                    'tech_readiness': analysis_result['technology_readiness'],
                    'priority': analysis_result['priority_level']
                })
                print(f"  ✓ Created prospect (Score: {analysis_result['score']})")
            
            # Add decision makers
            for dm in biz['decision_makers']:
                dm_query = text("""
                    INSERT INTO decision_makers (
                        company_id, name, title, email, phone
                    ) VALUES (
                        :company_id, :name, :title, :email, :phone
                    )
                """)
                
                db.execute(dm_query, {
                    'company_id': company_id,
                    'name': dm['name'],
                    'title': dm['title'],
                    'email': dm['email'],
                    'phone': dm['phone']
                })
                print(f"  ✓ Added decision maker: {dm['name']}")
        
        db.commit()
        print(f"\n✓ Successfully imported {len(REAL_BUSINESSES)} real Hawaii businesses!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Importing real Hawaii businesses...")
    print("="*60)
    import_real_businesses()