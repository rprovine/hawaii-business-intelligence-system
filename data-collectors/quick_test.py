#!/usr/bin/env python3
"""Quick test of data collection"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test just the Yelp scraper
from scrapers.yelp_scraper import scrape_yelp_hawaii_businesses

print("Testing Yelp scraper...")
try:
    businesses = scrape_yelp_hawaii_businesses()
    print(f"Found {len(businesses)} businesses")
    if businesses:
        print(f"First business: {businesses[0]['name']} in {businesses[0]['island']}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()