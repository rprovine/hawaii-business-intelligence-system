import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all Hawaii business data scrapers"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.user_agent = UserAgent()
        self.delay = int(os.getenv('SCRAPER_DELAY', 2))
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent.random
        })
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page with retry logic"""
        try:
            logger.info(f"Fetching URL: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(self.delay)  # Respect rate limits
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
            
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method to be implemented by subclasses"""
        pass
        
    @abstractmethod
    def parse_business_info(self, element: Any) -> Dict[str, Any]:
        """Parse business information from HTML element"""
        pass
        
    def validate_business_data(self, data: Dict[str, Any]) -> bool:
        """Validate scraped business data"""
        required_fields = ['name', 'island']
        return all(field in data and data[field] for field in required_fields)
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if not text:
            return ""
        return ' '.join(text.strip().split())
        
    def determine_island(self, address: str) -> str:
        """Determine which Hawaiian island based on address"""
        if not address:
            return "Unknown"
            
        address_lower = address.lower()
        island_keywords = {
            'Oahu': ['honolulu', 'pearl city', 'kailua', 'kaneohe', 'waipahu', 'mililani', 'aiea', 'ewa'],
            'Maui': ['kahului', 'kihei', 'lahaina', 'wailuku', 'makawao', 'paia', 'haiku'],
            'Big Island': ['hilo', 'kona', 'kailua-kona', 'waimea', 'pahoa', 'kamuela'],
            'Kauai': ['lihue', 'kapaa', 'princeville', 'poipu', 'hanapepe', 'waimea'],
            'Molokai': ['kaunakakai', 'maunaloa'],
            'Lanai': ['lanai city']
        }
        
        for island, keywords in island_keywords.items():
            if any(keyword in address_lower for keyword in keywords):
                return island
                
        return "Unknown"
        
    def determine_industry(self, description: str, name: str = "") -> str:
        """Determine industry based on business description and name"""
        text = f"{description} {name}".lower()
        
        industry_keywords = {
            'Tourism': ['tour', 'tourist', 'visitor', 'sightseeing', 'activity', 'excursion'],
            'Hospitality': ['hotel', 'resort', 'accommodation', 'lodging', 'bed and breakfast', 'vacation rental'],
            'Agriculture': ['farm', 'ranch', 'agricultural', 'crop', 'livestock', 'aquaculture'],
            'Retail': ['store', 'shop', 'boutique', 'mall', 'retail', 'merchandise'],
            'Healthcare': ['hospital', 'clinic', 'medical', 'health', 'doctor', 'dental', 'pharmacy'],
            'Real Estate': ['realty', 'property', 'real estate', 'broker', 'development', 'construction'],
            'Technology': ['software', 'tech', 'it', 'computer', 'digital', 'app', 'saas'],
            'Food Service': ['restaurant', 'cafe', 'food', 'dining', 'catering', 'bakery'],
            'Transportation': ['transport', 'shipping', 'freight', 'logistics', 'delivery', 'moving'],
            'Professional Services': ['consulting', 'accounting', 'legal', 'law', 'marketing', 'design']
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in text for keyword in keywords):
                return industry
                
        return "Other"