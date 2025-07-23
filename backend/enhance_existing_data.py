#!/usr/bin/env python3
"""
Enhance existing business data with comprehensive AI analysis and real decision makers
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from sqlalchemy import text
import time
import logging
from urllib.parse import urljoin, urlparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal
from services.claude_analyzer import ClaudeBusinessAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBusinessAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.analyzer = ClaudeBusinessAnalyzer()
    
    def extract_decision_makers(self, url, company_name, soup, full_text):
        """Extract real decision makers from website"""
        decision_makers = []
        
        # Common patterns for names and titles
        name_patterns = [
            r'(?:Dr\.|Mr\.|Ms\.|Mrs\.)?\s*([A-Z][a-z]+\s+[A-Z][a-z]+)(?:\s+(?:Jr\.|Sr\.|III|IV|DDS|MD|CPA))?',
            r'([A-Z][a-z]+\s+[A-Z]\.?\s+[A-Z][a-z]+)',  # First Middle Last
        ]
        
        title_patterns = [
            r'(?:President|CEO|Owner|Manager|Director|Partner|Principal|Doctor|Dr|DDS|CPA|Attorney|Lawyer)',
            r'(?:Managing Partner|General Manager|Operations Manager|Practice Manager|Office Manager)',
            r'(?:Founder|Co-Founder|Executive Director|Medical Director|Lead Dentist)'
        ]
        
        # Look for structured data (JSON-LD, microdata)
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict):
                    # Look for person or employee data
                    if data.get('@type') == 'Person':
                        name = data.get('name')
                        title = data.get('jobTitle') or data.get('description', '')
                        email = data.get('email')
                        phone = data.get('telephone')
                        if name:
                            decision_makers.append({
                                'name': name,
                                'title': title,
                                'email': email,
                                'phone': phone,
                                'source': 'structured_data'
                            })
                    elif 'employee' in data or 'founder' in str(data).lower():
                        # Extract employee/founder info
                        employees = data.get('employee', [])
                        if not isinstance(employees, list):
                            employees = [employees]
                        for emp in employees:
                            if isinstance(emp, dict):
                                name = emp.get('name')
                                title = emp.get('jobTitle', '')
                                if name:
                                    decision_makers.append({
                                        'name': name,
                                        'title': title,
                                        'email': emp.get('email'),
                                        'phone': emp.get('telephone'),
                                        'source': 'employee_data'
                                    })
            except:
                continue
        
        # Look for "About Us", "Team", "Staff" pages
        team_links = []
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text().lower()
            if any(word in href or word in text for word in ['about', 'team', 'staff', 'doctor', 'meet', 'biography']):
                if href.startswith('http'):
                    team_links.append(href)
                elif href.startswith('/'):
                    team_links.append(urljoin(url, href))
        
        # Scrape team pages for more detailed info
        for team_url in team_links[:3]:  # Limit to 3 team pages
            try:
                team_response = self.session.get(team_url, timeout=10)
                team_soup = BeautifulSoup(team_response.content, 'html.parser')
                team_text = team_soup.get_text()
                
                # Look for name-title combinations in team pages
                lines = team_text.split('\n')
                for i, line in enumerate(lines):
                    line = line.strip()
                    if len(line) > 5 and len(line) < 100:
                        # Check if this line contains a name
                        for name_pattern in name_patterns:
                            name_match = re.search(name_pattern, line)
                            if name_match:
                                name = name_match.group(1) if name_match.lastindex else name_match.group(0)
                                
                                # Look for title in surrounding lines
                                title = ""
                                for j in range(max(0, i-2), min(len(lines), i+3)):
                                    if j != i:
                                        for title_pattern in title_patterns:
                                            if re.search(title_pattern, lines[j], re.IGNORECASE):
                                                title = lines[j].strip()
                                                break
                                        if title:
                                            break
                                
                                # Extract email if nearby
                                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', team_text[max(0, team_text.find(name)-200):team_text.find(name)+200])
                                email = email_match.group(0) if email_match else None
                                
                                if name and any(word in name for word in ['Dr', 'CEO', 'President', 'Manager', 'Director']):
                                    decision_makers.append({
                                        'name': name,
                                        'title': title or 'Key Personnel',
                                        'email': email,
                                        'phone': None,
                                        'source': 'team_page'
                                    })
                                break
                
            except Exception as e:
                logger.warning(f"Failed to scrape team page {team_url}: {e}")
                continue
            
            time.sleep(1)  # Be respectful
        
        # Fallback: Extract from main page content
        if not decision_makers:
            # Look for patterns like "Dr. Smith, DDS" or "John Doe, CEO"
            main_text_lines = full_text.split('\n')
            for line in main_text_lines:
                line = line.strip()
                if 20 < len(line) < 150:  # Reasonable length for name+title
                    # Pattern: Name, Title or Title Name
                    patterns = [
                        r'(Dr\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+)(?:,\s*)?(DDS|MD|CPA)?',
                        r'([A-Z][a-z]+\s+[A-Z][a-z]+)(?:,\s*)?(CEO|President|Owner|Manager|Director|Principal)',
                        r'(President|CEO|Owner|Director|Manager)(?:\s*:?\s*)([A-Z][a-z]+\s+[A-Z][a-z]+)'
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            if 'Dr.' in match.group(0) or any(title in match.group(0) for title in ['CEO', 'President', 'Owner']):
                                groups = match.groups()
                                if len(groups) >= 2:
                                    if groups[0] in ['President', 'CEO', 'Owner', 'Director', 'Manager']:
                                        name = groups[1]
                                        title = groups[0]
                                    else:
                                        name = groups[0]
                                        title = groups[1] if groups[1] else 'Key Personnel'
                                else:
                                    name = groups[0]
                                    title = 'Owner'
                                
                                decision_makers.append({
                                    'name': name.strip(),
                                    'title': title.strip(),
                                    'email': None,
                                    'phone': None,
                                    'source': 'main_page'
                                })
                                break
        
        # Generate email from domain if not found
        domain = urlparse(url).netloc.replace('www.', '')
        for dm in decision_makers:
            if not dm['email']:
                # Generate professional email
                name_parts = dm['name'].lower().split()
                if len(name_parts) >= 2:
                    dm['email'] = f"{name_parts[0]}.{name_parts[-1]}@{domain}"
                else:
                    dm['email'] = f"{name_parts[0]}@{domain}"
        
        # Remove duplicates and limit to top 3
        seen_names = set()
        unique_dms = []
        for dm in decision_makers:
            if dm['name'] not in seen_names:
                seen_names.add(dm['name'])
                unique_dms.append(dm)
                if len(unique_dms) >= 3:
                    break
        
        return unique_dms
    
    def create_comprehensive_analysis(self, business_data, decision_makers, website_content):
        """Create comprehensive AI analysis using all scraped data"""
        
        # Enhanced business data with scraped content
        enhanced_data = {**business_data}
        enhanced_data['website_content_length'] = len(website_content)
        enhanced_data['decision_makers_found'] = len(decision_makers)
        enhanced_data['decision_maker_titles'] = [dm['title'] for dm in decision_makers]
        enhanced_data['has_professional_website'] = len(website_content) > 1000
        
        # Create detailed prompt for Claude
        prompt = f"""
As an expert AI consultant for Hawaii businesses, provide a comprehensive analysis for LeniLani Consulting:

BUSINESS PROFILE:
Company: {business_data['name']}
Industry: {business_data['industry']}
Location: {business_data['island']}, Hawaii
Website: {business_data['website']}
Employees: {business_data['employee_count']}
Description: {business_data['description']}
Google Rating: {business_data.get('google_rating', 'N/A')}/5

DECISION MAKERS IDENTIFIED:
{', '.join([f"{dm['name']} ({dm['title']})" for dm in decision_makers]) if decision_makers else 'None found'}

WEBSITE ANALYSIS:
Content Length: {len(website_content)} characters
Professional Quality: {'High' if len(website_content) > 2000 else 'Medium' if len(website_content) > 500 else 'Basic'}

PROVIDE DETAILED ANALYSIS:

1. OPPORTUNITY ASSESSMENT (Score 0-100):
Consider business size, digital presence, industry growth potential, and Hawaii market position.

2. COMPREHENSIVE BUSINESS ANALYSIS (300+ words):
- Current market position in Hawaii
- Digital transformation readiness
- Specific operational challenges this industry faces in Hawaii
- Competitive landscape and AI opportunity
- Growth trajectory and expansion potential
- Technology adoption indicators from website quality

3. CRITICAL PAIN POINTS (5 specific issues):
- Current inefficiencies based on industry and size
- Hawaii-specific challenges (tourism dependency, inter-island logistics, etc.)
- Customer service bottlenecks
- Data and analytics gaps
- Marketing and growth limitations

4. AI SERVICE RECOMMENDATIONS (2-3 most impactful):
From: Data Analytics, Custom Chatbots, HubSpot Digital Marketing, Fractional CTO
Explain WHY each service addresses specific pain points.

5. GROWTH SIGNALS & READINESS INDICATORS:
- Business stability markers
- Technology adoption signs
- Expansion opportunities
- Investment capacity indicators

6. DETAILED SALES STRATEGY:
- Primary decision maker approach ({decision_makers[0]['name'] + ' (' + decision_makers[0]['title'] + ')' if decision_makers else 'Owner/Manager'})
- Key value propositions to emphasize
- Hawaii cultural considerations
- Specific conversation starters
- Objection handling strategies

7. ROI PROJECTIONS:
- Conservative estimate
- Optimistic scenario
- Timeline to value
- Success metrics

8. COMPETITIVE INTELLIGENCE:
- Likely current technology stack
- Competitor advantage opportunities
- Market positioning benefits

Format as detailed JSON with comprehensive explanations for each section.
"""

        try:
            # Use Claude to generate comprehensive analysis
            message = self.analyzer.client.messages.create(
                model="claude-3-sonnet-20240229",  # Use Sonnet for higher quality analysis
                max_tokens=3000,  # Increased for comprehensive analysis
                temperature=0.7,
                system="""You are an expert AI consultant specializing in Hawaii businesses. 
                Provide detailed, actionable insights that demonstrate deep understanding of 
                each business's specific challenges and opportunities in the Hawaii market.""",
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # Try to extract JSON, fallback to structured text
            try:
                import json
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    analysis_data = json.loads(json_str)
                else:
                    # Create structured analysis from text
                    analysis_data = self._parse_text_analysis(response_text, business_data)
            except:
                analysis_data = self._parse_text_analysis(response_text, business_data)
            
            return analysis_data
            
        except Exception as e:
            logger.error(f"Claude analysis failed: {e}")
            return self._create_fallback_analysis(business_data, decision_makers)
    
    def _parse_text_analysis(self, text, business_data):
        """Parse text response into structured format"""
        # Extract score
        score_match = re.search(r'(?:score|assessment).*?(\d{1,3})', text, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 75
        
        return {
            'score': min(score, 100),
            'summary': text[:500] + "..." if len(text) > 500 else text,
            'pain_points': self._extract_pain_points(text),
            'recommended_services': ['Data Analytics', 'Custom Chatbots'],
            'estimated_deal_value': business_data['employee_count'] * 3000,
            'growth_signals': [f"Established {business_data['industry']} business in {business_data['island']}"],
            'technology_readiness': 'Medium'
        }
    
    def _extract_pain_points(self, text):
        """Extract pain points from text"""
        pain_points = []
        lines = text.split('\n')
        
        for line in lines:
            if ('•' in line or '-' in line) and any(word in line.lower() for word in ['challenge', 'problem', 'issue', 'pain', 'difficulty']):
                clean_line = line.strip('•- ').strip()
                if 20 < len(clean_line) < 200:
                    pain_points.append(clean_line)
                    if len(pain_points) >= 3:
                        break
        
        if not pain_points:
            # Generic industry pain points
            pain_points = [
                "Manual processes limiting operational efficiency",
                "Limited data insights for strategic decision making",
                "Customer service bottlenecks during peak periods"
            ]
        
        return pain_points[:3]
    
    def _create_fallback_analysis(self, business_data, decision_makers):
        """Create fallback analysis if Claude fails"""
        return {
            'score': 75,
            'summary': f"{business_data['name']} is a {business_data['industry']} business in {business_data['island']} with significant potential for AI automation and data analytics improvements.",
            'pain_points': [
                "Manual processes limiting scalability",
                "Limited customer data insights",
                "Operational inefficiencies during peak periods"
            ],
            'recommended_services': ['Data Analytics', 'Custom Chatbots'],
            'estimated_deal_value': business_data['employee_count'] * 3000,
            'growth_signals': [f"Established business with {business_data['employee_count']} employees"],
            'technology_readiness': 'Medium'
        }

def enhance_all_existing_businesses():
    """Enhance all existing businesses with comprehensive analysis and decision makers"""
    analyzer = EnhancedBusinessAnalyzer()
    db = SessionLocal()
    
    try:
        # Get all companies
        companies = db.execute(text("""
            SELECT id, name, website, industry, island, employee_count_estimate, 
                   description, phone, address
            FROM companies
        """)).fetchall()
        
        logger.info(f"Enhancing {len(companies)} businesses...")
        
        for company in companies:
            company_id, name, website, industry, island, employee_count, description, phone, address = company
            
            logger.info(f"\nEnhancing {name}...")
            
            if not website:
                logger.warning(f"No website for {name}, skipping")
                continue
            
            try:
                # Scrape website for comprehensive data
                response = analyzer.session.get(website, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                full_text = soup.get_text()
                
                # Extract decision makers
                decision_makers = analyzer.extract_decision_makers(website, name, soup, full_text)
                logger.info(f"  Found {len(decision_makers)} decision makers")
                
                # Create comprehensive business data
                business_data = {
                    'name': name,
                    'industry': industry,
                    'island': island,
                    'employee_count': employee_count,
                    'description': description,
                    'website': website,
                    'phone': phone,
                    'address': address,
                    'google_rating': None  # Could enhance with Google Places data
                }
                
                # Get comprehensive AI analysis
                analysis = analyzer.create_comprehensive_analysis(business_data, decision_makers, full_text)
                logger.info(f"  Generated comprehensive analysis ({len(str(analysis))} chars)")
                
                # Update prospect with enhanced analysis
                services_array = '{' + ','.join([f'"{s}"' for s in analysis.get('recommended_services', ['Data Analytics'])]) + '}'
                pain_points_array = '{' + ','.join([f'"{p}"' for p in analysis.get('pain_points', [])]) + '}'
                growth_signals_array = '{' + ','.join([f'"{g}"' for g in analysis.get('growth_signals', [])]) + '}'
                
                db.execute(text("""
                    UPDATE prospects SET 
                        score = :score,
                        ai_analysis = :analysis,
                        pain_points = :pain_points,
                        recommended_services = :services,
                        growth_signals = :growth_signals,
                        technology_readiness = :tech_readiness,
                        estimated_deal_value = :deal_value,
                        last_analyzed = NOW()
                    WHERE company_id = :company_id
                """), {
                    'score': analysis.get('score', 75),
                    'analysis': analysis.get('summary', ''),
                    'pain_points': pain_points_array,
                    'services': services_array,
                    'growth_signals': growth_signals_array,
                    'tech_readiness': analysis.get('technology_readiness', 'Medium'),
                    'deal_value': analysis.get('estimated_deal_value', 50000),
                    'company_id': company_id
                })
                
                # Clear existing decision makers and add new ones
                db.execute(text("DELETE FROM decision_makers WHERE company_id = :id"), {'id': company_id})
                
                for dm in decision_makers:
                    db.execute(text("""
                        INSERT INTO decision_makers (company_id, name, title, email, phone)
                        VALUES (:company_id, :name, :title, :email, :phone)
                    """), {
                        'company_id': company_id,
                        'name': dm['name'],
                        'title': dm['title'],
                        'email': dm['email'],
                        'phone': dm['phone'] or phone  # Use company phone as fallback
                    })
                    logger.info(f"  ✅ Added: {dm['name']} ({dm['title']})")
                
                db.commit()
                
            except Exception as e:
                logger.error(f"Failed to enhance {name}: {e}")
                db.rollback()
                continue
            
            time.sleep(2)  # Be respectful with requests
        
        logger.info("\n✅ Enhancement complete!")
        
        # Summary
        total_dms = db.execute(text("SELECT COUNT(*) FROM decision_makers")).fetchone()[0]
        avg_analysis_length = db.execute(text("SELECT AVG(LENGTH(ai_analysis)) FROM prospects")).fetchone()[0]
        
        logger.info(f"Results:")
        logger.info(f"  Total decision makers: {total_dms}")
        logger.info(f"  Average analysis length: {avg_analysis_length:.0f} characters")
        
    except Exception as e:
        logger.error(f"Enhancement failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    enhance_all_existing_businesses()