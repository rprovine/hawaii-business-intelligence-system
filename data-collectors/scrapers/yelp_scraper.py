"""
Yelp Hawaii Business Scraper
Extracts real business data from Yelp for Hawaii locations
"""

import re
import json
from typing import List, Optional, Dict
import logging
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlencode

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class YelpScraper(BaseScraper):
    """Scraper for Yelp Hawaii businesses"""
    
    def __init__(self):
        super().__init__("Yelp")
        self.base_url = 'https://www.yelp.com'
        
        # Hawaii locations to search
        self.locations = [
            {'city': 'Honolulu, HI', 'island': 'Oahu'},
            {'city': 'Kahului, HI', 'island': 'Maui'},
            {'city': 'Kailua-Kona, HI', 'island': 'Big Island'},
            {'city': 'Lihue, HI', 'island': 'Kauai'},
            {'city': 'Hilo, HI', 'island': 'Big Island'},
            {'city': 'Wailea, HI', 'island': 'Maui'},
            {'city': 'Princeville, HI', 'island': 'Kauai'}
        ]
        
        # Business categories relevant for AI consulting prospects
        self.categories = [
            'hotels',
            'restaurants', 
            'medicalpractice',
            'dentists',
            'realestate',
            'contractors',
            'lawyers',
            'accountants',
            'automotivesales',
            'gyms',
            'spas',
            'eventservices'
        ]
        
    def scrape(self) -> List[Dict]:
        """Scrape Yelp for Hawaii businesses"""
        all_companies = []
        
        # Limit searches for rate limiting
        for location in self.locations[:3]:  # Start with 3 locations
            for category in self.categories[:4]:  # Start with 4 categories
                logger.info(f"Searching Yelp for {category} in {location['city']}")
                
                try:
                    companies = self._search_location_category(location, category)
                    all_companies.extend(companies)
                    
                    # Be respectful with rate limiting
                    time.sleep(3)
                    
                except Exception as e:
                    logger.error(f"Error searching {category} in {location['city']}: {e}")
                    
        # Remove duplicates
        unique_companies = {}
        for company in all_companies:
            if company.name not in unique_companies:
                unique_companies[company.name] = company
                
        logger.info(f"Found {len(unique_companies)} unique businesses from Yelp")
        return list(unique_companies.values())
    
    def _search_location_category(self, location: dict, category: str) -> List[Dict]:
        """Search for businesses in a specific location and category"""
        companies = []
        
        try:
            # Build search URL
            params = {
                'find_desc': category,
                'find_loc': location['city']
            }
            
            search_url = f"{self.base_url}/search?{urlencode(params)}"
            
            response = self.session.get(search_url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find business listings
                # Yelp uses different structures, try multiple selectors
                listings = soup.find_all('div', {'data-testid': 'serp-ia-card'})
                if not listings:
                    listings = soup.find_all('div', class_='container__09f24__mpR8_')
                if not listings:
                    listings = soup.find_all('li', class_='border-color--default__09f24__NPAKY')
                
                for listing in listings[:10]:  # Limit to 10 per search
                    company = self._extract_company_from_listing(listing, location)
                    if company:
                        companies.append(company)
                        
        except Exception as e:
            logger.debug(f"Error in location/category search: {e}")
            
        return companies
    
    def _extract_company_from_listing(self, listing, location: dict) -> Optional[Dict]:
        """Extract company information from Yelp listing"""
        try:
            # Business name
            name_elem = listing.find('a', class_=['css-1m051bw', 'css-1422juy'])
            if not name_elem:
                name_elem = listing.find('h3')
            if not name_elem:
                name_elem = listing.find('a', {'data-analytics-label': 'biz-name'})
                
            if not name_elem:
                return None
                
            name = self._clean_text(name_elem)
            if not name or 'Sponsored' in name:
                return None
            
            # Skip if it's a chain or franchise (less likely to need AI consulting)
            chain_indicators = ['McDonald', 'Starbucks', 'Subway', 'Pizza Hut', '7-Eleven', 'Walmart']
            if any(chain in name for chain in chain_indicators):
                return None
            
            # Address/Location
            address_elem = listing.find('span', class_=['css-chan6m', 'raw__09f24__T4Ezm'])
            if not address_elem:
                address_elem = listing.find('address')
                
            address = self._clean_text(address_elem) if address_elem else location['city']
            
            # Phone
            phone_elem = listing.find('div', {'data-testid': 'serp-ia-phone'})
            if not phone_elem:
                phone_elem = listing.find('span', class_='css-1p9ibgf')
            phone = self._clean_text(phone_elem) if phone_elem else None
            
            # Category/Industry
            category_elem = listing.find('span', class_=['css-11bijt4', 'priceCategory__09f24__eCihX'])
            category_text = self._clean_text(category_elem) if category_elem else ''
            
            # Reviews count (indicates business size/activity)
            reviews_elem = listing.find('span', class_=['css-chan6m', 'reviewCount__09f24__tnBk4'])
            reviews_text = self._clean_text(reviews_elem) if reviews_elem else '0'
            review_count = self._extract_number(reviews_text)
            
            # Price range (indicates business tier)
            price_elem = listing.find('span', class_='priceRange__09f24__mmOuH')
            price_range = len(price_elem.text.strip()) if price_elem else 2  # $$ default
            
            # Website - Try to get from business page if not in listing
            website = None
            
            # Estimate employee count based on category and reviews
            employee_estimate = self._estimate_employees(category_text, review_count, price_range)
            
            # Determine industry
            industry = self._map_yelp_category_to_industry(category_text, name)
            
            # Build description
            description = f"Active {category_text or 'business'} with {review_count} Yelp reviews. "
            if price_range >= 3:
                description += "Higher-end establishment. "
            
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
                'source': "Yelp",
                'source_url': search_url if 'search_url' in locals() else self.base_url,
                'linkedin_url': None,
                'founded_date': None,
                'is_verified': True
            }
            
        except Exception as e:
            logger.debug(f"Error extracting company from Yelp listing: {e}")
            return None
    
    def _map_yelp_category_to_industry(self, category: str, name: str) -> str:
        """Map Yelp categories to our industry classifications"""
        if not category:
            category = ''
        category = category.lower()
        name = name.lower()
        
        # Check both category and name for industry indicators
        combined = f"{category} {name}"
        
        if any(term in combined for term in ['hotel', 'resort', 'inn', 'motel']):
            return 'Hospitality'
        elif any(term in combined for term in ['restaurant', 'cafe', 'bistro', 'grill', 'kitchen', 'food']):
            return 'Food Service'
        elif any(term in combined for term in ['medical', 'clinic', 'health', 'doctor', 'physician']):
            return 'Healthcare'
        elif any(term in combined for term in ['dental', 'dentist', 'orthodont']):
            return 'Healthcare'
        elif any(term in combined for term in ['real estate', 'realty', 'property']):
            return 'Real Estate'
        elif any(term in combined for term in ['contractor', 'construction', 'builder']):
            return 'Construction'
        elif any(term in combined for term in ['law', 'attorney', 'legal']):
            return 'Professional Services'
        elif any(term in combined for term in ['account', 'cpa', 'tax', 'bookkeep']):
            return 'Professional Services'
        elif any(term in combined for term in ['auto', 'car', 'vehicle', 'dealer']):
            return 'Retail'
        elif any(term in combined for term in ['gym', 'fitness', 'yoga', 'pilates']):
            return 'Healthcare'
        elif any(term in combined for term in ['spa', 'salon', 'beauty']):
            return 'Healthcare'
        elif any(term in combined for term in ['tour', 'activity', 'adventure']):
            return 'Tourism'
        else:
            return 'Other'
    
    def _estimate_employees(self, category: str, review_count: int, price_range: int) -> int:
        """Estimate employee count based on business indicators"""
        base_estimate = 10
        
        # Adjust based on review count (proxy for business activity)
        if review_count > 1000:
            base_estimate = 50
        elif review_count > 500:
            base_estimate = 30
        elif review_count > 200:
            base_estimate = 20
        elif review_count > 50:
            base_estimate = 15
        
        # Adjust based on category
        category = category.lower() if category else ''
        if 'hotel' in category or 'resort' in category:
            base_estimate *= 3
        elif 'restaurant' in category:
            base_estimate = int(base_estimate * 1.5)
        elif 'medical' in category or 'dental' in category:
            base_estimate = int(base_estimate * 1.2)
        
        # Adjust based on price range
        if price_range >= 4:  # $$$$
            base_estimate = int(base_estimate * 1.5)
        elif price_range == 1:  # $
            base_estimate = int(base_estimate * 0.7)
        
        return max(5, base_estimate)  # Minimum 5 employees
    
    def _extract_number(self, text: str) -> int:
        """Extract number from text like '(123 reviews)'"""
        if not text:
            return 0
        
        # Remove commas and find numbers
        text = text.replace(',', '')
        match = re.search(r'(\d+)', text)
        if match:
            return int(match.group(1))
        return 0
    
    def parse_business_info(self, element):
        """Required by base class - parses a business listing element"""
        return self._extract_company_from_listing(element, {})