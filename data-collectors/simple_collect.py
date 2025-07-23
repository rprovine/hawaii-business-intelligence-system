
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import what we need
from services.database_service import DatabaseService
from processors.data_processor import DataProcessor

# Create sample data
sample_businesses = [
    {
        'name': 'Hawaii Tech Solutions',
        'address': '1000 Bishop Street, Honolulu, HI 96813',
        'island': 'Oahu',
        'industry': 'Technology',
        'description': 'IT consulting and software development',
        'employee_count_estimate': 25,
        'website': 'https://example.com',
        'source': 'Manual Entry'
    },
    {
        'name': 'Maui Ocean Tours',
        'address': '300 Maalaea Road, Wailuku, HI 96793',
        'island': 'Maui',
        'industry': 'Tourism',
        'description': 'Snorkeling and whale watching tours',
        'employee_count_estimate': 15,
        'website': 'https://example.com',
        'source': 'Manual Entry'
    }
]

# Process the data
processor = DataProcessor()
processed, added = processor.process_businesses(sample_businesses, 'manual')
print(f"Processed {processed} businesses, added {added} new ones")

# Analyze new prospects
if added > 0:
    processor.analyze_new_prospects()
    print("AI analysis completed")
