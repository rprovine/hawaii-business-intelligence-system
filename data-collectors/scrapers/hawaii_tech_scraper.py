"""
Hawaii Technology and Innovation Sector Scraper
Extracts tech company data from Hawaii tech organizations and directories
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


class HawaiiTechScraper(BaseScraper):
    """Scraper for Hawaii technology companies and startups"""
    
    def __init__(self):
        super().__init__()
        self.sources = [
            {
                'name': 'Hawaii Technology Development Corporation',
                'url': 'https://www.htdc.org/',
                'type': 'htdc'
            },
            {
                'name': 'Blue Startups Hawaii',
                'url': 'https://www.bluestartups.com/',
                'type': 'accelerator'
            },
            {
                'name': 'Purple Mai\'a',
                'url': 'https://www.purplemaia.org/',
                'type': 'education'
            },
            {
                'name': 'Hawaii Strategic Development Corporation',
                'url': 'https://www.hsdc.hawaii.gov/',
                'type': 'investment'
            },
            {
                'name': 'ThriveHI',
                'url': 'https://www.thrivehi.com/',
                'type': 'community'
            },
            {
                'name': 'Hawaii Science & Technology Council',
                'url': 'https://www.hstonline.org/',
                'type': 'council'
            }
        ]
        
    def scrape(self) -> List[Dict]:
        """Scrape all tech sources"""
        all_companies = []
        
        for source in self.sources:
            logger.info(f"Scraping {source['name']}...")
            companies = self._scrape_tech_source(source)
            all_companies.extend(companies)
        
        # Remove duplicates
        unique_companies = {}
        for company in all_companies:
            if company['name'] not in unique_companies:
                unique_companies[company['name']] = company
                
        return list(unique_companies.values())
    
    def _scrape_tech_source(self, source: Dict) -> List[Dict]:
        """Scrape a specific tech source"""
        companies = []
        
        try:
            if source['type'] == 'htdc':
                companies = self._scrape_htdc(source)
            elif source['type'] == 'accelerator':
                companies = self._scrape_accelerator(source)
            elif source['type'] == 'council':
                companies = self._scrape_tech_council(source)
            else:
                companies = self._scrape_generic_tech_directory(source)
                
        except Exception as e:
            logger.error(f"Error scraping {source['name']}: {e}")
            
        return companies
    
    def _scrape_htdc(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Technology Development Corporation"""
        companies = []
        
        try:
            # HTDC lists incubator tenants and tech companies
            tenant_urls = [
                f"{source['url']}/tenants",
                f"{source['url']}/portfolio",
                f"{source['url']}/directory"
            ]
            
            for url in tenant_urls:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find company listings
                    companies_list = soup.find_all(['div', 'article'], class_=['tenant', 'company', 'portfolio-item'])
                    
                    for item in companies_list[:30]:
                        name = self._clean_text(item.find(['h3', 'h4', 'a']))
                        if not name:
                            continue
                        
                        # Extract company details
                        description = self._clean_text(item.find(['p', 'div'], class_=['description', 'summary']))
                        website = self._extract_website(item)
                        location = self._clean_text(item.find(['span', 'div'], class_=['location', 'address']))
                        
                        # Most HTDC companies are on Oahu
                        island = self.extract_island(location) if location else 'Oahu'
                        
                        # Extract tech focus area
                        tech_area = self._extract_tech_area(description)
                        
                        company = {
                            'name': name,
                            'address': location or "Honolulu, HI",
                            'island': island,
                            'industry': 'Technology',
                            'website': website,
                            'phone': None,
                            'employee_count_estimate': 15,  # Tech startups typically small
                            'annual_revenue_estimate': None,
                            'description': description or f"Technology company focused on {tech_area}",
                            'source': "Hawaii Technology Development Corporation",
                            'source_url': url,
                            'linkedin_url': None,
                            'founded_date': None,
                            'is_verified': True
                        }
                        
                        companies.append(company)
                        
        except Exception as e:
            logger.debug(f"Error scraping HTDC: {e}")
            
        return companies
    
    def _scrape_accelerator(self, source: Dict) -> List[Dict]:
        """Scrape startup accelerator portfolios"""
        companies = []
        
        try:
            # Blue Startups portfolio companies
            portfolio_url = f"{source['url']}/portfolio"
            response = self.session.get(portfolio_url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find portfolio companies
                startups = soup.find_all(['div', 'li'], class_= ['portfolio-company', 'startup', 'company'])
                
                for startup in startups[:25]:
                    name = self._clean_text(startup.find(['h3', 'h4', 'a']))
                    if not name:
                        continue
                    
                    # Extract startup details
                    tagline = self._clean_text(startup.find(['p', 'span'], class_= ['tagline', 'description']))
                    website = self._extract_website(startup)
                    cohort = self._clean_text(startup.find(['span', 'div'], class_= 'cohort'))
                    
                    # Determine tech vertical
                    vertical = self._extract_tech_vertical(tagline)
                    
                    company = {
                        'name': name,
                        'address': "Honolulu, HI",  # Most Blue Startups companies in Honolulu
                        'island': 'Oahu',
                        'industry': 'Technology',
                        'website': website,
                        'phone': None,
                        'employee_count_estimate': 8,  # Early-stage startups
                        'annual_revenue_estimate': None,
                        'description': f"{tagline or 'Tech startup'}. {cohort or 'Blue Startups portfolio company'}",
                        'source': source['name'],
                        'source_url': portfolio_url,
                        'linkedin_url': None,
                        'founded_date': self._extract_year_from_cohort(cohort),
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping accelerator: {e}")
            
        return companies
    
    def _scrape_tech_council(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Science & Technology Council members"""
        companies = []
        
        try:
            members_url = f"{source['url']}/members"
            response = self.session.get(members_url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find member companies
                members = soup.find_all(['div', 'li'], class_= ['member', 'company'])
                
                for member in members[:40]:
                    name = self._clean_text(member.find(['h3', 'a']))
                    if not name:
                        continue
                    
                    # Extract details
                    sector = self._clean_text(member.find(['span', 'div'], class_= ['sector', 'category']))
                    description = self._clean_text(member.find(['p', 'div'], class_= 'description'))
                    website = self._extract_website(member)
                    size = self._clean_text(member.find(['span', 'div'], class_= 'company-size'))
                    
                    # Determine location
                    location = self._clean_text(member.find(['span', 'div'], class_= 'location'))
                    island = self.extract_island(location) if location else 'Oahu'
                    
                    # Estimate employee count
                    employee_count = self._estimate_tech_company_size(size, description)
                    
                    company = {
                        'name': name,
                        'address': location or f"{island}, HI",
                        'island': island,
                        'industry': 'Technology',
                        'website': website,
                        'phone': self._extract_phone(member.text),
                        'employee_count_estimate': employee_count,
                        'annual_revenue_estimate': None,
                        'description': f"{sector or 'Technology'} company. {description or ''}".strip(),
                        'source': "Hawaii Science & Technology Council",
                        'source_url': members_url,
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping tech council: {e}")
            
        return companies
    
    def _scrape_generic_tech_directory(self, source: Dict) -> List[Dict]:
        """Generic scraper for other tech directories"""
        companies = []
        
        try:
            response = self.session.get(source['url'], timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for company listings
                listings = soup.find_all(['div', 'article', 'li'], 
                                        class_= re.compile(r'company|member|listing|item', re.I))
                
                for listing in listings[:20]:
                    name = self._clean_text(listing.find(['h2', 'h3', 'h4', 'a']))
                    if not name or self._is_navigation_text(name):
                        continue
                    
                    # Extract whatever details are available
                    description = self._clean_text(listing.find(['p', 'div'], class_= re.compile(r'desc|summary|about', re.I)))
                    website = self._extract_website(listing)
                    
                    company = {
                        'name': name,
                        'address': "Hawaii",
                        'island': 'Oahu',  # Default to Oahu for tech companies
                        'industry': 'Technology',
                        'website': website,
                        'phone': None,
                        'employee_count_estimate': 10,
                        'annual_revenue_estimate': None,
                        'description': description or f"Technology company listed on {source['name']}",
                        'source': source['name'],
                        'source_url': source['url'],
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping {source['name']}: {e}")
            
        return companies
    
    def _extract_tech_area(self, description: str) -> str:
        """Extract technology focus area from description"""
        if not description:
            return "software"
            
        description = description.lower()
        
        tech_areas = {
            'ai': ['artificial intelligence', 'machine learning', 'ai', 'ml', 'neural'],
            'saas': ['saas', 'software as a service', 'cloud', 'subscription'],
            'fintech': ['fintech', 'financial', 'payment', 'banking', 'crypto'],
            'healthtech': ['health', 'medical', 'healthcare', 'biotech', 'pharma'],
            'edtech': ['education', 'learning', 'training', 'edtech'],
            'iot': ['iot', 'internet of things', 'sensor', 'device'],
            'cybersecurity': ['security', 'cyber', 'protection', 'privacy'],
            'ecommerce': ['ecommerce', 'e-commerce', 'marketplace', 'retail tech'],
            'cleantech': ['clean', 'renewable', 'energy', 'sustainable'],
            'agtech': ['agriculture', 'farming', 'agtech', 'food tech']
        }
        
        for area, keywords in tech_areas.items():
            if any(keyword in description for keyword in keywords):
                return area
                
        return "software"
    
    def _extract_tech_vertical(self, tagline: str) -> str:
        """Extract technology vertical from tagline"""
        return self._extract_tech_area(tagline)
    
    def _extract_year_from_cohort(self, cohort: str) -> Optional[str]:
        """Extract founding year from cohort information"""
        if not cohort:
            return None
            
        year_match = re.search(r'20\d{2}', cohort)
        if year_match:
            return year_match.group(0)
            
        return None
    
    def _estimate_tech_company_size(self, size_text: str, description: str) -> int:
        """Estimate employee count for tech companies"""
        if size_text:
            size_text = size_text.lower()
            if 'startup' in size_text or '1-10' in size_text:
                return 5
            elif '11-50' in size_text or 'small' in size_text:
                return 25
            elif '51-200' in size_text or 'medium' in size_text:
                return 100
            elif 'large' in size_text or '200+' in size_text:
                return 250
                
        # Estimate based on description
        if description:
            description = description.lower()
            if 'enterprise' in description or 'global' in description:
                return 100
            elif 'startup' in description or 'early stage' in description:
                return 8
                
        return 15  # Default for tech companies
    
    def _is_navigation_text(self, text: str) -> bool:
        """Check if text is navigation/menu item"""
        nav_terms = ['home', 'about', 'contact', 'blog', 'news', 'events', 'resources']
        return text.lower() in nav_terms
    
    def _extract_website(self, element) -> Optional[str]:
        """Extract website URL from element"""
        # Look for company website (not the directory site)
        links = element.find_all('a', href= True)
        for link in links:
            href = link.get('href', '')
            # Skip internal/navigation links
            if href and not any(skip in href for skip in ['#', 'mailto:', 'tel:', '/about', '/contact']):
                if href.startswith('http') and source['url'] not in href:
                    return href
                    
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
        if phone_match:
            return phone_match.group(1)
        return None