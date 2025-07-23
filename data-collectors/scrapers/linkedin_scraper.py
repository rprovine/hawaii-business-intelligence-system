"""
LinkedIn Companies Scraper for Hawaii Businesses
Note: LinkedIn has strict anti-scraping measures. This uses public search results only.
For production use, consider LinkedIn's official APIs.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
import logging
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from .base_scraper import BaseScraper


class LinkedInScraper(BaseScraper):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def search_hawaii_companies(self, industry: str = None, island: str = None) -> List[Dict]:
        """
        Search for Hawaii companies on LinkedIn using Google search
        (LinkedIn's own search requires login)
        """
        companies = []
        
        # Build search queries for different Hawaii locations
        locations = {
            'Oahu': ['Honolulu', 'Pearl City', 'Kailua', 'Kaneohe', 'Waipahu'],
            'Maui': ['Kahului', 'Lahaina', 'Kihei', 'Wailuku'],
            'Big Island': ['Hilo', 'Kona', 'Kailua-Kona', 'Waimea'],
            'Kauai': ['Lihue', 'Kapaa', 'Princeville'],
            'Molokai': ['Kaunakakai'],
            'Lanai': ['Lanai City']
        }
        
        # If specific island requested, use only those locations
        if island:
            search_locations = locations.get(island, [])
        else:
            # Search all locations
            search_locations = []
            for locs in locations.values():
                search_locations.extend(locs)
        
        for location in search_locations:
            try:
                # Use Google to find LinkedIn company pages
                query = f'site:linkedin.com/company "{location} Hawaii"'
                if industry:
                    query += f' "{industry}"'
                
                google_url = f'https://www.google.com/search?q={quote(query)}'
                
                response = self.session.get(google_url)
                time.sleep(random.uniform(2, 4))  # Be respectful
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract LinkedIn URLs from Google results
                    for link in soup.find_all('a', href=True):
                        href = link.get('href', '')
                        if 'linkedin.com/company/' in href and '/url?q=' in href:
                            # Extract actual LinkedIn URL from Google redirect
                            linkedin_url = href.split('/url?q=')[1].split('&')[0]
                            
                            # Extract company info from the search result
                            parent = link.find_parent('div', class_='g')
                            if parent:
                                title_elem = parent.find('h3')
                                snippet_elem = parent.find('span', class_='st') or parent.find('div', class_='VwiC3b')
                                
                                if title_elem:
                                    company_name = title_elem.get_text().replace(' | LinkedIn', '').strip()
                                    
                                    companies.append({
                                        'name': company_name,
                                        'linkedin_url': linkedin_url,
                                        'location': location,
                                        'island': self._get_island_for_location(location, locations),
                                        'description_snippet': snippet_elem.get_text() if snippet_elem else '',
                                        'source': 'LinkedIn'
                                    })
                                    
                                    logger.info(f"Found company: {company_name} in {location}")
                
            except Exception as e:
                logger.error(f"Error searching LinkedIn for {location}: {str(e)}")
                continue
        
        # Remove duplicates based on company name
        seen = set()
        unique_companies = []
        for company in companies:
            if company['name'] not in seen:
                seen.add(company['name'])
                unique_companies.append(company)
        
        return unique_companies
    
    def _get_island_for_location(self, location: str, locations_map: Dict) -> str:
        """Get island name for a given location"""
        for island, locs in locations_map.items():
            if location in locs:
                return island
        return 'Unknown'
    
    def enrich_company_data(self, company: Dict) -> Dict:
        """
        Attempt to enrich company data by parsing LinkedIn page
        Note: This is limited without login
        """
        try:
            if 'linkedin_url' in company:
                response = self.session.get(company['linkedin_url'])
                time.sleep(random.uniform(2, 4))
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Try to extract any visible data
                    # Note: Most data requires login, but sometimes basic info is visible
                    
                    # Look for company size in meta tags or visible text
                    size_indicators = ['employees', 'company size']
                    for indicator in size_indicators:
                        size_elem = soup.find(text=lambda t: t and indicator in t.lower())
                        if size_elem:
                            company['employee_count_indicator'] = size_elem.strip()
                            break
                    
                    # Look for industry information
                    industry_elem = soup.find('meta', {'property': 'og:description'})
                    if industry_elem:
                        company['meta_description'] = industry_elem.get('content', '')
                    
        except Exception as e:
            logger.error(f"Error enriching company data: {str(e)}")
        
        return company
    
    def scrape(self) -> List[Dict]:
        """Main scrape method called by scheduler"""
        logger.info("Starting LinkedIn scraper for Hawaii companies")
        return self._scrape_linkedin_hawaii_companies()
    
    def _scrape_linkedin_hawaii_companies(self) -> List[Dict]:
        """Internal method to scrape LinkedIn for Hawaii companies"""
        all_companies = []
        
        # Search for companies by island
        islands = ['Oahu', 'Maui', 'Big Island', 'Kauai']
        
        for island in islands:
            logger.info(f"Searching for companies in {island}")
            companies = self.search_hawaii_companies(island=island)
            
            # Enrich data for each company
            for company in companies:
                enriched = self.enrich_company_data(company)
                all_companies.append(enriched)
            
            # Be respectful of rate limits
            time.sleep(random.uniform(5, 10))
        
        # Also search for specific Hawaii-focused industries
        hawaii_industries = [
            'tourism', 'hospitality', 'resort', 'hotel',
            'agriculture', 'macadamia', 'coffee', 'pineapple',
            'renewable energy', 'solar', 'wind power',
            'marine', 'ocean', 'fishing',
            'construction', 'real estate',
            'healthcare', 'medical',
            'technology', 'software'
        ]
        
        for industry in hawaii_industries[:5]:  # Limit to 5 industries for now
            logger.info(f"Searching for {industry} companies in Hawaii")
            companies = self.search_hawaii_companies(industry=industry)
            
            for company in companies:
                # Check if we already have this company
                if not any(c['name'] == company['name'] for c in all_companies):
                    enriched = self.enrich_company_data(company)
                    all_companies.append(enriched)
            
            time.sleep(random.uniform(5, 10))
        
        logger.info(f"Found {len(all_companies)} total companies")
        
        # Transform to match expected format
        businesses = []
        for company in all_companies:
            business = {
                'name': company['name'],
                'address': f"{company['location']}, Hawaii",
                'island': company['island'],
                'industry': company.get('meta_description', 'Business Services')[:100] if 'meta_description' in company else 'Business Services',
                'website': company.get('linkedin_url', ''),
                'description': company.get('description_snippet', ''),
                'employee_count_estimate': company.get('employee_count_indicator', ''),
                'source': 'LinkedIn',
                'source_url': company.get('linkedin_url', '')
            }
            businesses.append(business)
        
        return businesses
    
    def parse_business_info(self, element):
        """Required by base class - not used in this implementation"""
        return {}


def scrape_linkedin_hawaii_companies():
    """Main function to scrape LinkedIn for Hawaii companies"""
    scraper = LinkedInScraper()
    all_companies = []
    
    # Search for companies by island
    islands = ['Oahu', 'Maui', 'Big Island', 'Kauai']
    
    for island in islands:
        logger.info(f"Searching for companies in {island}")
        companies = scraper.search_hawaii_companies(island=island)
        
        # Enrich data for each company
        for company in companies:
            enriched = scraper.enrich_company_data(company)
            all_companies.append(enriched)
        
        # Be respectful of rate limits
        time.sleep(random.uniform(5, 10))
    
    # Also search for specific Hawaii-focused industries
    hawaii_industries = [
        'tourism', 'hospitality', 'resort', 'hotel',
        'agriculture', 'macadamia', 'coffee', 'pineapple',
        'renewable energy', 'solar', 'wind power',
        'marine', 'ocean', 'fishing',
        'construction', 'real estate',
        'healthcare', 'medical',
        'technology', 'software'
    ]
    
    for industry in hawaii_industries:
        logger.info(f"Searching for {industry} companies in Hawaii")
        companies = scraper.search_hawaii_companies(industry=industry)
        
        for company in companies:
            # Check if we already have this company
            if not any(c['name'] == company['name'] for c in all_companies):
                enriched = scraper.enrich_company_data(company)
                all_companies.append(enriched)
        
        time.sleep(random.uniform(5, 10))
    
    logger.info(f"Found {len(all_companies)} total companies")
    return all_companies


if __name__ == "__main__":
    # Test the scraper
    companies = scrape_linkedin_hawaii_companies()
    
    print(f"\nFound {len(companies)} Hawaii companies on LinkedIn:")
    for company in companies[:10]:  # Show first 10
        print(f"\n- {company['name']}")
        print(f"  Location: {company['location']}, {company['island']}")
        print(f"  LinkedIn: {company['linkedin_url']}")
        if 'description_snippet' in company:
            print(f"  Description: {company['description_snippet'][:100]}...")