from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List

from models.database import get_db

router = APIRouter()


@router.get("/")
async def get_prospects(
    island: Optional[str] = None,
    industry: Optional[str] = None,
    min_score: Optional[int] = Query(None, ge=0, le=100),
    priority: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get filtered list of prospects using raw SQL"""
    
    # Build query
    query = """
        SELECT 
            p.id,
            p.score,
            p.ai_analysis,
            p.pain_points,
            p.recommended_services,
            p.estimated_deal_value,
            p.growth_signals,
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
            c.source_url
        FROM prospects p
        JOIN companies c ON p.company_id = c.id
        WHERE 1=1
    """
    
    params = {}
    
    if island:
        query += " AND c.island = :island"
        params['island'] = island
    
    if industry:
        query += " AND c.industry = :industry"
        params['industry'] = industry
    
    if min_score:
        query += " AND p.score >= :min_score"
        params['min_score'] = min_score
    
    if priority:
        query += " AND p.priority_level = :priority"
        params['priority'] = priority
    
    query += " ORDER BY p.score DESC LIMIT :limit OFFSET :offset"
    params['limit'] = limit
    params['offset'] = offset
    
    results = db.execute(text(query), params).fetchall()
    
    prospects = []
    for row in results:
        prospect = {
            "id": row[0],
            "score": row[1],
            "ai_analysis": row[2],
            "pain_points": row[3] if row[3] else [],
            "recommended_services": list(row[4]) if row[4] and isinstance(row[4], (list, tuple)) else [s.strip('" ') for s in row[4].strip('{}').split(',')] if row[4] and isinstance(row[4], str) else [],
            "estimated_deal_value": float(row[5]) if row[5] else 0,
            "growth_signals": row[6] if row[6] else [],
            "technology_readiness": row[7],
            "priority_level": row[8],
            "last_analyzed": row[9].isoformat() if row[9] else None,
            "created_at": row[10].isoformat() if row[10] else None,
            "updated_at": row[11].isoformat() if row[11] else None,
            "company": {
                "id": row[12],
                "name": row[13],
                "address": row[14],
                "island": row[15],
                "industry": row[16],
                "website": row[17],
                "phone": row[18],
                "employee_count_estimate": row[19],
                "annual_revenue_estimate": float(row[20]) if row[20] else 0,
                "description": row[21],
                "source": row[22],
                "source_url": row[23]
            }
        }
        prospects.append(prospect)
    
    return prospects


@router.get("/{prospect_id}")
async def get_prospect_by_id(
    prospect_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific prospect by ID using raw SQL"""
    
    try:
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
                c.source_url
            FROM prospects p
            JOIN companies c ON p.company_id = c.id
            WHERE p.id = :prospect_id
        """
        
        result = db.execute(text(query), {"prospect_id": prospect_id}).fetchone()
        
        if not result:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Prospect not found")
        
        # Convert result to dictionary
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
                "founded_date": None
            },
            # Use default arrays for now - these are stored as PostgreSQL arrays which are complex to parse
            "pain_points": ["Outdated technology infrastructure", "Manual processes", "Limited data insights"],
            "recommended_services": ["Data Analytics", "Custom Chatbots"],
            "growth_signals": ["Expanding operations", "Hiring new staff"]
        }
        
        # Fetch actual pain points, services, and growth signals from database
        array_query = """
            SELECT 
                p.pain_points,
                p.recommended_services,
                p.growth_signals
            FROM prospects p
            WHERE p.id = :prospect_id
        """
        array_result = db.execute(text(array_query), {"prospect_id": prospect_id}).fetchone()
        if array_result:
            if array_result[0]:
                prospect["pain_points"] = array_result[0]
            if array_result[1]:
                # Handle both array and string representations
                services = array_result[1]
                if isinstance(services, str):
                    # Parse PostgreSQL array string format like '{"Data Analytics","Custom Chatbots"}'
                    if services.startswith('{') and services.endswith('}'):
                        services = services[1:-1]  # Remove curly braces
                        # Split by comma and clean up quotes
                        services = [s.strip().strip('"') for s in services.split(',') if s.strip()]
                        prospect["recommended_services"] = services
                    else:
                        prospect["recommended_services"] = [services]
                else:
                    prospect["recommended_services"] = services
            if array_result[2]:
                prospect["growth_signals"] = array_result[2]
        
        # Fetch decision makers
        dm_query = """
            SELECT 
                dm.id,
                dm.name,
                dm.title,
                dm.email,
                dm.phone,
                dm.linkedin_url
            FROM decision_makers dm
            WHERE dm.company_id = :company_id
            ORDER BY dm.name
        """
        dm_results = db.execute(text(dm_query), {"company_id": result[9]}).fetchall()
        
        prospect["decision_makers"] = [
            {
                "id": dm[0],
                "name": dm[1],
                "title": dm[2],
                "email": dm[3],
                "phone": dm[4],
                "linkedin_url": dm[5]
            }
            for dm in dm_results
        ]
        
        return prospect
        
    except Exception as e:
        from fastapi import HTTPException
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=f"Error fetching prospect: {str(e)}")