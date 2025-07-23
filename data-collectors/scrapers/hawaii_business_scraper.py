import re
from typing import List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class HawaiiBusinessNewsScraper(BaseScraper):
    """Scraper for Hawaii Business Magazine and Pacific Business News"""
    
    def __init__(self):
        super().__init__("Hawaii Business News")
        self.base_urls = [
            "https://www.hawaiibusiness.com/",
            "https://www.bizjournals.com/pacific/"
        ]
        
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape business news for company mentions and growth signals"""
        all_businesses = []
        
        for base_url in self.base_urls:
            try:
                businesses = self._scrape_source(base_url)
                all_businesses.extend(businesses)
            except Exception as e:
                logger.error(f"Error scraping {base_url}: {str(e)}")
                
        return all_businesses
        
    def _scrape_source(self, base_url: str) -> List[Dict[str, Any]]:
        """Scrape a specific news source"""
        businesses = []
        
        # This is a simplified version - in production, you'd implement
        # proper pagination and article parsing
        soup = self.fetch_page(base_url)
        
        # Find article links
        article_links = self._extract_article_links(soup, base_url)
        
        for link in article_links[:10]:  # Limit to 10 articles for demo
            try:
                article_businesses = self._extract_businesses_from_article(link)
                businesses.extend(article_businesses)
            except Exception as e:
                logger.error(f"Error processing article {link}: {str(e)}")
                
        return businesses
        
    def _extract_article_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract article links from the main page"""
        links = []
        
        # Generic article link patterns
        for a in soup.find_all('a', href=True):
            href = a['href']
            if any(pattern in href for pattern in ['/article/', '/news/', '/story/']):
                if href.startswith('http'):
                    links.append(href)
                else:
                    links.append(base_url.rstrip('/') + '/' + href.lstrip('/'))
                    
        return list(set(links))  # Remove duplicates
        
    def _extract_businesses_from_article(self, article_url: str) -> List[Dict[str, Any]]:
        """Extract business mentions from a news article"""
        businesses = []
        
        try:
            soup = self.fetch_page(article_url)
            article_text = self._extract_article_text(soup)
            
            # Extract company names using patterns
            company_patterns = [
                r'([A-Z][A-Za-z\s&]+(?:Inc\.|LLC|Corp\.|Corporation|Company|Co\.))',
                r'([A-Z][A-Za-z\s&]+)\s+(?:announced|launched|opened|expanded)',
            ]
            
            companies_mentioned = set()
            for pattern in company_patterns:
                matches = re.findall(pattern, article_text)
                companies_mentioned.update(matches)
                
            # Extract location information
            location_info = self._extract_location_info(article_text)
            
            for company in companies_mentioned:
                business_data = self.parse_business_info({
                    'name': company,
                    'text': article_text,
                    'location': location_info,
                    'url': article_url
                })
                
                if self.validate_business_data(business_data):
                    businesses.append(business_data)
                    
        except Exception as e:
            logger.error(f"Error extracting businesses from article: {str(e)}")
            
        return businesses
        
    def _extract_article_text(self, soup: BeautifulSoup) -> str:
        """Extract main article text"""
        # Try common article containers
        article_selectors = [
            'article', '.article-content', '.story-content',
            '[itemprop="articleBody"]', '.entry-content'
        ]
        
        for selector in article_selectors:
            article = soup.select_one(selector)
            if article:
                return self.clean_text(article.get_text())
                
        # Fallback to body text
        return self.clean_text(soup.get_text())
        
    def _extract_location_info(self, text: str) -> str:
        """Extract Hawaii location information from text"""
        # Look for Hawaii city/island mentions
        hawaii_locations = [
            'Honolulu', 'Pearl City', 'Kailua', 'Kaneohe', 'Hilo', 'Kona',
            'Kahului', 'Lihue', 'Oahu', 'Maui', 'Big Island', 'Kauai'
        ]
        
        for location in hawaii_locations:
            if location.lower() in text.lower():
                return location
                
        return ""
        
    def parse_business_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse business information from article data"""
        name = self.clean_text(data.get('name', ''))
        text = data.get('text', '')
        location = data.get('location', '')
        
        # Extract growth signals
        growth_signals = []
        growth_keywords = [
            'expanding', 'hiring', 'launched', 'opened', 'acquired',
            'investment', 'funding', 'growth', 'new location', 'partnership'
        ]
        
        for keyword in growth_keywords:
            if keyword in text.lower():
                growth_signals.append(keyword)
                
        # Estimate employee count from text
        employee_count = None
        employee_match = re.search(r'(\d+)\s*employees?', text, re.IGNORECASE)
        if employee_match:
            employee_count = int(employee_match.group(1))
            
        return {
            'name': name,
            'source': self.source_name,
            'source_url': data.get('url', ''),
            'island': self.determine_island(location),
            'industry': self.determine_industry(text, name),
            'description': text[:500] + '...' if len(text) > 500 else text,
            'growth_signals': growth_signals,
            'employee_count_estimate': employee_count,
            'scraped_at': datetime.now().isoformat()
        }
    
    def parse_business_info(self, element: Any) -> Dict[str, Any]:
        """Parse business information from element - required by base class"""
        return {}