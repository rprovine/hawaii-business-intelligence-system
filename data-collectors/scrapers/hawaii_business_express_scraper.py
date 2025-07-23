"""
Hawaii Business Express (HBE) Scraper
Extracts business registration data from Hawaii's official business portal
"""

import re
import json
from typing import List, Dict, Optional
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, quote

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class HawaiiBusinessExpressScraper(BaseScraper):
    """Scraper for Hawaii Business Express - State business registrations"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://hbe.hawaii.gov"
        self.search_url = "https://hbe.hawaii.gov/documents/search.html"
        
    def scrape(self) -> List[Dict]:
        """Scrape business registrations from Hawaii Business Express"""
        companies = []
        
        try:
            # Search for recently registered businesses
            # HBE requires specific search parameters
            search_terms = [
                "LLC", "Corporation", "Inc", "Corp", "Limited",
                "Partnership", "LP", "LLP", "Services", "Solutions"
            ]
            
            for term in search_terms:
                logger.info(f"Searching Hawaii Business Express for: {term}")
                results = self._search_businesses(term)
                companies.extend(results)
                
            # Remove duplicates based on name
            unique_companies = {}
            for company in companies:
                if company['name'] not in unique_companies:
                    unique_companies[company['name']] = company
                    
            return list(unique_companies.values())
            
        except Exception as e:
            logger.error(f"Error scraping Hawaii Business Express: {e}")
            return []
    
    def _search_businesses(self, search_term: str) -> List[Dict]:
        """Search for businesses with specific term"""
        companies = []
        
        try:
            # HBE uses a form-based search
            search_data = {
                'searchTerm': search_term,
                'searchType': 'entityName',
                'searchSubType': 'contains',
                'statusType': 'active'  # Only active businesses
            }
            
            response = self.session.post(
                self.search_url,
                data=search_data,
                timeout=30
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find business entries in search results
                business_entries = soup.find_all('div', class_='search-result-item')
                if not business_entries:
                    # Try alternative structure
                    business_entries = soup.find_all('tr', class_='result-row')
                
                for entry in business_entries[:20]:  # Limit to 20 per search
                    company = self._extract_company_info(entry)
                    if company:
                        companies.append(company)
                        
        except Exception as e:
            logger.error(f"Error searching for {search_term}: {e}")
            
        return companies
    
    def _extract_company_info(self, entry) -> Optional[Dict]:
        """Extract company information from search result entry"""
        try:
            # Extract basic info
            name = self._clean_text(entry.find(['h3', 'td', 'div'], class_=['entity-name', 'name', 'title']))
            if not name:
                return None
            
            # Skip if it's an individual name (not a business)
            if self._is_individual_name(name):
                return None
            
            # Extract registration details
            reg_number = self._clean_text(entry.find(['span', 'td'], class_=['reg-number', 'file-number']))
            status = self._clean_text(entry.find(['span', 'td'], class_=['status', 'entity-status']))
            
            # Extract address
            address_elem = entry.find(['div', 'td'], class_=['address', 'principal-address'])
            address = self._clean_text(address_elem) if address_elem else None
            
            # Determine island from address
            island = self.extract_island(address) if address else 'Oahu'  # Default to Oahu
            
            # Extract business type/structure
            business_type = self._clean_text(entry.find(['span', 'td'], class_=['entity-type', 'type']))
            
            # Determine industry from name and type
            industry = self.extract_industry(f"{name} {business_type or ''}")
            
            # Create company object
            company = {
                'name': name,
                'address': address or "Address not available",
                'island': island,
                'industry': industry,
                'website': None,  # HBE doesn't provide websites
                'phone': None,  # Will need to get from other sources
                'employee_count_estimate': self._estimate_employee_count(business_type),
                'annual_revenue_estimate': None,
                'description': f"Hawaii registered {business_type or 'business'}. Registration #: {reg_number}",
                'source': "Hawaii Business Express",
                'source_url': self.search_url,
                'linkedin_url': None,
                'founded_date': None,
                'is_verified': True  # Government source
            }
            
            return company
            
        except Exception as e:
            logger.error(f"Error extracting company info: {e}")
            return None
    
    def _estimate_employee_count(self, business_type: str) -> int:
        """Estimate employee count based on business type"""
        if not business_type:
            return 5
            
        business_type = business_type.lower()
        
        # Larger structures typically have more employees
        if any(term in business_type for term in ['corporation', 'corp', 'inc']):
            return 25
        elif any(term in business_type for term in ['llc', 'limited liability']):
            return 10
        elif any(term in business_type for term in ['partnership', 'lp', 'llp']):
            return 5
        else:
            return 5
    
    def _is_individual_name(self, name: str) -> bool:
        """Check if the name appears to be an individual rather than a business"""
        # Common patterns for individual names
        individual_patterns = [
            r'^[A-Z][a-z]+ [A-Z][a-z]+$',  # First Last
            r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$',  # First M. Last
            r'^[A-Z][a-z]+, [A-Z][a-z]+$',  # Last, First
        ]
        
        for pattern in individual_patterns:
            if re.match(pattern, name):
                return True
                
        # Check for business indicators
        business_indicators = [
            'LLC', 'Inc', 'Corp', 'Company', 'Services', 'Solutions',
            'Group', 'Partners', 'Associates', 'Enterprises', 'Holdings'
        ]
        
        return not any(indicator.lower() in name.lower() for indicator in business_indicators)