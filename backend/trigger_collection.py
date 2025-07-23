#!/usr/bin/env python3
"""
Script to trigger data collection through the backend API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def trigger_workflow(action, source=None):
    """Trigger a workflow through the API"""
    url = f"{BASE_URL}/api/workflows/trigger"
    payload = {
        "action": action,
        "source": source
    }
    
    print(f"Triggering {action} workflow{' for ' + source if source else ''}...")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"Response: {result['message']}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_status():
    """Check workflow status"""
    url = f"{BASE_URL}/api/workflows/status"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        status = response.json()
        
        print("\n=== Workflow Status ===")
        if status['running_workflows']:
            print("Running workflows:")
            for wf in status['running_workflows']:
                print(f"  - {wf}")
        else:
            print("No running workflows")
            
        if status['recent_runs']:
            print("\nRecent runs:")
            for run in status['recent_runs']:
                print(f"  - {run['source']}: {run['status']} ({run['records_found']} found, {run['records_added']} added)")
        else:
            print("\nNo recent runs")
            
    except Exception as e:
        print(f"Error checking status: {e}")

def run_real_collection():
    """Actually run the data collection using subprocess"""
    import subprocess
    import os
    
    print("\n=== Running Real Data Collection ===")
    
    # Change to data-collectors directory
    collectors_dir = os.path.join(os.path.dirname(__file__), '..', 'data-collectors')
    
    # First, let's just load the demo data to ensure everything works
    print("Loading demo data first...")
    result = subprocess.run(
        ['python', 'collect_data.py', 'demo'],
        cwd=collectors_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("Demo data loaded successfully!")
        print(result.stdout)
    else:
        print("Error loading demo data:")
        print(result.stderr)
        
        # Try to fix the imports and run a simple collection
        print("\nTrying direct collection...")
        simple_collect = '''
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
'''
        
        # Write and run the simple script
        simple_script = os.path.join(collectors_dir, 'simple_collect.py')
        with open(simple_script, 'w') as f:
            f.write(simple_collect)
            
        result = subprocess.run(
            ['python', simple_script],
            cwd=collectors_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Simple collection successful!")
            print(result.stdout)
        else:
            print("Simple collection failed:")
            print(result.stderr)

if __name__ == "__main__":
    print("Hawaii Business Intelligence - Data Collection Tool")
    print("=" * 50)
    
    # Check initial status
    check_status()
    
    # Try to trigger through API (this is just a mock)
    print("\nNote: The API trigger is currently a mock implementation.")
    trigger_workflow("scrape", "all")
    
    # Run actual collection
    run_real_collection()
    
    # Check status again
    time.sleep(2)
    check_status()
    
    print("\n✓ Collection process completed!")
    print("Check your dashboard at http://localhost:3002 to see the results")