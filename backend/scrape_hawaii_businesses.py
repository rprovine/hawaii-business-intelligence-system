#!/usr/bin/env python3
"""
Scrape real Hawaii businesses from public sources
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from sqlalchemy import text
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from services.claude_analyzer import ClaudeBusinessAnalyzer

def clean_phone(phone):
    """Clean phone number to standard format"""
    if not phone:
        return None
    # Remove all non-numeric characters
    numbers = re.sub(r'\D', '', phone)
    if len(numbers) == 10:
        return f"({numbers[:3]}) {numbers[3:6]}-{numbers[6:]}"
    return phone

def scrape_hawaii_chamber():
    """Scrape businesses from Hawaii Chamber of Commerce or similar directories"""
    businesses = []
    
    try:
        # Let's use the Hawaii Business Express search
        # This would normally scrape real data, but for now we'll search for specific businesses
        
        # Search for real Hawaii businesses we can verify exist
        search_terms = [
            "dental honolulu",
            "coffee kona hawaii", 
            "web design maui",
            "construction oahu",
            "wellness kauai",
            "accounting honolulu",
            "tours big island",
            "property management hawaii",
            "restaurant maui",
            "law firm honolulu"
        ]
        
        # For demonstration, I'll fetch from a few known Hawaii business websites
        # In a real implementation, this would scrape business directories
        
        # Example: Let's check some real businesses
        real_businesses_to_check = [
            {
                'url': 'https://www.yelp.com/biz/aloha-dental-group-honolulu',
                'expected_name': 'Aloha Dental Group'
            },
            {
                'url': 'https://www.yelp.com/search?find_desc=coffee&find_loc=Kailua-Kona%2C+HI',
                'expected_name': 'Coffee shops in Kona'
            }
        ]
        
        print("Note: Real web scraping would require handling rate limits, authentication, etc.")
        print("For production use, consider using official APIs or business registries")
        
    except Exception as e:
        print(f"Scraping error: {e}")
    
    return businesses

def fetch_from_google_places(api_key):
    """Fetch real businesses from Google Places API"""
    businesses = []
    
    # Hawaii business search parameters
    locations = [
        {'lat': 21.3099, 'lng': -157.8581, 'island': 'Oahu'},  # Honolulu
        {'lat': 20.7984, 'lng': -156.3319, 'island': 'Maui'},  # Kahului
        {'lat': 19.6400, 'lng': -155.9969, 'island': 'Big Island'},  # Kona
        {'lat': 21.9811, 'lng': -159.3711, 'island': 'Kauai'}  # Lihue
    ]
    
    business_types = [
        'dentist', 'coffee_shop', 'web_design', 'construction_company',
        'wellness_center', 'accounting', 'tour_agency', 'property_management',
        'restaurant', 'law_firm'
    ]
    
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    for location in locations:
        for business_type in business_types:
            params = {
                'location': f"{location['lat']},{location['lng']}",
                'radius': 50000,  # 50km radius
                'type': business_type,
                'key': api_key
            }
            
            try:
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    
                    for place in data.get('results', [])[:2]:  # Get top 2 per category
                        # Get place details
                        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                        details_params = {
                            'place_id': place['place_id'],
                            'fields': 'name,formatted_address,formatted_phone_number,website,types,rating,user_ratings_total',
                            'key': api_key
                        }
                        
                        details_response = requests.get(details_url, params=details_params)
                        if details_response.status_code == 200:
                            details = details_response.json().get('result', {})
                            
                            # Only include businesses with websites
                            if details.get('website'):
                                business = {
                                    'name': details.get('name'),
                                    'address': details.get('formatted_address'),
                                    'phone': details.get('formatted_phone_number'),
                                    'website': details.get('website'),
                                    'island': location['island'],
                                    'types': details.get('types', []),
                                    'rating': details.get('rating'),
                                    'review_count': details.get('user_ratings_total', 0)
                                }
                                businesses.append(business)
                                print(f"Found: {business['name']} - {business['website']}")
                        
                        time.sleep(0.1)  # Rate limiting
                        
            except Exception as e:
                print(f"Error fetching {business_type} in {location['island']}: {e}")
            
            time.sleep(0.5)  # Rate limiting between searches
    
    return businesses

def map_to_industry(types):
    """Map Google Places types to our industry enum"""
    type_string = ' '.join(types).lower()
    
    if any(word in type_string for word in ['dentist', 'doctor', 'medical', 'health', 'clinic']):
        return 'Healthcare'
    elif any(word in type_string for word in ['restaurant', 'food', 'cafe', 'coffee']):
        return 'Food Service'
    elif any(word in type_string for word in ['hotel', 'lodging', 'resort']):
        return 'Hospitality'
    elif any(word in type_string for word in ['tour', 'travel']):
        return 'Tourism'
    elif any(word in type_string for word in ['store', 'shop', 'retail']):
        return 'Retail'
    elif any(word in type_string for word in ['real_estate', 'property']):
        return 'Real Estate'
    elif any(word in type_string for word in ['construction', 'contractor']):
        return 'Construction'
    elif any(word in type_string for word in ['lawyer', 'attorney', 'legal']):
        return 'Professional Services'
    elif any(word in type_string for word in ['accounting', 'finance', 'tax']):
        return 'Professional Services'
    elif any(word in type_string for word in ['technology', 'software', 'web']):
        return 'Technology'
    else:
        return 'Other'

def import_scraped_businesses(businesses):
    """Import scraped businesses into database"""
    db = SessionLocal()
    analyzer = ClaudeBusinessAnalyzer()
    
    try:
        # Clear existing data
        print("\nClearing existing data...")
        db.execute(text("DELETE FROM decision_makers"))
        db.execute(text("DELETE FROM prospects"))
        db.execute(text("DELETE FROM companies"))
        db.commit()
        
        print(f"\nImporting {len(businesses)} real Hawaii businesses...")
        
        imported = 0
        seen_names = set()
        
        for biz in businesses:
            if imported >= 15:  # Limit to 15 businesses
                break
            
            # Skip duplicates and generic entries
            if (biz['name'] in seen_names or 
                biz['name'].lower() in ['honolulu', 'maui', 'kauai', 'hawaii'] or
                'hotel' in biz['name'].lower() and imported > 5):  # Limit hotels
                continue
                
            seen_names.add(biz['name'])
            
            print(f"\n{biz['name']}:")
            
            # Estimate employee count based on review count
            employee_estimate = min(10 + (biz.get('review_count', 0) // 50), 100)
            
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
            
            description = f"Rating: {biz.get('rating', 'N/A')}/5 ({biz.get('review_count', 0)} reviews)"
            
            result = db.execute(company_query, {
                'name': biz['name'],
                'address': biz.get('address', ''),
                'island': biz['island'],
                'industry': map_to_industry(biz.get('types', [])),
                'website': biz['website'],
                'phone': clean_phone(biz.get('phone')),
                'employee_count': employee_estimate,
                'annual_revenue': employee_estimate * 150000,
                'description': description,
                'source': 'Google Places API',
                'source_url': biz['website']
            })
            company_id = result.fetchone()[0]
            print(f"  ✓ Created company (ID: {company_id})")
            print(f"  ✓ Website: {biz['website']}")
            
            # Get AI analysis
            company_data = {
                'name': biz['name'],
                'industry': map_to_industry(biz.get('types', [])),
                'employee_count': employee_estimate,
                'island': biz['island'],
                'description': description,
                'website': biz['website']
            }
            
            analysis_result = analyzer.analyze_business(company_data)
            
            if analysis_result:
                # Map services to valid enums
                valid_services = []
                for service in analysis_result['recommended_services']:
                    if 'data' in service.lower():
                        valid_services.append('Data Analytics')
                    elif 'chatbot' in service.lower():
                        valid_services.append('Custom Chatbots')
                    elif 'marketing' in service.lower():
                        valid_services.append('HubSpot Digital Marketing')
                    elif 'cto' in service.lower():
                        valid_services.append('Fractional CTO')
                
                if not valid_services:
                    valid_services = ['Data Analytics', 'Custom Chatbots']
                
                # Insert prospect
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
            
            # Add a generic decision maker (would need more scraping for real contacts)
            dm_query = text("""
                INSERT INTO decision_makers (
                    company_id, name, title, email, phone
                ) VALUES (
                    :company_id, :name, :title, :email, :phone
                )
            """)
            
            # Create generic contact based on business name
            company_short = biz['name'].lower().replace(' ', '').replace(',', '').replace('.', '')[:20]
            
            db.execute(dm_query, {
                'company_id': company_id,
                'name': f"{biz['name']} Management",
                'title': 'General Manager',
                'email': f"info@{company_short}.com",
                'phone': biz.get('phone', clean_phone(biz.get('phone')))
            })
            print(f"  ✓ Added decision maker")
            
            imported += 1
        
        db.commit()
        print(f"\n✓ Successfully imported {imported} real Hawaii businesses!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function to scrape and import businesses"""
    # Try Google Places API first
    google_api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not google_api_key:
        print("Error: GOOGLE_PLACES_API_KEY not found in environment variables")
        return []
    
    if google_api_key:
        print("Fetching real Hawaii businesses from Google Places...")
        businesses = fetch_from_google_places(google_api_key)
        
        if businesses:
            import_scraped_businesses(businesses)
        else:
            print("No businesses found. Check API key and connection.")
    else:
        print("No Google Places API key found.")
        print("Attempting to scrape from other sources...")
        businesses = scrape_hawaii_chamber()
        
        if businesses:
            import_scraped_businesses(businesses)
        else:
            print("No businesses found from web scraping.")

if __name__ == "__main__":
    print("Starting real Hawaii business scraper...")
    print("="*60)
    main()