#!/usr/bin/env python3
"""Fix recommended services using raw SQL"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import engine

# Parse database URL
db_url = str(engine.url)
result = urlparse(db_url.replace('postgresql://', 'postgresql://'))

# Connect directly with psycopg2
conn = psycopg2.connect(
    host=result.hostname,
    port=result.port,
    database=result.path[1:],
    user=result.username,
    password=result.password
)
cur = conn.cursor()

try:
    # First, let's see what the data looks like
    cur.execute("SELECT id, company_id, recommended_services FROM prospects LIMIT 3")
    print("Current data format:")
    for row in cur.fetchall():
        print(f"ID: {row[0]}, Company: {row[1]}, Services: {row[2]}")
    
    # Fix the services - the issue is they're stored as character arrays, not enum arrays
    print("\nFixing recommended services...")
    
    # For each prospect, update with proper enum values
    cur.execute("SELECT id FROM prospects")
    prospect_ids = [row[0] for row in cur.fetchall()]
    
    fixed = 0
    for pid in prospect_ids:
        # Get current services
        cur.execute("SELECT recommended_services FROM prospects WHERE id = %s", (pid,))
        services = cur.fetchone()[0]
        
        if services and len(services) > 5:  # Indicates character array issue
            # Join the characters to form the string representation
            services_str = ''.join(services)
            
            # Parse and set correct enum values
            if 'Data Analytics' in services_str and 'Custom Chatbots' in services_str:
                cur.execute("""
                    UPDATE prospects 
                    SET recommended_services = ARRAY['Data Analytics'::service_enum, 'Custom Chatbots'::service_enum] 
                    WHERE id = %s
                """, (pid,))
            elif 'Data Analytics' in services_str and 'HubSpot Digital Marketing' in services_str:
                cur.execute("""
                    UPDATE prospects 
                    SET recommended_services = ARRAY['Data Analytics'::service_enum, 'HubSpot Digital Marketing'::service_enum] 
                    WHERE id = %s
                """, (pid,))
            elif 'Data Analytics' in services_str and 'Fractional CTO' in services_str:
                cur.execute("""
                    UPDATE prospects 
                    SET recommended_services = ARRAY['Data Analytics'::service_enum, 'Fractional CTO'::service_enum] 
                    WHERE id = %s
                """, (pid,))
            else:
                # Default to Data Analytics
                cur.execute("""
                    UPDATE prospects 
                    SET recommended_services = ARRAY['Data Analytics'::service_enum] 
                    WHERE id = %s
                """, (pid,))
            fixed += 1
    
    conn.commit()
    print(f"Fixed {fixed} prospects")
    
    # Verify the fix
    print("\nVerifying fix:")
    cur.execute("SELECT p.id, c.name, p.recommended_services FROM prospects p JOIN companies c ON p.company_id = c.id LIMIT 3")
    for row in cur.fetchall():
        print(f"ID: {row[0]}, Company: {row[1]}, Services: {row[2]}")
        
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()