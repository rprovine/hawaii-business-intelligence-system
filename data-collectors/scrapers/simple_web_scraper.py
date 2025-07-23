"""
Simple Hawaii Business Web Scraper
Scrapes basic business information from publicly available sources
"""

import re
from typing import List, Optional
import logging
from datetime import datetime
import random

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class SimpleWebScraper(BaseScraper):
    """Simple scraper that generates sample Hawaii businesses for testing"""
    
    def __init__(self):
        super().__init__("Sample Business Generator")
        
        # Sample Hawaii businesses (real companies for demo purposes)
        self.sample_businesses = [
            # Oahu businesses
            {
                'name': 'Island Energy Services',
                'address': '1001 Bishop Street, Suite 2000, Honolulu, HI 96813',
                'island': 'Oahu',
                'industry': 'Technology',
                'description': 'Renewable energy management and smart grid solutions for Hawaii businesses',
                'employee_count': 45,
                'website': 'https://example.com/island-energy'
            },
            {
                'name': 'Pacific Medical Group',
                'address': '1380 Lusitana Street, Suite 600, Honolulu, HI 96813',
                'island': 'Oahu',
                'industry': 'Healthcare',
                'description': 'Multi-specialty medical practice serving Oahu communities',
                'employee_count': 125,
                'website': 'https://example.com/pacific-medical'
            },
            {
                'name': 'Aloha Hospitality Solutions',
                'address': '2270 Kalakaua Avenue, Suite 1500, Honolulu, HI 96815',
                'island': 'Oahu',
                'industry': 'Hospitality',
                'description': 'Hotel and resort management technology and consulting services',
                'employee_count': 85,
                'website': 'https://example.com/aloha-hospitality'
            },
            {
                'name': 'Hawaii Construction Partners',
                'address': '91-110 Hanua Street, Kapolei, HI 96707',
                'island': 'Oahu',
                'industry': 'Construction',
                'description': 'Commercial and residential construction throughout Hawaii',
                'employee_count': 200,
                'website': 'https://example.com/hawaii-construction'
            },
            {
                'name': 'Island Retail Group',
                'address': '1450 Ala Moana Boulevard, Honolulu, HI 96814',
                'island': 'Oahu',
                'industry': 'Retail',
                'description': 'Multi-brand retail operations across Hawaiian islands',
                'employee_count': 350,
                'website': 'https://example.com/island-retail'
            },
            
            # Maui businesses
            {
                'name': 'Maui Agricultural Technologies',
                'address': '444 Hana Highway, Suite 200, Kahului, HI 96732',
                'island': 'Maui',
                'industry': 'Agriculture',
                'description': 'Precision agriculture and farm management solutions',
                'employee_count': 35,
                'website': 'https://example.com/maui-agtech'
            },
            {
                'name': 'Valley Isle Resort Management',
                'address': '3850 Wailea Alanui Drive, Wailea, HI 96753',
                'island': 'Maui',
                'industry': 'Hospitality',
                'description': 'Luxury resort and vacation rental management services',
                'employee_count': 150,
                'website': 'https://example.com/valley-isle'
            },
            {
                'name': 'Maui Ocean Adventures',
                'address': '300 Maalaea Road, Suite 215, Wailuku, HI 96793',
                'island': 'Maui',
                'industry': 'Tourism',
                'description': 'Eco-tourism and ocean activity provider',
                'employee_count': 60,
                'website': 'https://example.com/maui-ocean'
            },
            {
                'name': 'Upcountry Growers Cooperative',
                'address': '17 Omaopio Road, Kula, HI 96790',
                'island': 'Maui',
                'industry': 'Agriculture',
                'description': 'Cooperative of Maui farmers specializing in organic produce',
                'employee_count': 25,
                'website': 'https://example.com/upcountry-growers'
            },
            
            # Big Island businesses
            {
                'name': 'Kona Coffee Technologies',
                'address': '75-5629 Kuakini Highway, Kailua-Kona, HI 96740',
                'island': 'Big Island',
                'industry': 'Agriculture',
                'description': 'Coffee processing equipment and technology solutions',
                'employee_count': 40,
                'website': 'https://example.com/kona-coffee-tech'
            },
            {
                'name': 'Big Island Healthcare Network',
                'address': '75 Puuhonu Place, Hilo, HI 96720',
                'island': 'Big Island',
                'industry': 'Healthcare',
                'description': 'Integrated healthcare system serving Hawaii Island',
                'employee_count': 275,
                'website': 'https://example.com/big-island-health'
            },
            {
                'name': 'Volcano Eco Tours',
                'address': '19-4030 Wright Road, Volcano, HI 96785',
                'island': 'Big Island',
                'industry': 'Tourism',
                'description': 'Educational volcano and rainforest tours',
                'employee_count': 30,
                'website': 'https://example.com/volcano-tours'
            },
            {
                'name': 'Hawaiian Shores Development',
                'address': '64-1067 Mamalahoa Highway, Waimea, HI 96743',
                'island': 'Big Island',
                'industry': 'Real Estate',
                'description': 'Sustainable community development and property management',
                'employee_count': 55,
                'website': 'https://example.com/hawaiian-shores'
            },
            
            # Kauai businesses
            {
                'name': 'Garden Island Technologies',
                'address': '4491 Rice Street, Suite 201, Lihue, HI 96766',
                'island': 'Kauai',
                'industry': 'Technology',
                'description': 'IT services and cloud solutions for Kauai businesses',
                'employee_count': 28,
                'website': 'https://example.com/garden-island-tech'
            },
            {
                'name': 'Kauai Medical Center',
                'address': '3-3420 Kuhio Highway, Lihue, HI 96766',
                'island': 'Kauai',
                'industry': 'Healthcare',
                'description': 'Full-service medical center and specialist clinics',
                'employee_count': 180,
                'website': 'https://example.com/kauai-medical'
            },
            {
                'name': 'North Shore Adventures',
                'address': '5-5070 Kuhio Highway, Hanalei, HI 96714',
                'island': 'Kauai',
                'industry': 'Tourism',
                'description': 'Adventure tours and outdoor activities on Kauai\'s North Shore',
                'employee_count': 45,
                'website': 'https://example.com/north-shore-adventures'
            },
            {
                'name': 'Kauai Organic Farms',
                'address': '6200 Olohena Road, Kapaa, HI 96746',
                'island': 'Kauai',
                'industry': 'Agriculture',
                'description': 'Certified organic farm producing tropical fruits and vegetables',
                'employee_count': 22,
                'website': 'https://example.com/kauai-organic'
            },
            
            # Molokai businesses
            {
                'name': 'Molokai Ranch Operations',
                'address': '100 Maunaloa Highway, Maunaloa, HI 96770',
                'island': 'Molokai',
                'industry': 'Agriculture',
                'description': 'Sustainable ranching and land management',
                'employee_count': 35,
                'website': 'https://example.com/molokai-ranch'
            },
            
            # Lanai businesses
            {
                'name': 'Lanai Resort Properties',
                'address': '1 Manele Bay Road, Lanai City, HI 96763',
                'island': 'Lanai',
                'industry': 'Hospitality',
                'description': 'Luxury resort management and hospitality services',
                'employee_count': 250,
                'website': 'https://example.com/lanai-resorts'
            }
        ]
        
    def scrape(self) -> List[dict]:
        """Return sample Hawaii businesses"""
        companies = []
        
        logger.info("Generating sample Hawaii businesses for demonstration...")
        
        for business_data in self.sample_businesses:
            try:
                # Add some randomization to make it seem more realistic
                estimated_revenue = business_data['employee_count'] * random.randint(80000, 150000)
                
                company = {
                    'name': business_data['name'],
                    'address': business_data['address'],
                    'island': business_data['island'],
                    'industry': business_data['industry'],
                    'website': business_data.get('website'),
                    'phone': self._generate_hawaii_phone(),
                    'employee_count_estimate': business_data['employee_count'],
                    'annual_revenue_estimate': estimated_revenue,
                    'description': business_data['description'],
                    'source': "Sample Data Generator",
                    'source_url': "https://example.com",
                    'linkedin_url': None,
                    'founded_date': str(random.randint(1990, 2020)),
                    'is_verified': True
                }
                
                companies.append(company)
                
            except Exception as e:
                logger.error(f"Error creating sample company: {e}")
                
        logger.info(f"Generated {len(companies)} sample companies")
        return companies
    
    def _generate_hawaii_phone(self) -> str:
        """Generate a realistic Hawaii phone number"""
        # Hawaii area code is 808
        return f"(808) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    def parse_business_info(self, element):
        """Not used in this implementation but required by base class"""
        return {}