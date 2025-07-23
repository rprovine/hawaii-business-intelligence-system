"""
Hawaii Tourism Authority and Tourism Industry Scraper
Extracts tourism-related business data from HTA and tourism directories
"""

import re
import json
from typing import List, Dict, Optional
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import requests

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class HawaiiTourismScraper(BaseScraper):
    """Scraper for Hawaii tourism industry businesses"""
    
    def __init__(self):
        super().__init__()
        self.sources = [
            {
                'name': 'Hawaii Tourism Authority',
                'url': 'https://www.hawaiitourismauthority.org/',
                'type': 'official'
            },
            {
                'name': 'Go Hawaii - Official Tourism Site',
                'url': 'https://www.gohawaii.com/',
                'type': 'directory'
            },
            {
                'name': 'Hawaii Hotels Association',
                'url': 'https://www.hawaiihotels.org/',
                'type': 'association'
            },
            {
                'name': 'Hawaii Ecotourism Association',
                'url': 'https://www.hawaiiecotourism.org/',
                'type': 'specialty'
            }
        ]
        
    def scrape(self) -> List[Dict]:
        """Scrape all tourism sources"""
        all_companies = []
        
        for source in self.sources:
            logger.info(f"Scraping {source['name']}...")
            companies = self._scrape_source(source)
            all_companies.extend(companies)
        
        # Also scrape specific tourism business types
        tourism_categories = [
            'hotels', 'resorts', 'tours', 'activities', 
            'transportation', 'restaurants', 'attractions'
        ]
        
        for category in tourism_categories:
            companies = self._scrape_tourism_category(category)
            all_companies.extend(companies)
        
        # Remove duplicates
        unique_companies = {}
        for company in all_companies:
            if company['name'] not in unique_companies:
                unique_companies[company['name']] = company
                
        return list(unique_companies.values())
    
    def _scrape_source(self, source: Dict) -> List[Dict]:
        """Scrape a specific tourism source"""
        companies = []
        
        try:
            if source['type'] == 'official':
                companies = self._scrape_hta_members(source)
            elif source['type'] == 'directory':
                companies = self._scrape_gohawaii(source)
            elif source['type'] == 'association':
                companies = self._scrape_hotel_association(source)
            elif source['type'] == 'specialty':
                companies = self._scrape_ecotourism(source)
                
        except Exception as e:
            logger.error(f"Error scraping {source['name']}: {e}")
            
        return companies
    
    def _scrape_hta_members(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Tourism Authority member/partner listings"""
        companies = []
        
        try:
            # HTA lists major tourism partners and members
            response = self.session.get(f"{source['url']}/industry/members", timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find member listings
                members = soup.find_all(['div', 'li'], class_=['member', 'partner', 'listing'])
                
                for member in members[:30]:
                    name = self._clean_text(member.find(['h3', 'h4', 'a']))
                    if not name:
                        continue
                    
                    # Extract details
                    island = self._extract_island_from_text(member.text)
                    website = self._extract_website(member)
                    description = self._clean_text(member.find(['p', 'div'], class_='description'))
                    
                    company = {
                        'name': name,
                        'address': f"{island}, HI" if island else "Hawaii",
                        'island': island or 'Oahu',
                        'industry': 'Tourism',
                        'website': website,
                        'phone': None,
                        'employee_count_estimate': 50,  # HTA partners are typically larger
                        'annual_revenue_estimate': None,
                        'description': description or "Hawaii Tourism Authority partner",
                        'source': "Hawaii Tourism Authority",
                        'source_url': source['url'],
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping HTA: {e}")
            
        return companies
    
    def _scrape_gohawaii(self, source: Dict) -> List[Dict]:
        """Scrape Go Hawaii tourism directory"""
        companies = []
        
        # Go Hawaii has listings by island and category
        islands = ['oahu', 'maui', 'kauai', 'big-island', 'molokai', 'lanai']
        categories = ['hotels-resorts', 'activities', 'dining', 'shopping']
        
        for island in islands:
            for category in categories:
                try:
                    url = f"{source['url']}/{island}/{category}"
                    response = self.session.get(url, timeout=30)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Find business listings
                        listings = soup.find_all(['div', 'article'], class_=['listing', 'business', 'item'])
                        
                        for listing in listings[:10]:  # Limit per category/island
                            name = self._clean_text(listing.find(['h2', 'h3', 'a']))
                            if not name:
                                continue
                            
                            # Map URL island to our island enum
                            island_map = {
                                'oahu': 'Oahu',
                                'maui': 'Maui',
                                'kauai': 'Kauai',
                                'big-island': 'Big Island',
                                'molokai': 'Molokai',
                                'lanai': 'Lanai'
                            }
                            
                            location = self._clean_text(listing.find(['span', 'div'], class_='location'))
                            phone = self._extract_phone(listing.text)
                            website = self._extract_website(listing)
                            
                            # Determine specific tourism industry
                            if 'hotel' in category or 'resort' in category:
                                industry = 'Hospitality'
                            elif 'dining' in category or 'restaurant' in category:
                                industry = 'Food Service'
                            else:
                                industry = 'Tourism'
                            
                            company = {
                                'name': name,
                                'address': location or f"{island_map.get(island, 'Oahu')}, HI",
                                'island': island_map.get(island, 'Oahu'),
                                'industry': industry,
                                'website': website,
                                'phone': phone,
                                'employee_count_estimate': 25,
                                'annual_revenue_estimate': None,
                                'description': f"{category.replace('-', ' ').title()} business on {island_map.get(island, 'Oahu')}",
                                'source': "Go Hawaii",
                                'source_url': url,
                                'linkedin_url': None,
                                'founded_date': None,
                                'is_verified': True
                            }
                            
                            companies.append(company)
                            
                except Exception as e:
                    logger.debug(f"Error scraping Go Hawaii {island}/{category}: {e}")
                    
        return companies
    
    def _scrape_hotel_association(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Hotels Association members"""
        companies = []
        
        try:
            response = self.session.get(f"{source['url']}/members", timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find hotel member listings
                hotels = soup.find_all(['div', 'li'], class_=['member', 'hotel', 'property'])
                
                for hotel in hotels[:40]:
                    name = self._clean_text(hotel.find(['h3', 'a']))
                    if not name:
                        continue
                    
                    # Extract hotel details
                    location = self._clean_text(hotel.find(['span', 'div'], class_='location'))
                    island = self.extract_island(location) if location else 'Oahu'
                    rooms = self._extract_room_count(hotel.text)
                    
                    # Estimate employees based on room count
                    employee_estimate = max(50, rooms * 2) if rooms else 100
                    
                    company = {
                        'name': name,
                        'address': location or f"{island}, HI",
                        'island': island,
                        'industry': 'Hospitality',
                        'website': self._extract_website(hotel),
                        'phone': self._extract_phone(hotel.text),
                        'employee_count_estimate': employee_estimate,
                        'annual_revenue_estimate': None,
                        'description': f"Hotel/Resort with {rooms} rooms" if rooms else "Hotel/Resort property",
                        'source': "Hawaii Hotels Association",
                        'source_url': source['url'],
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping Hotels Association: {e}")
            
        return companies
    
    def _scrape_ecotourism(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Ecotourism Association members"""
        companies = []
        
        try:
            response = self.session.get(source['url'], timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find eco-tour operators
                operators = soup.find_all(['div', 'article'], class_=['member', 'operator', 'business'])
                
                for operator in operators[:25]:
                    name = self._clean_text(operator.find(['h3', 'a']))
                    if not name:
                        continue
                    
                    # Extract details
                    activities = self._clean_text(operator.find(['div', 'p'], class_=['activities', 'services']))
                    location = self._clean_text(operator.find(['span', 'div'], class_='location'))
                    island = self.extract_island(location) if location else self._determine_island_from_activities(activities)
                    
                    company = {
                        'name': name,
                        'address': location or f"{island}, HI",
                        'island': island,
                        'industry': 'Tourism',
                        'website': self._extract_website(operator),
                        'phone': self._extract_phone(operator.text),
                        'employee_count_estimate': 15,  # Eco-tours typically smaller operations
                        'annual_revenue_estimate': None,
                        'description': f"Eco-tourism operator. {activities or 'Sustainable tourism activities'}",
                        'source': "Hawaii Ecotourism Association",
                        'source_url': source['url'],
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping Ecotourism Association: {e}")
            
        return companies
    
    def _scrape_tourism_category(self, category: str) -> List[Dict]:
        """Scrape specific tourism category businesses"""
        companies = []
        
        # Search for tourism businesses by category
        search_urls = {
            'hotels': 'https://www.hawaii-hotels.com/',
            'tours': 'https://www.hawaii-activities.com/',
            'restaurants': 'https://www.opentable.com/hawaii',
            'attractions': 'https://www.viator.com/Hawaii/d669'
        }
        
        # Implement basic scraping for each category
        # This is a simplified version - real implementation would be more detailed
        
        return companies
    
    def _extract_island_from_text(self, text: str) -> Optional[str]:
        """Extract island name from text"""
        if not text:
            return None
            
        text = text.lower()
        island_keywords = {
            'oahu': ['oahu', 'honolulu', 'waikiki', 'pearl harbor'],
            'maui': ['maui', 'lahaina', 'kihei', 'haleakala'],
            'big island': ['big island', 'hawaii island', 'kona', 'hilo', 'kailua-kona'],
            'kauai': ['kauai', 'lihue', 'poipu', 'princeville'],
            'molokai': ['molokai'],
            'lanai': ['lanai']
        }
        
        for island, keywords in island_keywords.items():
            if any(keyword in text for keyword in keywords):
                return island.title()
                
        return None
    
    def _extract_room_count(self, text: str) -> Optional[int]:
        """Extract number of rooms from text"""
        room_match = re.search(r'(\d+)\s*(?:rooms?|suites?|units?)', text, re.I)
        if room_match:
            return int(room_match.group(1))
        return None
    
    def _determine_island_from_activities(self, activities: str) -> str:
        """Determine island based on activity descriptions"""
        if not activities:
            return 'Oahu'
            
        activities = activities.lower()
        
        # Island-specific activities
        if 'pearl harbor' in activities or 'diamond head' in activities:
            return 'Oahu'
        elif 'haleakala' in activities or 'road to hana' in activities:
            return 'Maui'
        elif 'volcano' in activities or 'mauna kea' in activities:
            return 'Big Island'
        elif 'napali' in activities or 'waimea canyon' in activities:
            return 'Kauai'
            
        return 'Oahu'  # Default
    
    def _extract_website(self, element) -> Optional[str]:
        """Extract website URL from element"""
        # Look for website links
        website_link = element.find('a', href=re.compile(r'^https?://(?!.*(?:hawaii|tourism|association))', re.I))
        if website_link:
            return website_link.get('href')
            
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
        if phone_match:
            return phone_match.group(1)
        return None