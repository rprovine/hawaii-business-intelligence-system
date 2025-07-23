#!/usr/bin/env python3
"""Fix recommended services array serialization issue"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Prospect

db = SessionLocal()

try:
    prospects = db.query(Prospect).all()
    print(f'Fixing recommended services for {len(prospects)} prospects...')
    
    fixed_count = 0
    for prospect in prospects:
        # Check if services are stored as individual characters
        if prospect.recommended_services and len(prospect.recommended_services) > 5:
            # This indicates it's stored as characters not strings
            services_str = ''.join(prospect.recommended_services)
            
            # Parse the string representation to get actual services
            if 'Data Analytics' in services_str and 'Custom Chatbots' in services_str:
                prospect.recommended_services = ['Data Analytics', 'Custom Chatbots']
            elif 'Data Analytics' in services_str and 'HubSpot Digital Marketing' in services_str:
                prospect.recommended_services = ['Data Analytics', 'HubSpot Digital Marketing']
            elif 'Data Analytics' in services_str and 'Fractional CTO' in services_str:
                prospect.recommended_services = ['Data Analytics', 'Fractional CTO']
            elif 'Data Analytics' in services_str:
                prospect.recommended_services = ['Data Analytics']
            elif 'Custom Chatbots' in services_str:
                prospect.recommended_services = ['Custom Chatbots']
            elif 'HubSpot Digital Marketing' in services_str:
                prospect.recommended_services = ['HubSpot Digital Marketing']
            elif 'Fractional CTO' in services_str:
                prospect.recommended_services = ['Fractional CTO']
            else:
                # Default fallback
                prospect.recommended_services = ['Data Analytics']
            
            fixed_count += 1
    
    db.commit()
    print(f'Fixed {fixed_count} prospects')
    
    # Verify the fix
    print('\nVerifying fix:')
    for prospect in db.query(Prospect).limit(3).all():
        print(f'{prospect.company.name}: {prospect.recommended_services}')
        
except Exception as e:
    print(f'Error: {e}')
    db.rollback()
finally:
    db.close()