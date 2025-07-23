import schedule
import time
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

from scrapers.hawaii_business_scraper import HawaiiBusinessNewsScraper
from scrapers.simple_web_scraper import SimpleWebScraper
from scrapers.yelp_scraper import YelpScraper
from scrapers.google_places_scraper import GooglePlacesScraper
from scrapers.linkedin_scraper import LinkedInScraper
# Future scrapers
# from scrapers.chamber_of_commerce_scraper import ChamberOfCommerceScraper
from processors.data_processor import DataProcessor
from services.database_service import DatabaseService

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataCollectionScheduler:
    """Manages scheduled data collection tasks"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.processor = DataProcessor()
        # Initialize scrapers - separate demo from real data
        self.demo_scrapers = {
            'sample_businesses': SimpleWebScraper(),  # Keep for demos
        }
        
        self.real_scrapers = {
            'hawaii_business_news': HawaiiBusinessNewsScraper(),
            'yelp': YelpScraper(),
            'google_places': GooglePlacesScraper(),  # Requires API key
            'linkedin': LinkedInScraper(),
        }
        
        # Combined for backward compatibility
        self.scrapers = {**self.demo_scrapers, **self.real_scrapers}
        
    def run_collection(self, source='all'):
        """Run data collection for specified source"""
        start_time = datetime.now()
        total_found = 0
        total_processed = 0
        total_added = 0
        errors = 0
        error_details = []
        
        try:
            if source == 'all':
                sources_to_run = self.scrapers.keys()
            else:
                sources_to_run = [source] if source in self.scrapers else []
                
            for scraper_name in sources_to_run:
                logger.info(f"Starting collection for {scraper_name}")
                scraper = self.scrapers[scraper_name]
                
                try:
                    # Scrape data
                    raw_data = scraper.scrape()
                    total_found += len(raw_data)
                    
                    # Process and save data
                    processed_count, added_count = self.processor.process_businesses(
                        raw_data, scraper_name
                    )
                    
                    total_processed += processed_count
                    total_added += added_count
                    
                    logger.info(f"Completed {scraper_name}: Found {len(raw_data)}, "
                               f"Processed {processed_count}, Added {added_count}")
                    
                except Exception as e:
                    errors += 1
                    error_msg = f"Error in {scraper_name}: {str(e)}"
                    error_details.append(error_msg)
                    logger.error(error_msg)
                    
            # Log collection results
            duration = (datetime.now() - start_time).seconds
            self.db_service.log_collection(
                source='all' if source == 'all' else source,
                records_found=total_found,
                records_processed=total_processed,
                records_added=total_added,
                errors=errors,
                error_details='\n'.join(error_details) if error_details else None,
                duration_seconds=duration,
                status='completed' if errors == 0 else 'completed_with_errors'
            )
            
            # Analyze new prospects
            if total_added > 0:
                logger.info(f"Analyzing {total_added} new prospects")
                self.processor.analyze_new_prospects()
                
        except Exception as e:
            logger.error(f"Critical error in data collection: {str(e)}")
            self.db_service.log_collection(
                source=source,
                records_found=0,
                records_processed=0,
                records_added=0,
                errors=1,
                error_details=str(e),
                duration_seconds=(datetime.now() - start_time).seconds,
                status='failed'
            )
            
    def daily_collection(self):
        """Run daily data collection"""
        logger.info("Starting daily data collection")
        self.run_collection('all')
        
    def hourly_quick_scan(self):
        """Run hourly quick scan for high-priority sources"""
        logger.info("Starting hourly quick scan")
        self.run_collection('hawaii_business_news')
        
    def weekly_analytics(self):
        """Generate weekly analytics snapshot"""
        logger.info("Generating weekly analytics snapshot")
        try:
            self.db_service.create_analytics_snapshot()
            logger.info("Analytics snapshot created successfully")
        except Exception as e:
            logger.error(f"Error creating analytics snapshot: {str(e)}")
    
    def load_demo_data(self):
        """Load demo/sample data for demonstrations"""
        logger.info("Loading demo data...")
        self.run_collection('sample_businesses')
        
    def run_real_collection(self):
        """Run only real data collectors"""
        logger.info("Starting real data collection")
        for scraper_name in self.real_scrapers.keys():
            self.run_collection(scraper_name)
            
    def start(self):
        """Start the scheduler"""
        logger.info("Starting data collection scheduler")
        
        # Schedule tasks
        schedule.every().day.at("06:00").do(self.daily_collection)
        schedule.every().day.at("18:00").do(self.daily_collection)
        schedule.every().hour.do(self.hourly_quick_scan)
        schedule.every().monday.at("09:00").do(self.weekly_analytics)
        
        # Run initial collection
        self.daily_collection()
        
        # Keep running
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(300)  # Wait 5 minutes on error


if __name__ == "__main__":
    scheduler = DataCollectionScheduler()
    scheduler.start()