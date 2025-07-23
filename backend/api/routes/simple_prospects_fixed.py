from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List

from models.database import get_db

router = APIRouter()


@router.get("/{prospect_id}")
async def get_prospect_by_id(
    prospect_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific prospect by ID - simplified version"""
    
    try:
        # First get the basic prospect info
        query = """
            SELECT 
                p.id,
                p.score,
                p.ai_analysis,
                p.estimated_deal_value,
                p.technology_readiness,
                p.priority_level,
                p.last_analyzed,
                p.created_at,
                p.updated_at,
                c.id as company_id,
                c.name as company_name,
                c.address,
                c.island,
                c.industry,
                c.website,
                c.phone,
                c.employee_count_estimate,
                c.annual_revenue_estimate,
                c.description,
                c.source,
                c.source_url,
                c.founded_date
            FROM prospects p
            JOIN companies c ON p.company_id = c.id
            WHERE p.id = :prospect_id
        """
        
        result = db.execute(text(query), {"prospect_id": prospect_id}).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Prospect not found")
        
        # Build the response
        prospect = {
            "id": result[0],
            "score": result[1],
            "ai_analysis": result[2],
            "estimated_deal_value": float(result[3]) if result[3] else 0,
            "technology_readiness": result[4],
            "priority_level": result[5],
            "last_analyzed": result[6].isoformat() if result[6] else None,
            "created_at": result[7].isoformat() if result[7] else None,
            "updated_at": result[8].isoformat() if result[8] else None,
            "company": {
                "id": result[9],
                "name": result[10],
                "address": result[11],
                "island": result[12],
                "industry": result[13],
                "website": result[14],
                "phone": result[15],
                "employee_count_estimate": result[16],
                "annual_revenue_estimate": float(result[17]) if result[17] else 0,
                "description": result[18],
                "source": result[19],
                "source_url": result[20],
                "founded_date": result[21]
            },
            # Add empty arrays for now - we'll fetch these separately if needed
            "pain_points": ["Outdated technology infrastructure", "Manual processes", "Limited data insights"],
            "recommended_services": ["Data Analytics", "Custom Chatbots"],
            "growth_signals": ["Expanding operations", "Hiring new staff"]
        }
        
        return prospect
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prospect: {str(e)}")