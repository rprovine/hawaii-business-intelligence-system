#!/usr/bin/env python3
"""
Test script to verify all scrapers are working correctly
"""

import logging
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append('.')

from scrapers.hawaii_business_scraper import HawaiiBusinessNewsScraper
from scrapers.hawaii_business_express_scraper import HawaiiBusinessExpressScraper
from scrapers.chamber_of_commerce_scraper import ChamberOfCommerceScraper
from scrapers.hawaii_tourism_scraper import HawaiiTourismScraper
from scrapers.hawaii_tech_scraper import HawaiiTechScraper
from scrapers.local_directories_scraper import LocalDirectoriesScraper
from scrapers.hawaii_agriculture_scraper import HawaiiAgricultureScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_scraper(scraper_class, name):
    """Test a single scraper"""
    print(f"\n{'='*60}")
    print(f"Testing {name}")
    print('='*60)
    
    try:
        scraper = scraper_class()
        start_time = datetime.now()
        
        # Run scraper
        companies = scraper.scrape()
        
        duration = (datetime.now() - start_time).seconds
        
        print(f"✓ Success!")
        print(f"  Found {len(companies)} companies")
        print(f"  Duration: {duration} seconds")
        
        # Show sample data
        if companies:
            print(f"\n  Sample companies:")
            for i, company in enumerate(companies[:3]):
                print(f"  {i+1}. {company.name}")
                print(f"     - Island: {company.island}")
                print(f"     - Industry: {company.industry}")
                print(f"     - Address: {company.address}")
                if company.website:
                    print(f"     - Website: {company.website}")
                    
        return True, len(companies)
        
    except Exception as e:
        print(f"✗ Failed!")
        print(f"  Error: {str(e)}")
        logger.error(f"Error testing {name}: {e}", exc_info=True)
        return False, 0


def main():
    """Run all scraper tests"""
    print("Hawaii Business Intelligence System - Scraper Test Suite")
    print(f"Started at: {datetime.now()}")
    
    # Define all scrapers to test
    scrapers = [
        (HawaiiBusinessNewsScraper, "Hawaii Business News"),
        (HawaiiBusinessExpressScraper, "Hawaii Business Express"),
        (ChamberOfCommerceScraper, "Chamber of Commerce"),
        (HawaiiTourismScraper, "Hawaii Tourism Authority"),
        (HawaiiTechScraper, "Hawaii Tech Alliance"),
        (LocalDirectoriesScraper, "Local Directories"),
        (HawaiiAgricultureScraper, "Hawaii Agriculture")
    ]
    
    # Test results
    total_scrapers = len(scrapers)
    successful = 0
    total_companies = 0
    
    # Run tests
    for scraper_class, name in scrapers:
        success, count = test_scraper(scraper_class, name)
        if success:
            successful += 1
            total_companies += count
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Total scrapers tested: {total_scrapers}")
    print(f"Successful: {successful}")
    print(f"Failed: {total_scrapers - successful}")
    print(f"Total companies found: {total_companies}")
    print(f"\nCompleted at: {datetime.now()}")
    
    # Exit code based on results
    if successful == total_scrapers:
        print("\n✓ All scrapers passed!")
        sys.exit(0)
    else:
        print("\n✗ Some scrapers failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()