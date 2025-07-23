"""
Google Places API Scraper for Hawaii Businesses
Requires Google Places API key to be set in environment variables
"""

import os
import json
from typing import List, Optional, Dict
import logging
import time
import requests
from datetime import datetime

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class GooglePlacesScraper(BaseScraper):
    """Scraper for Google Places API - gets real Hawaii business data"""
    
    def __init__(self):
        super().__init__("Google Places")
        self.api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        self.base_url = 'https://maps.googleapis.com/maps/api/place'
        
        if not self.api_key:
            logger.warning("Google Places API key not found. Set GOOGLE_PLACES_API_KEY environment variable.")
            
        # Hawaii search locations with coordinates
        self.locations = [
            {'name': 'Downtown Honolulu', 'lat': 21.3099, 'lng': -157.8581, 'island': 'Oahu'},
            {'name': 'Waikiki', 'lat': 21.2793, 'lng': -157.8292, 'island': 'Oahu'},
            {'name': 'Kapolei', 'lat': 21.3358, 'lng': -158.0564, 'island': 'Oahu'},
            {'name': 'Kahului', 'lat': 20.8893, 'lng': -156.4729, 'island': 'Maui'},
            {'name': 'Lahaina', 'lat': 20.8783, 'lng': -156.6825, 'island': 'Maui'},
            {'name': 'Kailua-Kona', 'lat': 19.6400, 'lng': -155.9969, 'island': 'Big Island'},
            {'name': 'Hilo', 'lat': 19.7216, 'lng': -155.0847, 'island': 'Big Island'},
            {'name': 'Lihue', 'lat': 21.9811, 'lng': -159.3711, 'island': 'Kauai'},
        ]
        
        # Business types to search for
        self.business_types = [
            'restaurant',
            'hotel',
            'medical_clinic',
            'dental_clinic',
            'law_firm',
            'accounting',
            'real_estate_agency',
            'construction_company',
            'car_dealer',
            'gym',
            'spa',
            'travel_agency'
        ]
        
    def scrape(self) -> List[Dict]:
        """Scrape Google Places for Hawaii businesses"""
        if not self.api_key:
            logger.error("Cannot scrape Google Places without API key")
            return []
            
        all_companies = []
        
        # Search each location for various business types
        for location in self.locations[:3]:  # Limit to conserve API quota
            for business_type in self.business_types[:4]:  # Limit types
                logger.info(f"Searching Google Places for {business_type} near {location['name']}")
                
                try:
                    companies = self._search_nearby(location, business_type)
                    all_companies.extend(companies)
                    
                    # Respect API rate limits
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error searching {business_type} in {location['name']}: {e}")
        
        # Remove duplicates
        unique_companies = {}
        for company in all_companies:
            if company.name not in unique_companies:
                unique_companies[company.name] = company
                
        logger.info(f"Found {len(unique_companies)} unique businesses from Google Places")
        return list(unique_companies.values())
    
    def _search_nearby(self, location: Dict, business_type: str) -> List[Dict]:
        """Search for businesses near a location"""
        companies = []
        
        try:
            # Nearby Search API
            url = f"{self.base_url}/nearbysearch/json"
            params = {
                'location': f"{location['lat']},{location['lng']}",
                'radius': 5000,  # 5km radius
                'type': business_type,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
                    results = data.get('results', [])
                    
                    for place in results[:10]:  # Limit to 10 per search
                        # Get detailed information
                        company = self._get_place_details(place, location)
                        if company:
                            companies.append(company)
                            time.sleep(0.5)  # Rate limiting for details API
                            
                elif data.get('status') == 'ZERO_RESULTS':
                    logger.debug(f"No results for {business_type} in {location['name']}")
                else:
                    logger.error(f"Google Places API error: {data.get('status')}")
                    
        except Exception as e:
            logger.error(f"Error in nearby search: {e}")
            
        return companies
    
    def _get_place_details(self, place: Dict, location: Dict) -> Optional[Dict]:
        """Get detailed information about a place"""
        try:
            place_id = place.get('place_id')
            if not place_id:
                return None
            
            # Skip chains and franchises
            name = place.get('name', '')
            chain_indicators = ['McDonald', 'Starbucks', 'Subway', '7-Eleven', 'Walmart', 'Target']
            if any(chain in name for chain in chain_indicators):
                return None
            
            # Place Details API for more info
            url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,types,price_level',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
                    result = data.get('result', {})
                    
                    # Extract business information
                    name = result.get('name', '')
                    address = result.get('formatted_address', '')
                    phone = result.get('formatted_phone_number')
                    website = result.get('website')
                    rating = result.get('rating', 0)
                    review_count = result.get('user_ratings_total', 0)
                    types = result.get('types', [])
                    price_level = result.get('price_level', 2)
                    
                    # Determine industry
                    industry = self._map_google_types_to_industry(types, name)
                    
                    # Estimate employees
                    employee_estimate = self._estimate_employees_google(types, review_count, price_level)
                    
                    # Build description
                    description = f"Google rating: {rating}/5 ({review_count} reviews). "
                    if types:
                        description += f"Business type: {', '.join(types[:3])}. "
                    
                    return {
                        'name': name,
                        'address': address,
                        'island': location['island'],
                        'industry': industry,
                        'website': website,
                        'phone': phone,
                        'employee_count_estimate': employee_estimate,
                        'annual_revenue_estimate': None,
                        'description': description.strip(),
                        'source': "Google Places",
                        'source_url': f"https://maps.google.com/?q={name}+{address}",
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
        except Exception as e:
            logger.debug(f"Error getting place details: {e}")
            
        return None
    
    def _map_google_types_to_industry(self, types: List[str], name: str) -> str:
        """Map Google Place types to our industry categories"""
        types_str = ' '.join(types).lower()
        name_lower = name.lower()
        
        if any(t in types_str for t in ['lodging', 'hotel', 'resort']):
            return 'Hospitality'
        elif any(t in types_str for t in ['restaurant', 'food', 'cafe', 'bakery']):
            return 'Food Service'
        elif any(t in types_str for t in ['health', 'medical', 'doctor', 'hospital']):
            return 'Healthcare'
        elif any(t in types_str for t in ['dentist', 'dental']):
            return 'Healthcare'
        elif any(t in types_str for t in ['real_estate', 'realty']):
            return 'Real Estate'
        elif any(t in types_str for t in ['construction', 'contractor', 'builder']):
            return 'Construction'
        elif any(t in types_str for t in ['lawyer', 'attorney', 'law']):
            return 'Professional Services'
        elif any(t in types_str for t in ['accounting', 'accountant', 'tax']):
            return 'Professional Services'
        elif any(t in types_str for t in ['car_dealer', 'car_rental', 'auto']):
            return 'Transportation'
        elif any(t in types_str for t in ['gym', 'fitness']):
            return 'Healthcare'
        elif any(t in types_str for t in ['spa', 'beauty']):
            return 'Healthcare'
        elif any(t in types_str for t in ['travel_agency', 'tour']):
            return 'Tourism'
        elif any(t in types_str for t in ['store', 'shop', 'retail']):
            return 'Retail'
        else:
            return 'Other'
    
    def _estimate_employees_google(self, types: List[str], review_count: int, price_level: int) -> int:
        """Estimate employee count based on Google data"""
        base = 10
        
        # Based on review count
        if review_count > 2000:
            base = 75
        elif review_count > 1000:
            base = 50
        elif review_count > 500:
            base = 30
        elif review_count > 200:
            base = 20
        elif review_count > 50:
            base = 15
        
        # Adjust by type
        types_str = ' '.join(types).lower()
        if 'hotel' in types_str or 'resort' in types_str:
            base = int(base * 3)
        elif 'restaurant' in types_str:
            base = int(base * 1.5)
        elif 'medical' in types_str or 'hospital' in types_str:
            base = int(base * 2)
        
        # Adjust by price level (1-4 scale)
        if price_level >= 4:
            base = int(base * 1.5)
        elif price_level == 1:
            base = int(base * 0.7)
        
        return max(5, base)
    
    def parse_business_info(self, element):
        """Required by base class - not used in this implementation"""
        return {}