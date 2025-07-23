import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.database_service import DatabaseService
from backend.services.claude_analyzer import ClaudeBusinessAnalyzer

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and analyze scraped business data"""
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.analyzer = ClaudeBusinessAnalyzer()
        
    def process_businesses(self, businesses: List[Dict[str, Any]], source: str) -> Tuple[int, int]:
        """Process list of businesses and save to database"""
        processed_count = 0
        added_count = 0
        
        for business_data in businesses:
            try:
                # Add source if not present
                if 'source' not in business_data:
                    business_data['source'] = source
                    
                # Check if company already exists
                existing_company = self.db_service.get_company_by_name_and_island(
                    business_data.get('name'),
                    business_data.get('island')
                )
                
                if existing_company:
                    # Update existing company
                    self.db_service.update_company(existing_company['id'], business_data)
                    processed_count += 1
                else:
                    # Create new company
                    company_id = self.db_service.create_company(business_data)
                    if company_id:
                        # Create prospect entry
                        prospect_id = self.db_service.create_prospect({
                            'company_id': company_id,
                            'score': 0,  # Will be updated by analysis
                            'growth_signals': business_data.get('growth_signals', [])
                        })
                        
                        if prospect_id:
                            added_count += 1
                            processed_count += 1
                            
            except Exception as e:
                logger.error(f"Error processing business {business_data.get('name')}: {str(e)}")
                
        return processed_count, added_count
        
    def analyze_new_prospects(self, limit: int = 50):
        """Analyze prospects that haven't been analyzed yet"""
        try:
            # Get unanalyzed prospects
            prospects = self.db_service.get_unanalyzed_prospects(limit)
            
            for prospect in prospects:
                try:
                    # Get company data
                    company = self.db_service.get_company(prospect['company_id'])
                    
                    if company:
                        # Prepare data for analysis
                        business_data = {
                            'name': company['name'],
                            'island': company['island'],
                            'industry': company['industry'],
                            'description': company.get('description', ''),
                            'employee_count_estimate': company.get('employee_count_estimate'),
                            'website': company.get('website'),
                            'growth_signals': prospect.get('growth_signals', [])
                        }
                        
                        # Analyze with Claude
                        analysis = self.analyzer.analyze_business(business_data)
                        
                        # Update prospect with analysis
                        self.db_service.update_prospect(prospect['id'], analysis)
                        
                        # Send alert if high priority
                        if analysis['score'] >= int(os.getenv('HIGH_PRIORITY_SCORE', 80)):
                            self._send_high_priority_alert(company, analysis)
                            
                        logger.info(f"Analyzed {company['name']} - Score: {analysis['score']}")
                        
                except Exception as e:
                    logger.error(f"Error analyzing prospect {prospect['id']}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error in analyze_new_prospects: {str(e)}")
            
    def _send_high_priority_alert(self, company: Dict[str, Any], analysis: Dict[str, Any]):
        """Send email alert for high priority prospects"""
        try:
            # This would integrate with email service
            logger.info(f"High priority alert: {company['name']} scored {analysis['score']}")
            
            # Log alert in database
            self.db_service.create_email_alert({
                'prospect_id': analysis.get('prospect_id'),
                'alert_type': 'high_priority',
                'recipient_email': os.getenv('ALERT_EMAIL'),
                'subject': f"High Priority Prospect: {company['name']} (Score: {analysis['score']})",
                'body': f"Company: {company['name']}\nIsland: {company['island']}\n"
                       f"Industry: {company['industry']}\nScore: {analysis['score']}\n\n"
                       f"Analysis: {analysis['ai_analysis']}\n\n"
                       f"Recommended Services: {', '.join(analysis['recommended_services'])}\n"
                       f"Estimated Deal Value: ${analysis['estimated_deal_value']:,.0f}",
                'status': 'pending'
            })
            
        except Exception as e:
            logger.error(f"Error sending high priority alert: {str(e)}")
            
    def enrich_company_data(self, company_id: int):
        """Enrich company data with additional information"""
        # This could include:
        # - LinkedIn company data
        # - Website technology stack analysis
        # - Social media presence
        # - News mentions
        # - Financial data if available
        pass