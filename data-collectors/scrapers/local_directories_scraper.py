"""
Local Hawaii Business Directories Scraper
Extracts business data from various local Hawaiian directories and yellow pages
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


class LocalDirectoriesScraper(BaseScraper):
    """Scraper for local Hawaii business directories"""
    
    def __init__(self):
        super().__init__()
        self.directories = [
            {
                'name': 'Hawaii Yellow Pages',
                'base_url': 'https://www.yellowpages.com/',
                'locations': [
                    {'city': 'Honolulu', 'state': 'HI', 'island': 'Oahu'},
                    {'city': 'Kahului', 'state': 'HI', 'island': 'Maui'},
                    {'city': 'Kailua-Kona', 'state': 'HI', 'island': 'Big Island'},
                    {'city': 'Hilo', 'state': 'HI', 'island': 'Big Island'},
                    {'city': 'Lihue', 'state': 'HI', 'island': 'Kauai'},
                    {'city': 'Kaunakakai', 'state': 'HI', 'island': 'Molokai'},
                    {'city': 'Lanai-City', 'state': 'HI', 'island': 'Lanai'}
                ]
            },
            {
                'name': 'Hawaii Business Directory',
                'url': 'https://www.hawaiibusiness.cc/',
                'type': 'general'
            },
            {
                'name': 'Aloha Pages',
                'url': 'https://www.alohapages.com/',
                'type': 'local'
            },
            {
                'name': 'Hawaii 411',
                'url': 'https://www.hawaii411.com/',
                'type': 'local'
            }
        ]
        
        # Categories relevant for AI consulting prospects
        self.target_categories = [
            'restaurants', 'hotels', 'medical-clinics', 'dental-offices',
            'law-firms', 'accounting-firms', 'real-estate-agencies',
            'construction-companies', 'wholesale-distributors',
            'manufacturing', 'retail-stores', 'auto-dealers',
            'property-management', 'insurance-agencies', 'banks'
        ]
        
    def scrape(self) -> List[Dict]:
        """Scrape all local directories"""
        all_companies = []
        
        for directory in self.directories:
            logger.info(f"Scraping {directory['name']}...")
            
            if 'locations' in directory:
                # Location-based directory (Yellow Pages style)
                companies = self._scrape_location_directory(directory)
            else:
                # General directory
                companies = self._scrape_general_directory(directory)
                
            all_companies.extend(companies)
        
        # Remove duplicates
        unique_companies = {}
        for company in all_companies:
            if company['name'] not in unique_companies:
                unique_companies[company['name']] = company
                
        return list(unique_companies.values())
    
    def _scrape_location_directory(self, directory: Dict) -> List[Dict]:
        """Scrape location-based directories like Yellow Pages"""
        companies = []
        
        for location in directory['locations']:
            for category in self.target_categories[:5]:  # Limit categories to avoid overload
                try:
                    # Build search URL
                    search_url = f"{directory['base_url']}search?search_terms={category}&geo_location_terms={location['city']}+{location['state']}"
                    
                    response = self.session.get(search_url, timeout=30)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Extract business listings
                        listings = soup.find_all('div', class_=['result', 'listing', 'business-card'])
                        
                        for listing in listings[:10]:  # Limit per category/location
                            company = self._extract_yellowpages_listing(listing, location)
                            if company:
                                companies.append(company)
                                
                except Exception as e:
                    logger.debug(f"Error scraping {location['city']} {category}: {e}")
                    
        return companies
    
    def _scrape_general_directory(self, directory: Dict) -> List[Dict]:
        """Scrape general Hawaii business directories"""
        companies = []
        
        try:
            response = self.session.get(directory['url'], timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                if directory['name'] == 'Hawaii Business Directory':
                    companies = self._scrape_hawaii_business_cc(soup, directory)
                elif directory['name'] == 'Aloha Pages':
                    companies = self._scrape_aloha_pages(soup, directory)
                elif directory['name'] == 'Hawaii 411':
                    companies = self._scrape_hawaii_411(soup, directory)
                    
        except Exception as e:
            logger.error(f"Error scraping {directory['name']}: {e}")
            
        return companies
    
    def _extract_yellowpages_listing(self, listing, location: Dict) -> Optional[Company]:
        """Extract company from Yellow Pages listing"""
        try:
            # Business name
            name_elem = listing.find(['h2', 'a'], class_=['business-name', 'listing-name'])
            if not name_elem:
                return None
                
            name = self._clean_text(name_elem)
            if not name:
                return None
            
            # Contact info
            address = self._clean_text(listing.find(['div', 'span'], class_=['street-address', 'address']))
            phone = self._clean_text(listing.find(['div', 'span'], class_=['phone', 'phones']))
            
            # Business details
            categories = listing.find_all(['span', 'a'], class_=['category', 'categories'])
            category_text = ' '.join([self._clean_text(cat) for cat in categories])
            
            # Years in business
            years_elem = listing.find(['div', 'span'], class_=['years-in-business', 'experience'])
            years_in_business = self._extract_years(years_elem.text) if years_elem else None
            
            # Website
            website = self._extract_website_from_listing(listing)
            
            # Determine industry
            industry = self.extract_industry(f"{name} {category_text}")
            
            # Estimate size based on listing details
            employee_estimate = self._estimate_size_from_listing(listing, category_text)
            
            company = {
                'name': name,
                'address': address or f"{location['city']}, {location['state']}",
                'island': location['island'],
                'industry': industry,
                'website': website,
                'phone': phone,
                'employee_count_estimate': employee_estimate,
                'annual_revenue_estimate': None,
                'description': f"{category_text}. Established business in {location['city']}.",
                'source': "Yellow Pages Hawaii",
                'source_url': listing.get('href', directory['base_url']),
                'linkedin_url': None,
                'founded_date': self._calculate_founded_date(years_in_business),
                'is_verified': True
            }
            
            return company
            
        except Exception as e:
            logger.debug(f"Error extracting Yellow Pages listing: {e}")
            return None
    
    def _scrape_hawaii_business_cc(self, soup: BeautifulSoup, directory: Dict) -> List[Dict]:
        """Scrape hawaiibusiness.cc directory"""
        companies = []
        
        # Find business listings by category
        categories = soup.find_all('div', class_=['category', 'business-category'])
        
        for category in categories[:10]:  # Limit categories
            category_name = self._clean_text(category.find(['h2', 'h3']))
            
            # Get businesses in this category
            businesses = category.find_all(['div', 'li'], class_=['business', 'listing'])
            
            for business in businesses[:15]:  # Limit per category
                try:
                    name = self._clean_text(business.find(['h3', 'h4', 'a']))
                    if not name:
                        continue
                    
                    # Extract details
                    location = self._clean_text(business.find(['span', 'div'], class_='location'))
                    phone = self._extract_phone(business.text)
                    description = self._clean_text(business.find(['p', 'div'], class_='description'))
                    
                    # Determine island
                    island = self.extract_island(location) if location else 'Oahu'
                    
                    # Industry from category
                    industry = self.extract_industry(f"{category_name} {name}")
                    
                    company = {
                        'name': name,
                        'address': location or "Hawaii",
                        'island': island,
                        'industry': industry,
                        'website': None,
                        'phone': phone,
                        'employee_count_estimate': 15,
                        'annual_revenue_estimate': None,
                        'description': description or f"{category_name} business",
                        'source': directory['name'],
                        'source_url': directory['url'],
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
                except Exception as e:
                    logger.debug(f"Error extracting hawaiibusiness.cc listing: {e}")
                    
        return companies
    
    def _scrape_aloha_pages(self, soup: BeautifulSoup, directory: Dict) -> List[Dict]:
        """Scrape Aloha Pages directory"""
        companies = []
        
        # Find featured businesses and listings
        listings = soup.find_all(['div', 'article'], class_=['business', 'featured', 'listing'])
        
        for listing in listings[:50]:
            try:
                name = self._clean_text(listing.find(['h2', 'h3', 'a']))
                if not name:
                    continue
                
                # Extract info
                info_div = listing.find('div', class_=['info', 'details'])
                if info_div:
                    address = self._clean_text(info_div.find(['p', 'span'], class_='address'))
                    phone = self._clean_text(info_div.find(['p', 'span'], class_='phone'))
                    website = self._extract_website(info_div)
                else:
                    address = None
                    phone = self._extract_phone(listing.text)
                    website = self._extract_website(listing)
                
                # Services/description
                services = self._clean_text(listing.find(['div', 'p'], class_=['services', 'description']))
                
                # Determine island from address
                island = self.extract_island(address) if address else 'Oahu'
                
                # Industry
                industry = self.extract_industry(f"{name} {services or ''}")
                
                company = {
                    'name': name,
                    'address': address or f"{island}, HI",
                    'island': island,
                    'industry': industry,
                    'website': website,
                    'phone': phone,
                    'employee_count_estimate': 20,
                    'annual_revenue_estimate': None,
                    'description': services or "Local Hawaii business",
                    'source': "Aloha Pages",
                    'source_url': directory['url'],
                    'linkedin_url': None,
                    'founded_date': None,
                    'is_verified': True
                }
                
                companies.append(company)
                
            except Exception as e:
                logger.debug(f"Error extracting Aloha Pages listing: {e}")
                
        return companies
    
    def _scrape_hawaii_411(self, soup: BeautifulSoup, directory: Dict) -> List[Dict]:
        """Scrape Hawaii 411 directory"""
        companies = []
        
        # Find business sections
        sections = soup.find_all('div', class_=['section', 'category-section'])
        
        for section in sections[:8]:
            # Get businesses in section
            businesses = section.find_all(['div', 'li'], class_=['business', 'item'])
            
            for business in businesses[:10]:
                try:
                    name = self._clean_text(business.find(['h3', 'a']))
                    if not name:
                        continue
                    
                    # Contact and details
                    contact = business.find('div', class_='contact')
                    if contact:
                        phone = self._extract_phone(contact.text)
                        address = self._clean_text(contact.find(['p', 'span'], class_='address'))
                    else:
                        phone = self._extract_phone(business.text)
                        address = None
                    
                    # Determine location
                    island = self.extract_island(address or business.text) or 'Oahu'
                    
                    # Industry
                    industry = self.extract_industry(name)
                    
                    company = {
                        'name': name,
                        'address': address or f"{island}, HI",
                        'island': island,
                        'industry': industry,
                        'website': None,
                        'phone': phone,
                        'employee_count_estimate': 12,
                        'annual_revenue_estimate': None,
                        'description': "Hawaii 411 listed business",
                        'source': "Hawaii 411",
                        'source_url': directory['url'],
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
                except Exception as e:
                    logger.debug(f"Error extracting Hawaii 411 listing: {e}")
                    
        return companies
    
    def _extract_years(self, text: str) -> Optional[int]:
        """Extract years in business from text"""
        if not text:
            return None
            
        year_match = re.search(r'(\d+)\s*years?', text, re.I)
        if year_match:
            return int(year_match.group(1))
            
        return None
    
    def _calculate_founded_date(self, years_in_business: Optional[int]) -> Optional[str]:
        """Calculate founding year from years in business"""
        if years_in_business:
            current_year = datetime.now().year
            founded_year = current_year - years_in_business
            return str(founded_year)
            
        return None
    
    def _estimate_size_from_listing(self, listing, category: str) -> int:
        """Estimate company size from listing details"""
        text = listing.text.lower()
        category = category.lower() if category else ''
        
        # Look for size indicators
        if any(term in text for term in ['nationwide', 'multiple locations', 'chain']):
            return 100
        elif any(term in text for term in ['established', 'since', 'years']):
            return 25
        elif any(term in category for term in ['restaurant', 'retail', 'store']):
            return 15
        elif any(term in category for term in ['law', 'dental', 'medical', 'clinic']):
            return 10
        elif any(term in category for term in ['consultant', 'freelance', 'independent']):
            return 5
            
        return 15  # Default
    
    def _extract_website_from_listing(self, listing) -> Optional[str]:
        """Extract website from directory listing"""
        # Look for website link
        website_link = listing.find('a', class_=['website', 'url', 'web'])
        if website_link:
            href = website_link.get('href', '')
            if href and href.startswith('http'):
                return href
                
        # Look for "Visit Website" type links
        visit_link = listing.find('a', text=re.compile(r'website|visit|web', re.I))
        if visit_link:
            href = visit_link.get('href', '')
            if href and href.startswith('http'):
                return href
                
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
        if phone_match:
            return phone_match.group(1)
        return None
    
    def _extract_website(self, element) -> Optional[str]:
        """Extract website URL from element"""
        links = element.find_all('a', href=True)
        for link in links:
            href = link.get('href', '')
            if href.startswith('http') and 'directory' not in href and 'yellowpages' not in href:
                return href
        return None