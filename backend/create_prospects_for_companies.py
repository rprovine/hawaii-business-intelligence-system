#!/usr/bin/env python3
"""
Create prospects for existing companies
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Company, Prospect
from services.claude_analyzer import ClaudeBusinessAnalyzer

def create_prospects():
    """Create prospects for all companies without prospects"""
    db = SessionLocal()
    analyzer = ClaudeBusinessAnalyzer()
    
    try:
        # Get companies without prospects
        companies = db.query(Company).outerjoin(Prospect).filter(Prospect.id == None).all()
        print(f"Found {len(companies)} companies without prospects")
        
        for company in companies:
            print(f"\nAnalyzing {company.name}...")
            
            try:
                # Convert to dict for analyzer
                company_data = {
                    'name': company.name,
                    'island': company.island,
                    'industry': company.industry,
                    'description': company.description or '',
                    'employee_count_estimate': company.employee_count_estimate or 50,
                    'website': company.website or '',
                    'annual_revenue_estimate': company.annual_revenue_estimate,
                    'founded_date': company.founded_date if hasattr(company, 'founded_date') else None
                }
                
                # Get AI analysis
                analysis = analyzer.analyze_business(company_data)
                
                if analysis:
                    # Create prospect
                    prospect = Prospect(
                        company_id=company.id,
                        score=analysis.get('score', 75),
                        ai_analysis=analysis.get('ai_analysis', 'AI analysis pending'),
                        pain_points=analysis.get('pain_points', []),
                        recommended_services=analysis.get('recommended_services', ['Data Analytics']),
                        estimated_deal_value=analysis.get('estimated_deal_value', 50000),
                        growth_signals=analysis.get('growth_signals', []),
                        technology_readiness=analysis.get('technology_readiness', 'Medium'),
                        priority_level=analysis.get('priority_level', 'Medium'),
                        last_analyzed=datetime.now()
                    )
                    
                    db.add(prospect)
                    db.commit()
                    print(f"✓ Created prospect - Score: {prospect.score}, Priority: {prospect.priority_level}")
                else:
                    print(f"✗ No analysis returned")
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                db.rollback()
        
        # Show summary
        total_prospects = db.query(Prospect).count()
        print(f"\n{'='*60}")
        print(f"Total prospects in system: {total_prospects}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating prospects for companies...")
    print("="*60)
    create_prospects()