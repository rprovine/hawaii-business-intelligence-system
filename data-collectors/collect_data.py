#!/usr/bin/env python3
"""
Data Collection Manager
Allows you to run different data collection modes
"""

import argparse
import sys
import os
from datetime import datetime
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scheduler import DataCollectionScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Hawaii Business Intelligence Data Collection')
    parser.add_argument('mode', choices=['demo', 'real', 'all', 'yelp', 'google', 'linkedin', 'news', 'test'],
                        help='Collection mode to run')
    parser.add_argument('--continuous', action='store_true',
                        help='Run scheduler continuously (otherwise runs once)')
    parser.add_argument('--api-key', help='Google Places API key (or set GOOGLE_PLACES_API_KEY env var)')
    
    args = parser.parse_args()
    
    # Set API key if provided
    if args.api_key:
        os.environ['GOOGLE_PLACES_API_KEY'] = args.api_key
    
    # Initialize scheduler
    scheduler = DataCollectionScheduler()
    
    print(f"\n{'='*60}")
    print(f"Hawaii Business Intelligence Data Collection")
    print(f"Mode: {args.mode}")
    print(f"Time: {datetime.now()}")
    print(f"{'='*60}\n")
    
    try:
        if args.mode == 'demo':
            print("Loading demo/sample data...")
            scheduler.load_demo_data()
            
        elif args.mode == 'real':
            print("Collecting real business data...")
            print("Sources: Hawaii Business News, Yelp, Google Places")
            if not os.getenv('GOOGLE_PLACES_API_KEY'):
                print("⚠️  Warning: Google Places API key not set. Google data will be skipped.")
                print("   Set with: export GOOGLE_PLACES_API_KEY='your-key-here'")
            scheduler.run_real_collection()
            
        elif args.mode == 'all':
            print("Running all data collectors...")
            scheduler.run_collection('all')
            
        elif args.mode == 'yelp':
            print("Collecting data from Yelp...")
            scheduler.run_collection('yelp')
            
        elif args.mode == 'google':
            if not os.getenv('GOOGLE_PLACES_API_KEY'):
                print("❌ Error: Google Places API key required!")
                print("   Set with: export GOOGLE_PLACES_API_KEY='your-key-here'")
                print("   Or use: --api-key YOUR_KEY")
                sys.exit(1)
            print("Collecting data from Google Places...")
            scheduler.run_collection('google_places')
            
        elif args.mode == 'linkedin':
            print("Collecting data from LinkedIn...")
            scheduler.run_collection('linkedin')
            
        elif args.mode == 'news':
            print("Collecting data from Hawaii Business News...")
            scheduler.run_collection('hawaii_business_news')
            
        elif args.mode == 'test':
            print("Running test collection (sample data only)...")
            scheduler.run_collection('sample_businesses')
        
        if args.continuous and args.mode != 'demo':
            print("\nStarting continuous scheduler...")
            print("Press Ctrl+C to stop")
            scheduler.start()
        else:
            print("\n✓ Data collection completed!")
            print(f"Check the dashboard at http://localhost:3002 to see the results")
            
    except KeyboardInterrupt:
        print("\n\nData collection stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logger.error("Collection failed", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()