#!/usr/bin/env python3
"""
Simple re-analysis script that just updates scores and analysis text
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Prospect
from services.claude_analyzer import ClaudeBusinessAnalyzer

def reanalyze_prospects():
    """Re-analyze all prospects with score 0"""
    db = SessionLocal()
    analyzer = ClaudeBusinessAnalyzer()
    
    try:
        # Get prospects with score 0
        prospects = db.query(Prospect).filter(Prospect.score == 0).all()
        print(f"Found {len(prospects)} prospects to re-analyze")
        
        success_count = 0
        for i, prospect in enumerate(prospects):
            company = prospect.company
            print(f"\n[{i+1}/{len(prospects)}] Analyzing {company.name}...")
            
            try:
                # Convert company to dictionary for analyzer
                company_data = {
                    'name': company.name,
                    'island': company.island,
                    'industry': company.industry,
                    'description': company.description or '',
                    'employee_count_estimate': company.employee_count_estimate or 50,
                    'website': company.website or '',
                    'growth_signals': []
                }
                
                # Get AI analysis
                analysis = analyzer.analyze_business(company_data)
                
                if analysis and analysis.get('score', 0) > 0:
                    # Update only the simple fields to avoid enum issues
                    prospect.score = analysis['score']
                    prospect.ai_analysis = analysis.get('ai_analysis', 'AI analysis completed')
                    prospect.priority_level = analysis['priority_level']
                    prospect.technology_readiness = analysis['technology_readiness']
                    prospect.estimated_deal_value = analysis['estimated_deal_value']
                    prospect.last_analyzed = datetime.now()
                    
                    db.commit()
                    success_count += 1
                    print(f"✓ Successfully analyzed - Score: {analysis['score']}, Priority: {analysis['priority_level']}")
                else:
                    print(f"✗ Analysis returned no score")
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                db.rollback()
                
        print(f"\n{success_count}/{len(prospects)} prospects successfully re-analyzed")
        
    finally:
        db.close()

if __name__ == "__main__":
    print("Re-analyzing prospects with Claude AI (simple version)...")
    print("=" * 60)
    reanalyze_prospects()
    
    # Show updated stats
    db = SessionLocal()
    total = db.query(Prospect).count()
    analyzed = db.query(Prospect).filter(Prospect.score > 0).count()
    high_priority = db.query(Prospect).filter(Prospect.priority_level == 'High').count()
    
    print(f"\n{'-' * 60}")
    print(f"Total prospects: {total}")
    print(f"Analyzed prospects: {analyzed}")
    print(f"High priority prospects: {high_priority}")
    db.close()