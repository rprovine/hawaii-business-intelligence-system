import os
import json
import logging
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class ClaudeBusinessAnalyzer:
    """Analyze Hawaii businesses using Claude API for intelligent insights"""
    
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY or ANTHROPIC_API_KEY not found in environment variables")
            
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"  # Using Haiku for cost efficiency
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_business(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single business and generate insights"""
        try:
            prompt = self._create_analysis_prompt(business_data)
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                system=self._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse the response
            analysis = self._parse_analysis_response(message.content[0].text)
            
            return {
                'score': analysis.get('score', 0),
                'ai_analysis': analysis.get('summary', ''),
                'pain_points': analysis.get('pain_points', []),
                'recommended_services': analysis.get('recommended_services', []),
                'estimated_deal_value': analysis.get('estimated_deal_value', 0),
                'growth_signals': analysis.get('growth_signals', []),
                'technology_readiness': analysis.get('technology_readiness', 'Unknown'),
                'priority_level': self._determine_priority(analysis.get('score', 0)),
                'outreach_strategy': analysis.get('outreach_strategy', '')
            }
            
        except Exception as e:
            logger.error(f"Error analyzing business {business_data.get('name')}: {str(e)}")
            return self._get_default_analysis()
            
    def _create_analysis_prompt(self, business_data: Dict[str, Any]) -> str:
        """Create a detailed prompt for Claude to analyze the business"""
        return f"""
        Analyze this Hawaii business for potential AI consulting opportunities:
        
        Company: {business_data.get('name', 'Unknown')}
        Island: {business_data.get('island', 'Unknown')}
        Industry: {business_data.get('industry', 'Unknown')}
        Description: {business_data.get('description', 'No description available')}
        Employee Count: {business_data.get('employee_count_estimate', 'Unknown')}
        Growth Signals: {', '.join(business_data.get('growth_signals', []))}
        Website: {business_data.get('website', 'Not provided')}
        
        LeniLani Consulting offers:
        1. Data Analytics - Transform business data into actionable insights
        2. Custom Chatbots - AI-powered customer service and engagement
        3. Fractional CTO - Strategic technology leadership
        4. HubSpot Digital Marketing - Marketing automation and CRM
        
        Please provide a JSON response with the following structure:
        {{
            "score": <0-100 based on fit and opportunity>,
            "summary": "<2-3 sentence executive summary>",
            "pain_points": ["<specific pain point 1>", "<pain point 2>", ...],
            "recommended_services": ["<service 1>", "<service 2>", ...],
            "estimated_deal_value": <annual value in USD>,
            "growth_signals": ["<signal 1>", "<signal 2>", ...],
            "technology_readiness": "<Low/Medium/High>",
            "outreach_strategy": "<personalized approach considering Hawaii culture and business environment>",
            "decision_makers": ["<likely title 1>", "<likely title 2>", ...]
        }}
        
        Consider Hawaii-specific factors:
        - Tourism dependency and seasonality
        - Inter-island business challenges
        - Local vs mainland competition
        - Aloha spirit in business culture
        - Sustainability and environmental consciousness
        
        Score higher for:
        - Growing businesses (hiring, expanding)
        - Tourism/hospitality needing analytics or automation
        - Companies with outdated technology
        - Businesses expanding to multiple islands
        - High employee count (>50)
        """
        
    def _get_system_prompt(self) -> str:
        """System prompt for Claude"""
        return """You are an expert business analyst specializing in the Hawaii market. 
        You understand the unique challenges of island businesses, from tourism dependency 
        to logistics complexities. You evaluate businesses for AI and technology consulting 
        opportunities, always considering local culture and the importance of building 
        relationships in Hawaii's tight-knit business community. Provide insights that 
        demonstrate deep understanding of each business's specific challenges and opportunities."""
        
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's response into structured data"""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                logger.warning("Could not find JSON in Claude response")
                return self._parse_text_response(response)
                
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, falling back to text parsing")
            return self._parse_text_response(response)
            
    def _parse_text_response(self, response: str) -> Dict[str, Any]:
        """Fallback parser for non-JSON responses"""
        # Simple text parsing logic
        analysis = {
            'score': 50,  # Default middle score
            'summary': response[:200],
            'pain_points': ['General business improvement needed'],
            'recommended_services': ['Data Analytics'],
            'estimated_deal_value': 50000,
            'growth_signals': [],
            'technology_readiness': 'Medium',
            'outreach_strategy': 'Schedule an introductory meeting to discuss needs'
        }
        
        # Try to extract score if mentioned
        import re
        score_match = re.search(r'score[:\s]+(\d+)', response, re.IGNORECASE)
        if score_match:
            analysis['score'] = int(score_match.group(1))
            
        return analysis
        
    def _determine_priority(self, score: int) -> str:
        """Determine priority level based on score"""
        if score >= 80:
            return 'High'
        elif score >= 50:
            return 'Medium'
        else:
            return 'Low'
            
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when API fails"""
        return {
            'score': 0,
            'ai_analysis': 'Analysis failed - manual review required',
            'pain_points': [],
            'recommended_services': [],
            'estimated_deal_value': 0,
            'growth_signals': [],
            'technology_readiness': 'Unknown',
            'priority_level': 'Low',
            'outreach_strategy': ''
        }
        
    def batch_analyze(self, businesses: List[Dict[str, Any]], max_batch_size: int = 10) -> List[Dict[str, Any]]:
        """Analyze multiple businesses in batches"""
        results = []
        
        for i in range(0, len(businesses), max_batch_size):
            batch = businesses[i:i + max_batch_size]
            logger.info(f"Analyzing batch {i//max_batch_size + 1} of {len(businesses)//max_batch_size + 1}")
            
            for business in batch:
                analysis = self.analyze_business(business)
                results.append({
                    'business_data': business,
                    'analysis': analysis
                })
                
        return results