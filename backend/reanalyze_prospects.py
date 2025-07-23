#!/usr/bin/env python3
"""
Re-analyze prospects with score 0 using Claude API
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Prospect, Company
from services.claude_analyzer import ClaudeBusinessAnalyzer

def map_to_valid_services(services):
    """Map Claude's service recommendations to valid enum values"""
    valid_services = []
    for service in services:
        service_lower = service.lower()
        if 'data analytics' in service_lower or 'analyze' in service_lower:
            valid_services.append('Data Analytics')
        elif 'chatbot' in service_lower or 'customer service' in service_lower:
            valid_services.append('Custom Chatbots')
        elif 'cto' in service_lower or 'technology leadership' in service_lower:
            valid_services.append('Fractional CTO')
        elif 'hubspot' in service_lower or 'digital marketing' in service_lower or 'marketing' in service_lower:
            valid_services.append('HubSpot Digital Marketing')
    
    # Remove duplicates and ensure we have valid services
    valid_services = list(set(valid_services))
    if not valid_services:
        valid_services = ['Data Analytics']  # Default recommendation
    
    return valid_services

def reanalyze_prospects():
    """Re-analyze all prospects with score 0"""
    db = SessionLocal()
    analyzer = ClaudeBusinessAnalyzer()
    
    try:
        # Get prospects with score 0
        prospects = db.query(Prospect).filter(Prospect.score == 0).all()
        print(f"Found {len(prospects)} prospects to re-analyze")
        
        success_count = 0
        for prospect in prospects:
            company = prospect.company
            print(f"\nAnalyzing {company.name}...")
            
            try:
                # Convert company to dictionary for analyzer
                company_data = {
                    'name': company.name,
                    'island': company.island,
                    'industry': company.industry,
                    'description': company.description,
                    'employee_count_estimate': company.employee_count_estimate,
                    'website': company.website,
                    'growth_signals': []
                }
                
                # Get AI analysis
                analysis = analyzer.analyze_business(company_data)
                
                if analysis and analysis.get('score', 0) > 0:
                    # Update prospect
                    prospect.score = analysis['score']
                    prospect.ai_analysis = analysis.get('ai_analysis', 'AI analysis pending')
                    prospect.pain_points = analysis['pain_points']
                    prospect.recommended_services = map_to_valid_services(analysis['recommended_services'])
                    prospect.estimated_deal_value = analysis['estimated_deal_value']
                    prospect.growth_signals = analysis.get('growth_signals', [])
                    prospect.technology_readiness = analysis['technology_readiness']
                    prospect.priority_level = analysis['priority_level']
                    prospect.last_analyzed = datetime.now()
                    
                    db.commit()
                    success_count += 1
                    print(f"✓ Successfully analyzed - Score: {analysis['score']}")
                else:
                    print(f"✗ Analysis failed or returned score 0")
                    
            except Exception as e:
                print(f"✗ Error analyzing {company.name}: {str(e)}")
                db.rollback()
                # Try to at least update the score and analysis
                try:
                    if 'analysis' in locals() and analysis and analysis.get('score', 0) > 0:
                        prospect.score = analysis['score'] 
                        prospect.ai_analysis = analysis.get('ai_analysis', 'AI analysis completed')
                        prospect.priority_level = analysis['priority_level']
                        prospect.technology_readiness = analysis['technology_readiness']
                        prospect.estimated_deal_value = analysis['estimated_deal_value']
                        prospect.last_analyzed = datetime.now()
                        # Skip the problematic fields for now
                        db.commit()
                        print(f"  Partially updated with score: {analysis['score']}")
                except Exception as e2:
                    print(f"  Failed to do partial update: {e2}")
                    db.rollback()
                
        print(f"\n{success_count}/{len(prospects)} prospects successfully re-analyzed")
        
    finally:
        db.close()

if __name__ == "__main__":
    print("Re-analyzing prospects with Claude AI...")
    reanalyze_prospects()