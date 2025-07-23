#!/usr/bin/env python3
"""
Fix the character array issue with recommended services
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal, engine
from models.models import Prospect, ServiceEnum
from sqlalchemy import text

def fix_services_properly():
    """Fix the character array issue"""
    db = SessionLocal()
    
    try:
        # First, let's fix this with raw SQL
        with engine.connect() as conn:
            # Fix prospects with character arrays representing valid services
            print("Fixing prospects with character array services...")
            
            # Prospects with {"Data Analytics","Custom Chatbots"} stored as chars
            result = conn.execute(text("""
                UPDATE prospects 
                SET recommended_services = ARRAY['Data Analytics'::service_enum, 'Custom Chatbots'::service_enum]
                WHERE array_length(recommended_services, 1) = 36
                RETURNING id, company_id
            """))
            conn.commit()
            fixed_1 = result.rowcount
            print(f"  Fixed {fixed_1} prospects with Data Analytics + Custom Chatbots")
            
            # Prospects with {} stored as chars (empty)
            result = conn.execute(text("""
                UPDATE prospects 
                SET recommended_services = ARRAY['Data Analytics'::service_enum]
                WHERE array_length(recommended_services, 1) = 2
                AND recommended_services[1] = '{'
                RETURNING id, company_id
            """))
            conn.commit()
            fixed_2 = result.rowcount
            print(f"  Fixed {fixed_2} prospects with empty services -> Data Analytics")
            
            # Now assign proper services to those with just Data Analytics based on their profile
            print("\nAssigning additional services based on industry...")
            
            # Get prospects that only have Data Analytics
            prospects = db.query(Prospect).all()
            additional_fixed = 0
            
            for prospect in prospects:
                if (prospect.recommended_services and 
                    len(prospect.recommended_services) == 1 and 
                    prospect.recommended_services[0] == 'Data Analytics'):
                    
                    company = prospect.company
                    
                    # Add additional service based on industry
                    if company.industry in ['Technology', 'Healthcare']:
                        result = conn.execute(text("""
                            UPDATE prospects 
                            SET recommended_services = ARRAY['Data Analytics'::service_enum, 'Custom Chatbots'::service_enum]
                            WHERE id = :id
                        """), {"id": prospect.id})
                        conn.commit()
                        additional_fixed += 1
                        print(f"    {company.name} -> +Custom Chatbots")
                        
                    elif company.industry in ['Hospitality', 'Tourism']:
                        result = conn.execute(text("""
                            UPDATE prospects 
                            SET recommended_services = ARRAY['Data Analytics'::service_enum, 'HubSpot Digital Marketing'::service_enum]
                            WHERE id = :id
                        """), {"id": prospect.id})
                        conn.commit()
                        additional_fixed += 1
                        print(f"    {company.name} -> +HubSpot Digital Marketing")
                        
                    elif company.industry in ['Construction', 'Real Estate'] and prospect.score >= 80:
                        result = conn.execute(text("""
                            UPDATE prospects 
                            SET recommended_services = ARRAY['Data Analytics'::service_enum, 'Fractional CTO'::service_enum]
                            WHERE id = :id
                        """), {"id": prospect.id})
                        conn.commit()
                        additional_fixed += 1
                        print(f"    {company.name} -> +Fractional CTO")
            
            print(f"\n✓ Total fixes: {fixed_1 + fixed_2 + additional_fixed}")
            
            # Verify the fix
            result = conn.execute(text("""
                SELECT COUNT(*) as total,
                       COUNT(CASE WHEN array_length(recommended_services, 1) > 0 THEN 1 END) as with_services,
                       COUNT(CASE WHEN array_length(recommended_services, 1) = 2 
                                  AND cardinality(recommended_services) = 2 THEN 1 END) as with_two_services
                FROM prospects
            """))
            row = result.fetchone()
            print(f"\nVerification:")
            print(f"  Total prospects: {row[0]}")
            print(f"  With services: {row[1]}")
            print(f"  With 2 services: {row[2]}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("Fixing recommended services properly...")
    print("="*60)
    fix_services_properly()