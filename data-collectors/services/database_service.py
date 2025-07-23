import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseService:
    """Database service for data collectors"""
    
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'hawaii_business_intel'),
            'user': os.getenv('DB_USER', 'hbi_user'),
            'password': os.getenv('DB_PASSWORD')
        }
        
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.connection_params)
        
    def create_company(self, company_data: Dict[str, Any]) -> Optional[int]:
        """Create a new company record"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO companies (
                            name, address, island, industry, website, phone,
                            employee_count_estimate, annual_revenue_estimate,
                            description, source, source_url
                        ) VALUES (
                            %(name)s, %(address)s, %(island)s, %(industry)s,
                            %(website)s, %(phone)s, %(employee_count_estimate)s,
                            %(annual_revenue_estimate)s, %(description)s,
                            %(source)s, %(source_url)s
                        ) RETURNING id
                    """
                    cursor.execute(query, company_data)
                    company_id = cursor.fetchone()[0]
                    conn.commit()
                    return company_id
                    
        except Exception as e:
            logger.error(f"Error creating company: {str(e)}")
            return None
            
    def update_company(self, company_id: int, company_data: Dict[str, Any]):
        """Update existing company record"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Build update query dynamically
                    update_fields = []
                    params = {'id': company_id}
                    
                    for field in ['description', 'employee_count_estimate', 
                                  'website', 'phone', 'source_url']:
                        if field in company_data:
                            update_fields.append(f"{field} = %({field})s")
                            params[field] = company_data[field]
                            
                    if update_fields:
                        query = f"""
                            UPDATE companies 
                            SET {', '.join(update_fields)}, updated_at = NOW()
                            WHERE id = %(id)s
                        """
                        cursor.execute(query, params)
                        conn.commit()
                        
        except Exception as e:
            logger.error(f"Error updating company: {str(e)}")
            
    def get_company(self, company_id: int) -> Optional[Dict[str, Any]]:
        """Get company by ID"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = "SELECT * FROM companies WHERE id = %s"
                    cursor.execute(query, (company_id,))
                    return cursor.fetchone()
                    
        except Exception as e:
            logger.error(f"Error getting company: {str(e)}")
            return None
            
    def get_company_by_name_and_island(self, name: str, island: str) -> Optional[Dict[str, Any]]:
        """Check if company already exists"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                        SELECT * FROM companies 
                        WHERE LOWER(name) = LOWER(%s) AND island = %s
                    """
                    cursor.execute(query, (name, island))
                    return cursor.fetchone()
                    
        except Exception as e:
            logger.error(f"Error checking company existence: {str(e)}")
            return None
            
    def create_prospect(self, prospect_data: Dict[str, Any]) -> Optional[int]:
        """Create a new prospect record"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO prospects (
                            company_id, score, growth_signals
                        ) VALUES (
                            %(company_id)s, %(score)s, %(growth_signals)s
                        ) RETURNING id
                    """
                    cursor.execute(query, prospect_data)
                    prospect_id = cursor.fetchone()[0]
                    conn.commit()
                    return prospect_id
                    
        except Exception as e:
            logger.error(f"Error creating prospect: {str(e)}")
            return None
            
    def update_prospect(self, prospect_id: int, analysis_data: Dict[str, Any]):
        """Update prospect with analysis results"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                        UPDATE prospects SET
                            score = %(score)s,
                            ai_analysis = %(ai_analysis)s,
                            pain_points = %(pain_points)s,
                            recommended_services = %(recommended_services)s,
                            estimated_deal_value = %(estimated_deal_value)s,
                            growth_signals = %(growth_signals)s,
                            technology_readiness = %(technology_readiness)s,
                            priority_level = %(priority_level)s,
                            last_analyzed = NOW(),
                            updated_at = NOW()
                        WHERE id = %(id)s
                    """
                    analysis_data['id'] = prospect_id
                    cursor.execute(query, analysis_data)
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error updating prospect: {str(e)}")
            
    def get_unanalyzed_prospects(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get prospects that need analysis"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                        SELECT * FROM prospects 
                        WHERE score = 0 OR last_analyzed IS NULL
                        ORDER BY created_at DESC
                        LIMIT %s
                    """
                    cursor.execute(query, (limit,))
                    return cursor.fetchall()
                    
        except Exception as e:
            logger.error(f"Error getting unanalyzed prospects: {str(e)}")
            return []
            
    def log_collection(self, **kwargs):
        """Log data collection run"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO data_collection_logs (
                            source, records_found, records_processed,
                            records_added, errors, error_details,
                            duration_seconds, status
                        ) VALUES (
                            %(source)s, %(records_found)s, %(records_processed)s,
                            %(records_added)s, %(errors)s, %(error_details)s,
                            %(duration_seconds)s, %(status)s
                        )
                    """
                    cursor.execute(query, kwargs)
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error logging collection: {str(e)}")
            
    def create_analytics_snapshot(self):
        """Create analytics snapshot"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Get analytics data
                    cursor.execute("""
                        SELECT 
                            COUNT(*) as total_prospects,
                            AVG(score) as average_score,
                            COUNT(*) FILTER (WHERE priority_level = 'High') as high_priority_count,
                            SUM(estimated_deal_value) as total_pipeline_value
                        FROM prospects
                    """)
                    stats = cursor.fetchone()
                    
                    # Get by island
                    cursor.execute("""
                        SELECT c.island, COUNT(*) as count
                        FROM prospects p
                        JOIN companies c ON p.company_id = c.id
                        GROUP BY c.island
                    """)
                    by_island = {row[0]: row[1] for row in cursor.fetchall()}
                    
                    # Get by industry
                    cursor.execute("""
                        SELECT c.industry, COUNT(*) as count
                        FROM prospects p
                        JOIN companies c ON p.company_id = c.id
                        GROUP BY c.industry
                    """)
                    by_industry = {row[0]: row[1] for row in cursor.fetchall()}
                    
                    # Insert snapshot
                    cursor.execute("""
                        INSERT INTO analytics_snapshots (
                            snapshot_date, total_prospects, prospects_by_island,
                            prospects_by_industry, average_score, high_priority_count,
                            total_pipeline_value, conversion_rate
                        ) VALUES (
                            CURRENT_DATE, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (snapshot_date) DO UPDATE SET
                            total_prospects = EXCLUDED.total_prospects,
                            prospects_by_island = EXCLUDED.prospects_by_island,
                            prospects_by_industry = EXCLUDED.prospects_by_industry,
                            average_score = EXCLUDED.average_score,
                            high_priority_count = EXCLUDED.high_priority_count,
                            total_pipeline_value = EXCLUDED.total_pipeline_value,
                            updated_at = NOW()
                    """, (
                        stats[0], psycopg2.extras.Json(by_island),
                        psycopg2.extras.Json(by_industry), stats[1],
                        stats[2], stats[3], 0  # Conversion rate placeholder
                    ))
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error creating analytics snapshot: {str(e)}")
            
    def create_email_alert(self, alert_data: Dict[str, Any]):
        """Create email alert record"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO email_alerts (
                            prospect_id, alert_type, recipient_email,
                            subject, body, status
                        ) VALUES (
                            %(prospect_id)s, %(alert_type)s, %(recipient_email)s,
                            %(subject)s, %(body)s, %(status)s
                        )
                    """
                    cursor.execute(query, alert_data)
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error creating email alert: {str(e)}")