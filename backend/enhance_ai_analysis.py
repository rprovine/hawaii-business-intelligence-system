#!/usr/bin/env python3
"""
Enhance AI analysis with detailed, actionable insights
"""

import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from models.models import Company, Prospect
from services.claude_analyzer import ClaudeBusinessAnalyzer

# Detailed company insights for rich AI analysis
COMPANY_INSIGHTS = {
    'Pacific Digital Partners': {
        'key_decision_makers': [
            {'name': 'Sarah Chen', 'title': 'CEO & Founder', 'approach': 'Tech-savvy, data-driven decision maker'},
            {'name': 'Mike Tanaka', 'title': 'VP of Client Services', 'approach': 'Focused on client retention and satisfaction'}
        ],
        'current_challenges': [
            'Scaling personalized service as client base grows',
            'Managing multiple client campaigns across different platforms',
            'Proving ROI to clients with limited analytics capabilities',
            'Competing with mainland agencies with larger resources'
        ],
        'technology_gaps': [
            'No unified dashboard for client campaign performance',
            'Manual reporting processes taking 10+ hours weekly',
            'Limited predictive analytics for campaign optimization',
            'No AI-powered content generation tools'
        ],
        'conversation_starters': [
            'How are you currently measuring campaign effectiveness across different clients?',
            'What percentage of your team\'s time is spent on reporting vs strategy?',
            'Have you explored AI tools for content generation or campaign optimization?'
        ],
        'value_proposition': 'Our AI-powered analytics platform can reduce reporting time by 80% while providing predictive insights that improve campaign performance by 25-40%.',
        'competitive_advantage': 'As a local Hawaii company, you understand the unique market dynamics here. AI tools can amplify this advantage by automating routine tasks so your team can focus on strategy.',
        'estimated_ai_roi': '3-5x ROI within 6 months through time savings and improved campaign performance'
    },
    
    'Aloha Family Dental': {
        'key_decision_makers': [
            {'name': 'Dr. James Wong', 'title': 'Owner & Lead Dentist', 'approach': 'Patient-focused, cautious about new technology'},
            {'name': 'Lisa Nakamura', 'title': 'Office Manager', 'approach': 'Efficiency-driven, handles day-to-day operations'}
        ],
        'current_challenges': [
            'High no-show rates (15-20%) impacting revenue',
            'Phone tag with patients for appointment scheduling',
            'Managing waitlists for popular time slots',
            'Patient intake forms still paper-based',
            'Difficulty tracking treatment plan compliance'
        ],
        'technology_gaps': [
            'No automated appointment reminders beyond basic emails',
            'Cannot handle after-hours scheduling requests',
            'No patient self-service portal',
            'Limited data on patient preferences and behaviors'
        ],
        'conversation_starters': [
            'What\'s your current no-show rate and how much revenue does that represent?',
            'How many hours per week does your staff spend on phone scheduling?',
            'Do patients ever complain about not being able to book appointments online?'
        ],
        'value_proposition': 'Our AI chatbot can handle 24/7 appointment scheduling, reduce no-shows by 40%, and free up 15 hours of staff time weekly for patient care.',
        'competitive_advantage': 'While other practices struggle with staffing, you can offer superior patient experience with AI handling routine communications.',
        'estimated_ai_roi': '$150K+ annual savings from reduced no-shows and staff efficiency'
    },
    
    'Kauai Adventure Tours': {
        'key_decision_makers': [
            {'name': 'Dave Mitchell', 'title': 'Owner', 'approach': 'Adventure enthusiast, values customer experience above all'},
            {'name': 'Keiko Yamada', 'title': 'Operations Manager', 'approach': 'Safety-focused, manages logistics'}
        ],
        'current_challenges': [
            'Seasonal booking fluctuations (40% variance)',
            'Last-minute cancellations due to weather',
            'Managing inventory for equipment across multiple tour types',
            'Coordinating guides and equipment for multi-day tours',
            'Competing with larger tour operators on TripAdvisor'
        ],
        'technology_gaps': [
            'Manual booking system requiring phone/email confirmation',
            'No dynamic pricing based on demand',
            'Cannot automatically rebook weather cancellations',
            'No predictive analytics for staffing needs',
            'Limited customer data for personalization'
        ],
        'conversation_starters': [
            'How do you currently handle weather-related cancellations and rebookings?',
            'What\'s your strategy for managing inventory during peak vs slow seasons?',
            'How much time does your team spend on booking management vs customer experience?'
        ],
        'value_proposition': 'AI-powered booking system with dynamic pricing can increase revenue 20-30% while automating 80% of routine customer communications.',
        'competitive_advantage': 'Offer instant booking confirmation and personalized tour recommendations that larger operators can\'t match.',
        'estimated_ai_roi': '$200K+ additional revenue through optimized pricing and reduced cancellations'
    },
    
    'Island Home Builders': {
        'key_decision_makers': [
            {'name': 'Robert Kahale', 'title': 'President', 'approach': 'Quality-focused, relationship-driven'},
            {'name': 'Jennifer Park', 'title': 'Project Director', 'approach': 'Detail-oriented, manages timelines'}
        ],
        'current_challenges': [
            'Project delays due to material availability',
            'Client communication gaps during build process',
            'Subcontractor scheduling conflicts',
            'Change order management causing budget overruns',
            'Competing with larger builders on price'
        ],
        'technology_gaps': [
            'No centralized project communication platform',
            'Manual scheduling using spreadsheets',
            'No automated progress updates for clients',
            'Limited visibility into material lead times',
            'Paper-based change order process'
        ],
        'conversation_starters': [
            'How do you keep clients informed during the 6-12 month build process?',
            'What\'s your biggest source of project delays?',
            'How do you differentiate from larger builders beyond craftsmanship?'
        ],
        'value_proposition': 'AI project management system provides real-time updates to clients, predicts delays before they happen, and reduces project timeline by 15-20%.',
        'competitive_advantage': 'Offer transparency and communication that builds trust and justifies premium pricing.',
        'estimated_ai_roi': 'Save $50K per project through better scheduling and reduce costly delays'
    }
}

def create_detailed_analysis(company_name: str, company_data: dict) -> str:
    """Create a detailed AI analysis for a company"""
    
    insights = COMPANY_INSIGHTS.get(company_name, {})
    
    # Build comprehensive analysis
    analysis = f"## Strategic Analysis for {company_name}\n\n"
    
    # Company Overview
    analysis += f"**Company Profile**: {company_data.get('description', '')}\n"
    analysis += f"**Size**: {company_data.get('employee_count_estimate', 'Unknown')} employees"
    if company_data.get('annual_revenue_estimate'):
        analysis += f" | ~${company_data['annual_revenue_estimate']/1000000:.1f}M annual revenue"
    analysis += f"\n**Industry**: {company_data.get('industry', 'Unknown')}\n\n"
    
    # Current Challenges
    if insights.get('current_challenges'):
        analysis += "### Key Business Challenges\n"
        for challenge in insights['current_challenges']:
            analysis += f"• {challenge}\n"
        analysis += "\n"
    
    # Technology Gaps
    if insights.get('technology_gaps'):
        analysis += "### Technology Gap Analysis\n"
        for gap in insights['technology_gaps']:
            analysis += f"• {gap}\n"
        analysis += "\n"
    
    # Decision Makers
    if insights.get('key_decision_makers'):
        analysis += "### Key Decision Makers\n"
        for dm in insights['key_decision_makers']:
            analysis += f"• **{dm['name']}** ({dm['title']}): {dm['approach']}\n"
        analysis += "\n"
    
    # Value Proposition
    if insights.get('value_proposition'):
        analysis += f"### LeniLani Value Proposition\n{insights['value_proposition']}\n\n"
    
    # ROI Estimation
    if insights.get('estimated_ai_roi'):
        analysis += f"### Estimated ROI\n{insights['estimated_ai_roi']}\n\n"
    
    # Conversation Starters
    if insights.get('conversation_starters'):
        analysis += "### Conversation Starters\n"
        for i, starter in enumerate(insights['conversation_starters'], 1):
            analysis += f"{i}. {starter}\n"
        analysis += "\n"
    
    # Competitive Positioning
    if insights.get('competitive_advantage'):
        analysis += f"### Competitive Positioning\n{insights['competitive_advantage']}\n\n"
    
    # Recommended Approach
    analysis += "### Recommended Sales Approach\n"
    analysis += "1. **Initial Contact**: Lead with industry-specific pain point\n"
    analysis += "2. **Discovery**: Focus on quantifying current inefficiencies\n"
    analysis += "3. **Demo**: Show similar business success stories\n"
    analysis += "4. **Proposal**: Emphasize ROI and competitive advantage\n"
    analysis += "5. **Close**: Offer pilot program with success metrics\n"
    
    return analysis

def enhance_all_prospects():
    """Enhance all prospects with detailed AI analysis"""
    db = SessionLocal()
    analyzer = ClaudeBusinessAnalyzer()
    
    try:
        # Get all prospects with their companies
        prospects = db.query(Prospect).join(Company).all()
        print(f"Enhancing {len(prospects)} prospects with detailed analysis...")
        
        enhanced = 0
        for prospect in prospects:
            company = prospect.company
            print(f"\nEnhancing {company.name}...")
            
            try:
                # Create company data dict
                company_data = {
                    'name': company.name,
                    'description': company.description,
                    'employee_count_estimate': company.employee_count_estimate,
                    'annual_revenue_estimate': company.annual_revenue_estimate,
                    'industry': company.industry,
                    'island': company.island
                }
                
                # Get detailed analysis
                if company.name in COMPANY_INSIGHTS:
                    # Use our detailed insights
                    detailed_analysis = create_detailed_analysis(company.name, company_data)
                    
                    # Update pain points with specific challenges
                    prospect.pain_points = COMPANY_INSIGHTS[company.name].get('current_challenges', [])[:3]
                    
                    # Update growth signals
                    prospect.growth_signals = [
                        f"{company.employee_count_estimate} employees indicates established operations",
                        f"Located in growing {company.island} market",
                        "Ready for digital transformation"
                    ]
                else:
                    # Use Claude for other companies
                    analysis_result = analyzer.analyze_business(company_data)
                    if analysis_result:
                        detailed_analysis = f"## Strategic Analysis for {company.name}\n\n"
                        detailed_analysis += analysis_result.get('ai_analysis', '')
                        detailed_analysis += "\n\n### Recommended Approach\n"
                        detailed_analysis += "1. Understand their current technology stack\n"
                        detailed_analysis += "2. Identify biggest operational pain points\n"
                        detailed_analysis += "3. Demonstrate relevant AI solutions\n"
                        detailed_analysis += "4. Provide clear ROI calculations\n"
                    else:
                        continue
                
                # Update prospect
                prospect.ai_analysis = detailed_analysis
                prospect.last_analyzed = datetime.now()
                
                # Adjust scores based on fit
                if company.employee_count_estimate <= 30 and company.industry in ['Technology', 'Healthcare']:
                    prospect.score = min(prospect.score + 5, 95)
                
                db.commit()
                enhanced += 1
                print(f"✓ Enhanced with {len(detailed_analysis)} characters of analysis")
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                db.rollback()
        
        print(f"\n✓ Enhanced {enhanced}/{len(prospects)} prospects")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Enhancing AI analysis for all prospects...")
    print("="*60)
    enhance_all_prospects()