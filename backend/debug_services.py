#!/usr/bin/env python3
"""Debug service arrays"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Prospect

db = SessionLocal()

# Check different ways services might be empty
prospects = db.query(Prospect).all()
print(f"Total prospects: {len(prospects)}")

for i, p in enumerate(prospects):
    services = p.recommended_services
    print(f"\n{i+1}. {p.company.name}:")
    print(f"   services = {services}")
    print(f"   type = {type(services)}")
    print(f"   len = {len(services) if services else 'None'}")
    print(f"   bool = {bool(services)}")
    
    # Check first element if exists
    if services and len(services) > 0:
        print(f"   first element = '{services[0]}' (type: {type(services[0])})")

db.close()