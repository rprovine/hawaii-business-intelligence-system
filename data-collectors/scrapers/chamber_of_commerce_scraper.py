"""
Hawaii Chamber of Commerce Directories Scraper
Extracts member business data from Chamber of Commerce Hawaii directory
"""

import re
import json
from typing import List, Dict, Optional
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, quote
import time

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class ChamberOfCommerceScraper(BaseScraper):
    """Scraper for Hawaii Chamber of Commerce member directory"""
    
    def __init__(self):
        super().__init__()
        # Chamber of Commerce Hawaii directory
        self.base_url = 'https://business.cochawaii.org'
        self.directory_url = f'{self.base_url}/directory'
        self.api_url = f'{self.base_url}/api/v2.2.0/directoryentries/search'
        
        # Categories to search
        self.categories = [
            'Technology', 'Healthcare', 'Tourism', 'Hospitality', 
            'Retail', 'Construction', 'Real Estate', 'Finance',
            'Professional Services', 'Manufacturing', 'Agriculture',
            'Transportation', 'Education', 'Non-Profit'
        ]
        
    def scrape(self) -> List[Dict]:
        """Scrape Chamber of Commerce directory"""
        all_companies = []
        
        try:
            # Try API approach first
            companies = self._scrape_via_api()
            if companies:
                return companies
                
            # Fallback to HTML scraping
            logger.info("API approach failed, trying HTML scraping...")
            
            # Search by category
            for category in self.categories[:5]:  # Limit for testing
                logger.info(f"Searching for {category} businesses...")
                companies = self._search_category(category)
                all_companies.extend(companies)
                time.sleep(2)  # Be respectful
                
            # Also get featured members
            featured = self._get_featured_members()
            all_companies.extend(featured)
            
        except Exception as e:
            logger.error(f"Error scraping Chamber directory: {e}")
            
        # Remove duplicates
        unique_companies = {}
        for company in all_companies:
            if company['name'] not in unique_companies:
                unique_companies[company['name']] = company
                
        return list(unique_companies.values())
    
    def _scrape_via_api(self) -> List[Dict]:
        """Try to scrape using the API endpoint"""
        companies = []
        
        try:
            # API parameters
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': self.session.headers['User-Agent']
            }
            
            # Search parameters
            data = {
                'PageSize': 100,
                'PageNumber': 1,
                'Sort': {'Field': 'Name', 'Direction': 'Ascending'}
            }
            
            response = self.session.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                
                if 'Items' in results:
                    for item in results['Items'][:50]:  # Limit to 50
                        company = self._parse_api_result(item)
                        if company:
                            companies.append(company)
                            
                logger.info(f"Found {len(companies)} companies via API")
                
        except Exception as e:
            logger.debug(f"API scraping failed: {e}")
            
        return companies
    
    def _parse_api_result(self, item: Dict) -> Optional[Dict]:
        """Parse company from API result"""
        try:
            # Extract basic info
            name = item.get('Name', '').strip()
            if not name:
                return None
                
            # Contact info
            address_parts = []
            if item.get('Address1'):
                address_parts.append(item['Address1'])
            if item.get('City'):
                address_parts.append(item['City'])
            if item.get('State'):
                address_parts.append(item['State'])
            if item.get('PostalCode'):
                address_parts.append(item['PostalCode'])
                
            address = ', '.join(address_parts) or 'Hawaii'
            
            # Determine island
            island = self.extract_island(address)
            
            # Industry from categories
            categories = item.get('Categories', [])
            category_names = [cat.get('Name', '') for cat in categories]
            industry = self.extract_industry(' '.join([name] + category_names))
            
            return {
                'name': name,
                'address': address,
                'island': island,
                'industry': industry,
                'website': item.get('Website'),
                'phone': item.get('Phone'),
                'employee_count_estimate': 20,
                'annual_revenue_estimate': None,
                'description': item.get('Description', f"Member of Chamber of Commerce Hawaii"),
                'source': "Chamber of Commerce Hawaii",
                'source_url': f"{self.directory_url}/{item.get('Slug', '')}",
                'linkedin_url': None,
                'founded_date': None,
                'is_verified': True
            }
            
        except Exception as e:
            logger.debug(f"Error parsing API result: {e}")
            return None
    
    def _search_category(self, category: str) -> List[Dict]:
        """Search for businesses in a specific category"""
        companies = []
        
        try:
            # Build search URL
            search_params = f'?category={quote(category)}'
            url = f'{self.directory_url}{search_params}'
            
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find business listings
                # Try different possible selectors
                listings = soup.find_all('div', class_=['gz-card', 'gz-list-card', 'gz-directory-card'])
                
                if not listings:
                    listings = soup.find_all('article', class_='directory-listing')
                    
                if not listings:
                    listings = soup.find_all('div', {'itemtype': 'http://schema.org/LocalBusiness'})
                
                for listing in listings[:20]:  # Limit per category
                    company = self._extract_company_from_listing(listing)
                    if company:
                        companies.append(company)
                        
                logger.info(f"Found {len(companies)} companies in {category}")
                
        except Exception as e:
            logger.debug(f"Error searching category {category}: {e}")
            
        return companies
    
    def _get_featured_members(self) -> List[Dict]:
        """Get featured member businesses"""
        companies = []
        
        try:
            response = self.session.get(self.directory_url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for featured members section
                featured_section = soup.find(['section', 'div'], class_=['featured', 'featured-members'])
                
                if featured_section:
                    listings = featured_section.find_all(['div', 'article'], class_=['member', 'listing'])
                    
                    for listing in listings[:10]:
                        company = self._extract_company_from_listing(listing)
                        if company:
                            companies.append(company)
                            
        except Exception as e:
            logger.debug(f"Error getting featured members: {e}")
            
        return companies
    
    def _extract_company_from_listing(self, listing) -> Optional[Dict]:
        """Extract company information from HTML listing"""
        try:
            # Company name - try multiple selectors
            name = None
            name_selectors = [
                ('h2', {'class': 'gz-card-title'}),
                ('h3', {'class': 'gz-h3'}),
                ('a', {'class': 'gz-card-title'}),
                ('h2', {'itemprop': 'name'}),
                ('span', {'itemprop': 'name'}),
                (['h2', 'h3', 'h4'], None)  # Any heading
            ]
            
            for tag, attrs in name_selectors:
                name_elem = listing.find(tag, attrs)
                if name_elem:
                    name = self._clean_text(name_elem)
                    if name:
                        break
                        
            if not name:
                return None
            
            # Address
            address = None
            address_selectors = [
                ('div', {'class': 'gz-card-address'}),
                ('span', {'itemprop': 'address'}),
                ('div', {'class': 'address'}),
                ('p', {'class': 'location'})
            ]
            
            for tag, attrs in address_selectors:
                addr_elem = listing.find(tag, attrs)
                if addr_elem:
                    address = self._clean_text(addr_elem)
                    if address:
                        break
                        
            if not address:
                # Try to find any text with city names
                text = listing.get_text()
                if 'Honolulu' in text:
                    address = 'Honolulu, HI'
                elif 'Maui' in text:
                    address = 'Maui, HI'
                elif 'Kauai' in text:
                    address = 'Kauai, HI'
                else:
                    address = 'Hawaii'
            
            # Phone
            phone = None
            phone_elem = listing.find(['span', 'a'], {'itemprop': 'telephone'})
            if phone_elem:
                phone = self._clean_text(phone_elem)
            else:
                phone = self._extract_phone(listing.get_text())
            
            # Website
            website = None
            website_elem = listing.find('a', {'itemprop': 'url'})
            if website_elem:
                website = website_elem.get('href')
            else:
                # Look for any external link
                links = listing.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    if href.startswith('http') and 'cochawaii' not in href:
                        website = href
                        break
            
            # Categories/Industry
            category_text = ''
            cat_elem = listing.find(['div', 'span'], class_=['categories', 'gz-card-categories'])
            if cat_elem:
                category_text = self._clean_text(cat_elem)
                
            # Description
            desc_elem = listing.find(['p', 'div'], class_=['description', 'gz-card-excerpt'])
            description = self._clean_text(desc_elem) if desc_elem else None
            
            # Determine island
            island = self.extract_island(address)
            
            # Determine industry
            industry = self.extract_industry(f"{name} {category_text} {description or ''}")
            
            return {
                'name': name,
                'address': address,
                'island': island,
                'industry': industry,
                'website': website,
                'phone': phone,
                'employee_count_estimate': 15,
                'annual_revenue_estimate': None,
                'description': description or f"Member of Chamber of Commerce Hawaii. {category_text}".strip(),
                'source': "Chamber of Commerce Hawaii",
                'source_url': self.directory_url,
                'linkedin_url': None,
                'founded_date': None,
                'is_verified': True
            }
            
        except Exception as e:
            logger.debug(f"Error extracting company from listing: {e}")
            return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        # Hawaii phone patterns
        phone_patterns = [
            r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',  # Standard US
            r'(808[-.\s]?\d{3}[-.\s]?\d{4})',  # 808 area code
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
                
        return None