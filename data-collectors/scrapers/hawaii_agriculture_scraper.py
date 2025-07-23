"""
Hawaii Agricultural Industry Scraper
Extracts agricultural business data from farming associations and ag directories
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


class HawaiiAgricultureScraper(BaseScraper):
    """Scraper for Hawaii agricultural businesses and farms"""
    
    def __init__(self):
        super().__init__()
        self.sources = [
            {
                'name': 'Hawaii Farm Bureau Federation',
                'url': 'https://www.hfbf.org/',
                'type': 'federation'
            },
            {
                'name': 'Hawaii Department of Agriculture',
                'url': 'https://hdoa.hawaii.gov/',
                'type': 'government'
            },
            {
                'name': 'Hawaii Farmers Union United',
                'url': 'https://www.hfuuhi.org/',
                'type': 'union'
            },
            {
                'name': 'Hawaii Coffee Association',
                'url': 'https://www.hawaiicoffeeassoc.org/',
                'type': 'specialty',
                'product': 'coffee'
            },
            {
                'name': 'Hawaii Macadamia Nut Association',
                'url': 'https://www.hawaiimacnuts.org/',
                'type': 'specialty',
                'product': 'macadamia'
            },
            {
                'name': 'Hawaii Tropical Fruit Growers',
                'url': 'https://www.htfg.org/',
                'type': 'specialty',
                'product': 'tropical fruit'
            },
            {
                'name': 'Hawaii Cattlemen\'s Council',
                'url': 'https://www.hicattle.org/',
                'type': 'livestock'
            },
            {
                'name': 'Hawaii Floriculture and Nursery Association',
                'url': 'https://www.hfna.org/',
                'type': 'specialty',
                'product': 'flowers'
            }
        ]
        
        # Agricultural product categories
        self.ag_categories = [
            'coffee', 'macadamia', 'pineapple', 'sugarcane', 'taro',
            'tropical fruit', 'vegetables', 'flowers', 'nursery',
            'livestock', 'dairy', 'aquaculture', 'organic farming'
        ]
        
    def scrape(self) -> List[Dict]:
        """Scrape all agricultural sources"""
        all_companies = []
        
        for source in self.sources:
            logger.info(f"Scraping {source['name']}...")
            companies = self._scrape_ag_source(source)
            all_companies.extend(companies)
        
        # Also scrape farmers markets and co-ops
        market_companies = self._scrape_farmers_markets()
        all_companies.extend(market_companies)
        
        # Remove duplicates
        unique_companies = {}
        for company in all_companies:
            if company['name'] not in unique_companies:
                unique_companies[company['name']] = company
                
        return list(unique_companies.values())
    
    def _scrape_ag_source(self, source: Dict) -> List[Dict]:
        """Scrape a specific agricultural source"""
        companies = []
        
        try:
            if source['type'] == 'federation':
                companies = self._scrape_farm_bureau(source)
            elif source['type'] == 'government':
                companies = self._scrape_hdoa(source)
            elif source['type'] == 'union':
                companies = self._scrape_farmers_union(source)
            elif source['type'] == 'specialty':
                companies = self._scrape_specialty_association(source)
            elif source['type'] == 'livestock':
                companies = self._scrape_cattlemen(source)
                
        except Exception as e:
            logger.error(f"Error scraping {source['name']}: {e}")
            
        return companies
    
    def _scrape_farm_bureau(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Farm Bureau Federation members"""
        companies = []
        
        try:
            # Farm Bureau member directory
            members_url = f"{source['url']}/members"
            response = self.session.get(members_url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find member farms
                members = soup.find_all(['div', 'li'], class_=['member', 'farm', 'listing'])
                
                for member in members[:40]:
                    name = self._clean_text(member.find(['h3', 'h4', 'a']))
                    if not name:
                        continue
                    
                    # Extract farm details
                    location = self._clean_text(member.find(['span', 'div'], class_=['location', 'address']))
                    products = self._clean_text(member.find(['div', 'p'], class_=['products', 'crops']))
                    size = self._clean_text(member.find(['span', 'div'], class_=['acreage', 'size']))
                    
                    # Determine island
                    island = self.extract_island(location) if location else self._determine_island_from_products(products)
                    
                    # Estimate size
                    employee_count = self._estimate_farm_employees(size, products)
                    
                    company = {
                        'name': name,
                        'address': location or f"{island}, HI",
                        'island': island,
                        'industry': 'Agriculture',
                        'website': self._extract_website(member),
                        'phone': self._extract_phone(member.text),
                        'employee_count_estimate': employee_count,
                        'annual_revenue_estimate': None,
                        'description': f"Farm producing {products or 'various agricultural products'}. Member of Hawaii Farm Bureau.",
                        'source': "Hawaii Farm Bureau Federation",
                        'source_url': members_url,
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping Farm Bureau: {e}")
            
        return companies
    
    def _scrape_hdoa(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Department of Agriculture registered farms"""
        companies = []
        
        try:
            # HDOA has various programs with participant lists
            programs = [
                'organic-certification',
                'export-certificates',
                'agricultural-parks',
                'farm-food-safety'
            ]
            
            for program in programs:
                url = f"{source['url']}/programs/{program}"
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find participant listings
                    participants = soup.find_all(['div', 'tr'], class_=['participant', 'farm', 'certified'])
                    
                    for participant in participants[:15]:  # Limit per program
                        name = self._clean_text(participant.find(['td', 'h4', 'a']))
                        if not name:
                            continue
                        
                        # Extract details
                        cert_type = self._clean_text(participant.find(['span', 'td'], class_=['certification', 'type']))
                        location = self._clean_text(participant.find(['td', 'span'], class_=['location', 'island']))
                        
                        # Determine island
                        island = self.extract_island(location) if location else 'Oahu'
                        
                        # Description based on program
                        if 'organic' in program:
                            description = f"Certified organic farm. {cert_type or ''}"
                        elif 'export' in program:
                            description = f"Export-certified agricultural producer"
                        else:
                            description = f"HDOA registered agricultural business"
                        
                        company = {
                            'name': name,
                            'address': location or f"{island}, HI",
                            'island': island,
                            'industry': 'Agriculture',
                            'website': None,
                            'phone': None,
                            'employee_count_estimate': 20,
                            'annual_revenue_estimate': None,
                            'description': description,
                            'source': "Hawaii Department of Agriculture",
                            'source_url': url,
                            'linkedin_url': None,
                            'founded_date': None,
                            'is_verified': True
                        }
                        
                        companies.append(company)
                        
        except Exception as e:
            logger.debug(f"Error scraping HDOA: {e}")
            
        return companies
    
    def _scrape_specialty_association(self, source: Dict) -> List[Dict]:
        """Scrape specialty crop associations (coffee, mac nuts, etc.)"""
        companies = []
        product = source.get('product', 'specialty crop')
        
        try:
            response = self.session.get(source['url'], timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find member/grower listings
                growers = soup.find_all(['div', 'li', 'article'], 
                                       class_=['member', 'grower', 'farm', 'producer'])
                
                for grower in growers[:30]:
                    name = self._clean_text(grower.find(['h3', 'h4', 'a']))
                    if not name:
                        continue
                    
                    # Extract details
                    location = self._clean_text(grower.find(['span', 'div'], class_=['location', 'region']))
                    estate = self._clean_text(grower.find(['span', 'div'], class_=['estate', 'farm-name']))
                    elevation = self._clean_text(grower.find(['span', 'div'], class_=['elevation', 'altitude']))
                    
                    # Determine island based on product and location
                    island = self._determine_island_for_product(product, location)
                    
                    # Build description
                    desc_parts = []
                    if product:
                        desc_parts.append(f"{product.title()} producer")
                    if estate:
                        desc_parts.append(f"Estate: {estate}")
                    if elevation:
                        desc_parts.append(f"Elevation: {elevation}")
                    
                    company = {
                        'name': name,
                        'address': location or f"{island}, HI",
                        'island': island,
                        'industry': 'Agriculture',
                        'website': self._extract_website(grower),
                        'phone': self._extract_phone(grower.text),
                        'employee_count_estimate': 15,
                        'annual_revenue_estimate': None,
                        'description': '. '.join(desc_parts) or f"{product.title()} farm",
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
    
    def _scrape_farmers_markets(self) -> List[Dict]:
        """Scrape farmers market vendors"""
        companies = []
        
        # Hawaii farmers markets
        markets = [
            {'name': 'KCC Farmers Market', 'island': 'Oahu'},
            {'name': 'Hilo Farmers Market', 'island': 'Big Island'},
            {'name': 'Maui Swap Meet', 'island': 'Maui'},
            {'name': 'Kauai Community Market', 'island': 'Kauai'}
        ]
        
        # This would typically scrape actual market vendor lists
        # For now, using placeholder logic
        
        return companies
    
    def _scrape_cattlemen(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Cattlemen's Council members"""
        companies = []
        
        try:
            response = self.session.get(f"{source['url']}/members", timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find rancher listings
                ranchers = soup.find_all(['div', 'li'], class_=['member', 'ranch', 'rancher'])
                
                for rancher in ranchers[:25]:
                    name = self._clean_text(rancher.find(['h3', 'a']))
                    if not name:
                        continue
                    
                    # Ranch details
                    location = self._clean_text(rancher.find(['span', 'div'], class_='location'))
                    acreage = self._clean_text(rancher.find(['span', 'div'], class_='acreage'))
                    cattle_type = self._clean_text(rancher.find(['span', 'div'], class_='cattle-type'))
                    
                    # Big Island has most ranches, but check location
                    island = self.extract_island(location) if location else 'Big Island'
                    
                    # Estimate employees based on ranch size
                    employee_count = self._estimate_ranch_employees(acreage)
                    
                    company = {
                        'name': name,
                        'address': location or f"{island}, HI",
                        'island': island,
                        'industry': 'Agriculture',
                        'website': self._extract_website(rancher),
                        'phone': self._extract_phone(rancher.text),
                        'employee_count_estimate': employee_count,
                        'annual_revenue_estimate': None,
                        'description': f"Cattle ranch. {cattle_type or 'Beef cattle operation'}. {acreage or ''}".strip(),
                        'source': "Hawaii Cattlemen's Council",
                        'source_url': source['url'],
                        'linkedin_url': None,
                        'founded_date': None,
                        'is_verified': True
                    }
                    
                    companies.append(company)
                    
        except Exception as e:
            logger.debug(f"Error scraping Cattlemen's Council: {e}")
            
        return companies
    
    def _scrape_farmers_union(self, source: Dict) -> List[Dict]:
        """Scrape Hawaii Farmers Union United members"""
        companies = []
        
        try:
            # HFUU has chapters on different islands
            chapters = ['oahu', 'maui', 'big-island', 'kauai']
            
            for chapter in chapters:
                url = f"{source['url']}/chapters/{chapter}"
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find member farms
                    members = soup.find_all(['div', 'li'], class_=['member', 'farm'])
                    
                    for member in members[:10]:  # Limit per chapter
                        name = self._clean_text(member.find(['h4', 'a']))
                        if not name:
                            continue
                        
                        # Farm details
                        farm_type = self._clean_text(member.find(['span', 'div'], class_='farm-type'))
                        practices = self._clean_text(member.find(['span', 'div'], class_='practices'))
                        
                        # Map chapter to island
                        island_map = {
                            'oahu': 'Oahu',
                            'maui': 'Maui',
                            'big-island': 'Big Island',
                            'kauai': 'Kauai'
                        }
                        island = island_map.get(chapter, 'Oahu')
                        
                        company = {
                            'name': name,
                            'address': f"{island}, HI",
                            'island': island,
                            'industry': 'Agriculture',
                            'website': None,
                            'phone': None,
                            'employee_count_estimate': 10,
                            'annual_revenue_estimate': None,
                            'description': f"{farm_type or 'Family farm'}. {practices or 'Sustainable farming practices'}",
                            'source': "Hawaii Farmers Union United",
                            'source_url': url,
                            'linkedin_url': None,
                            'founded_date': None,
                            'is_verified': True
                        }
                        
                        companies.append(company)
                        
        except Exception as e:
            logger.debug(f"Error scraping Farmers Union: {e}")
            
        return companies
    
    def _determine_island_from_products(self, products: str) -> str:
        """Determine island based on agricultural products"""
        if not products:
            return 'Oahu'
            
        products = products.lower()
        
        # Product-island associations
        if 'kona coffee' in products:
            return 'Big Island'
        elif 'maui onion' in products or 'upcountry' in products:
            return 'Maui'
        elif 'taro' in products and 'hanalei' in products:
            return 'Kauai'
        elif 'molokai' in products:
            return 'Molokai'
        elif 'pineapple' in products and 'lanai' in products:
            return 'Lanai'
            
        return 'Oahu'  # Default
    
    def _determine_island_for_product(self, product: str, location: str) -> str:
        """Determine island based on product type and location"""
        if location:
            island = self.extract_island(location)
            if island:
                return island
        
        # Product-specific defaults
        product = product.lower() if product else ''
        
        if product == 'coffee':
            return 'Big Island'  # Kona coffee region
        elif product == 'macadamia':
            return 'Big Island'  # Major mac nut producer
        elif product == 'flowers':
            return 'Maui'  # Upcountry flower farms
        elif product == 'taro':
            return 'Kauai'  # Hanalei taro fields
            
        return 'Oahu'
    
    def _estimate_farm_employees(self, size: str, products: str) -> int:
        """Estimate farm employee count"""
        if size:
            # Extract acreage
            acre_match = re.search(r'(\d+)\s*acres?', size, re.I)
            if acre_match:
                acres = int(acre_match.group(1))
                if acres > 500:
                    return 50
                elif acres > 100:
                    return 25
                elif acres > 20:
                    return 10
                else:
                    return 5
        
        # Estimate by product type
        if products:
            products = products.lower()
            if any(labor in products for labor in ['vegetable', 'flower', 'nursery']):
                return 20  # Labor intensive
            elif any(crop in products for crop in ['coffee', 'fruit', 'macadamia']):
                return 15
            elif 'cattle' in products or 'ranch' in products:
                return 10
                
        return 10  # Default farm size
    
    def _estimate_ranch_employees(self, acreage: str) -> int:
        """Estimate ranch employee count based on acreage"""
        if not acreage:
            return 15
            
        acre_match = re.search(r'(\d+)', acreage)
        if acre_match:
            acres = int(acre_match.group(1))
            if acres > 10000:
                return 50
            elif acres > 5000:
                return 30
            elif acres > 1000:
                return 20
            else:
                return 10
                
        return 15
    
    def _extract_website(self, element) -> Optional[str]:
        """Extract website URL from element"""
        links = element.find_all('a', href=True)
        for link in links:
            href = link.get('href', '')
            if href.startswith('http') and not any(skip in href for skip in ['facebook', 'twitter', 'instagram']):
                return href
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
        if phone_match:
            return phone_match.group(1)
        return None