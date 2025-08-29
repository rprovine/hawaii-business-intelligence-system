"""
Vercel Serverless Function API for Hawaii Business Intelligence
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        path = self.path
        
        # Basic routes
        if path == "/" or path == "/api":
            response = {
                "message": "Hawaii Business Intelligence System API",
                "version": "1.0.0",
                "status": "operational"
            }
        elif path == "/api/health":
            response = {"status": "healthy"}
        elif path == "/api/analytics/dashboard":
            response = {
                "total_companies": 15,
                "total_prospects": 15,
                "active_workflows": 3,
                "recent_interactions": 8,
                "high_score_prospects": 12,
                "average_score": 85
            }
        elif path == "/api/companies":
            response = [
                {"id": 1, "name": "Aloha Medical Center", "island": "Oahu", "industry": "Healthcare"},
                {"id": 2, "name": "Pacific Paradise Resort", "island": "Maui", "industry": "Tourism"},
                {"id": 3, "name": "Kona Coffee Collective", "island": "Big Island", "industry": "Food Service"},
                {"id": 4, "name": "Island Tech Solutions", "island": "Oahu", "industry": "Technology"},
                {"id": 5, "name": "Kauai Adventure Tours", "island": "Kauai", "industry": "Tourism"}
            ]
        elif path == "/api/prospects":
            response = [
                {"id": 1, "company_id": 1, "score": 92, "company_name": "Aloha Medical Center", "ai_analysis": "High potential for AI integration in patient management systems."},
                {"id": 2, "company_id": 2, "score": 88, "company_name": "Pacific Paradise Resort", "ai_analysis": "Strong candidate for AI-powered booking and guest experience."},
                {"id": 3, "company_id": 3, "score": 85, "company_name": "Kona Coffee Collective", "ai_analysis": "Could benefit from AI in supply chain and customer analytics."},
                {"id": 4, "company_id": 4, "score": 95, "company_name": "Island Tech Solutions", "ai_analysis": "Already tech-savvy, perfect for advanced AI solutions."},
                {"id": 5, "company_id": 5, "score": 87, "company_name": "Kauai Adventure Tours", "ai_analysis": "AI can optimize tour scheduling and personalization."}
            ]
        elif path == "/api/analytics/by-island":
            response = {"Oahu": 5, "Maui": 3, "Big Island": 3, "Kauai": 2, "Molokai": 1, "Lanai": 1}
        elif path == "/api/analytics/by-industry":
            response = {"Tourism": 5, "Healthcare": 3, "Technology": 3, "Food Service": 2, "Real Estate": 2}
        elif path == "/api/workflows/status":
            response = {"active": 3, "completed": 12, "failed": 0}
        elif path == "/api/interactions":
            response = []
        else:
            response = {"error": "Not found", "path": path}
        
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return