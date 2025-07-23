#!/usr/bin/env python3
"""
Create prospects for existing companies - simple version
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Company, Prospect, ServiceEnum

def create_prospects():
    """Create prospects for all companies without prospects"""
    db = SessionLocal()
    
    try:
        # Get companies without prospects
        companies = db.query(Company).outerjoin(Prospect).filter(Prospect.id == None).all()
        print(f"Found {len(companies)} companies without prospects")
        
        for company in companies:
            print(f"\nCreating prospect for {company.name}...")
            
            try:
                # Determine services based on industry
                services = []
                if company.industry in ['Healthcare', 'Hospitality', 'Real Estate']:
                    services = [ServiceEnum.DATA_ANALYTICS, ServiceEnum.CUSTOM_CHATBOTS]
                elif company.industry == 'Other':
                    # For banks, utilities, schools
                    if 'Bank' in company.name or 'Electric' in company.name:
                        services = [ServiceEnum.DATA_ANALYTICS, ServiceEnum.FRACTIONAL_CTO]
                    else:
                        services = [ServiceEnum.DATA_ANALYTICS, ServiceEnum.HUBSPOT_MARKETING]
                else:
                    services = [ServiceEnum.DATA_ANALYTICS]
                
                # Calculate score based on employee count and revenue
                score = 70
                if company.employee_count_estimate and company.employee_count_estimate > 500:
                    score += 10
                if company.annual_revenue_estimate and company.annual_revenue_estimate > 100000000:
                    score += 10
                
                # Determine priority
                priority = 'Medium'
                if score >= 80:
                    priority = 'High'
                elif score < 60:
                    priority = 'Low'
                
                # Create simple analysis
                analysis = f"{company.name} is a {company.industry.lower()} company on {company.island} "
                if company.employee_count_estimate:
                    analysis += f"with approximately {company.employee_count_estimate} employees. "
                analysis += f"They would benefit from AI consulting services to modernize operations and improve efficiency."
                
                # Pain points
                pain_points = [
                    "Manual processes slowing operations",
                    "Limited data visibility for decision making",
                    "Need for improved customer engagement"
                ]
                
                # Create prospect
                prospect = Prospect(
                    company_id=company.id,
                    score=score,
                    ai_analysis=analysis,
                    pain_points=pain_points,
                    recommended_services=services,
                    estimated_deal_value=100000 if score >= 80 else 50000,
                    growth_signals=["Established market presence", "Growth potential identified"],
                    technology_readiness='Medium',
                    priority_level=priority,
                    last_analyzed=datetime.now()
                )
                
                db.add(prospect)
                db.commit()
                print(f"✓ Created prospect - Score: {score}, Priority: {priority}")
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                db.rollback()
        
        # Show summary
        total_prospects = db.query(Prospect).count()
        total_companies = db.query(Company).count()
        print(f"\n{'='*60}")
        print(f"Total companies: {total_companies}")
        print(f"Total prospects: {total_prospects}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating prospects for companies (simple version)...")
    print("="*60)
    create_prospects()