#!/usr/bin/env python3
"""Check recommended services in database"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Prospect

db = SessionLocal()
prospects = db.query(Prospect).all()
print(f'Total prospects: {len(prospects)}')

count = 0
for p in prospects:
    if p.recommended_services and len(p.recommended_services) > 0:
        count += 1
        if count <= 5:
            print(f'{p.company.name}: {p.recommended_services}')

print(f'\nProspects with services: {count}')
print(f'Prospects without services: {len(prospects) - count}')
db.close()