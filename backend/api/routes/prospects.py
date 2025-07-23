from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.database import get_db
from models.models import Prospect, Company, IslandEnum, IndustryEnum
from api.schemas import ProspectResponse, ProspectCreate, ProspectUpdate
from services.claude_analyzer import ClaudeBusinessAnalyzer

router = APIRouter()


@router.get("/", response_model=List[ProspectResponse])
async def get_prospects(
    island: Optional[IslandEnum] = None,
    industry: Optional[IndustryEnum] = None,
    min_score: Optional[int] = Query(None, ge=0, le=100),
    priority: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get filtered list of prospects"""
    query = db.query(Prospect).join(Company)
    
    if island:
        query = query.filter(Company.island == island)
    if industry:
        query = query.filter(Company.industry == industry)
    if min_score:
        query = query.filter(Prospect.score >= min_score)
    if priority:
        query = query.filter(Prospect.priority_level == priority)
        
    prospects = query.order_by(Prospect.score.desc()).offset(offset).limit(limit).all()
    return prospects


@router.get("/{prospect_id}", response_model=ProspectResponse)
async def get_prospect(prospect_id: int, db: Session = Depends(get_db)):
    """Get a specific prospect by ID"""
    prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return prospect


@router.post("/", response_model=ProspectResponse)
async def create_prospect(prospect: ProspectCreate, db: Session = Depends(get_db)):
    """Create a new prospect"""
    # Check if company exists
    company = db.query(Company).filter(Company.id == prospect.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
        
    # Create prospect
    db_prospect = Prospect(**prospect.dict())
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    return db_prospect


@router.put("/{prospect_id}", response_model=ProspectResponse)
async def update_prospect(
    prospect_id: int,
    prospect_update: ProspectUpdate,
    db: Session = Depends(get_db)
):
    """Update a prospect"""
    prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
        
    for field, value in prospect_update.dict(exclude_unset=True).items():
        setattr(prospect, field, value)
        
    prospect.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(prospect)
    return prospect


@router.post("/{prospect_id}/analyze")
async def analyze_prospect(prospect_id: int, db: Session = Depends(get_db)):
    """Re-analyze a prospect using Claude API"""
    prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
        
    # Get company data
    company = prospect.company
    
    # Analyze with Claude
    analyzer = ClaudeBusinessAnalyzer()
    analysis = analyzer.analyze_business({
        'name': company.name,
        'island': company.island.value,
        'industry': company.industry.value,
        'description': company.description,
        'employee_count_estimate': company.employee_count_estimate,
        'website': company.website,
        'growth_signals': prospect.growth_signals or []
    })
    
    # Update prospect with new analysis
    for field, value in analysis.items():
        setattr(prospect, field, value)
        
    prospect.last_analyzed = datetime.utcnow()
    db.commit()
    db.refresh(prospect)
    
    return {"message": "Prospect re-analyzed successfully", "new_score": prospect.score}


@router.delete("/{prospect_id}")
async def delete_prospect(prospect_id: int, db: Session = Depends(get_db)):
    """Delete a prospect"""
    prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
        
    db.delete(prospect)
    db.commit()
    return {"message": "Prospect deleted successfully"}


@router.get("/high-priority/summary")
async def get_high_priority_summary(db: Session = Depends(get_db)):
    """Get summary of high priority prospects"""
    high_priority_prospects = db.query(Prospect).filter(
        Prospect.priority_level == "High"
    ).all()
    
    summary = {
        "total_count": len(high_priority_prospects),
        "by_island": {},
        "by_service": {},
        "total_potential_value": 0
    }
    
    for prospect in high_priority_prospects:
        # Count by island
        island = prospect.company.island.value
        summary["by_island"][island] = summary["by_island"].get(island, 0) + 1
        
        # Count by recommended service
        for service in (prospect.recommended_services or []):
            summary["by_service"][service] = summary["by_service"].get(service, 0) + 1
            
        # Sum potential value
        summary["total_potential_value"] += prospect.estimated_deal_value or 0
        
    return summary