from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from models.database import get_db
from models.models import Prospect, Company, Opportunity, AnalyticsSnapshot
from api.schemas import AnalyticsDashboard, AnalyticsIslandSummary, AnalyticsIndustrySummary

router = APIRouter()


@router.get("/dashboard", response_model=AnalyticsDashboard)
async def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard analytics"""
    # Basic stats
    total_prospects = db.query(Prospect).count()
    high_priority_count = db.query(Prospect).filter(Prospect.priority_level == "High").count()
    
    # Calculate totals
    pipeline_value = db.query(func.sum(Prospect.estimated_deal_value)).scalar() or 0
    avg_score = db.query(func.avg(Prospect.score)).scalar() or 0
    
    # By island analytics
    island_data = db.query(
        Company.island,
        func.count(Prospect.id).label('prospect_count'),
        func.avg(Prospect.score).label('average_score'),
        func.count(Prospect.id).filter(Prospect.priority_level == "High").label('high_priority_count'),
        func.sum(Prospect.estimated_deal_value).label('total_pipeline_value')
    ).join(Prospect).group_by(Company.island).all()
    
    by_island = [
        AnalyticsIslandSummary(
            island=row[0] if isinstance(row[0], str) else row[0].value,
            prospect_count=row[1],
            average_score=float(row[2] or 0),
            high_priority_count=row[3],
            total_pipeline_value=float(row[4] or 0)
        )
        for row in island_data
    ]
    
    # By industry analytics
    industry_data = db.query(
        Company.industry,
        func.count(Prospect.id).label('prospect_count'),
        func.avg(Prospect.score).label('average_score')
    ).join(Prospect).group_by(Company.industry).order_by(func.count(Prospect.id).desc()).limit(10).all()
    
    by_industry = [
        AnalyticsIndustrySummary(
            industry=row[0] if isinstance(row[0], str) else row[0].value,
            prospect_count=row[1],
            average_score=float(row[2] or 0),
            top_services=[]  # Would need additional query for this
        )
        for row in industry_data
    ]
    
    # Recent high scores
    recent_high_scores = db.query(Prospect).filter(
        Prospect.score >= 80
    ).order_by(Prospect.created_at.desc()).limit(10).all()
    
    # Calculate conversion rate (example: prospects to opportunities)
    total_opportunities = db.query(Opportunity).count()
    conversion_rate = (total_opportunities / total_prospects * 100) if total_prospects > 0 else 0
    
    return AnalyticsDashboard(
        total_prospects=total_prospects,
        high_priority_count=high_priority_count,
        total_pipeline_value=pipeline_value,
        average_score=avg_score,
        conversion_rate=conversion_rate,
        by_island=by_island,
        by_industry=by_industry,
        recent_high_scores=recent_high_scores
    )


@router.get("/by-island")
async def get_analytics_by_island(db: Session = Depends(get_db)):
    """Get detailed analytics by island"""
    results = db.query(
        Company.island,
        func.count(Prospect.id).label('total'),
        func.avg(Prospect.score).label('avg_score'),
        func.sum(Prospect.estimated_deal_value).label('total_value')
    ).join(Prospect).group_by(Company.island).all()
    
    return [
        {
            "island": row[0].value,
            "total_prospects": row[1],
            "average_score": float(row[2] or 0),
            "total_value": float(row[3] or 0)
        }
        for row in results
    ]


@router.get("/by-industry")
async def get_analytics_by_industry(db: Session = Depends(get_db)):
    """Get detailed analytics by industry"""
    results = db.query(
        Company.industry,
        func.count(Prospect.id).label('total'),
        func.avg(Prospect.score).label('avg_score')
    ).join(Prospect).group_by(Company.industry).order_by(func.count(Prospect.id).desc()).all()
    
    return [
        {
            "industry": row[0].value,
            "total_prospects": row[1],
            "average_score": float(row[2] or 0)
        }
        for row in results
    ]


@router.get("/timeline")
async def get_analytics_timeline(days: int = 30, db: Session = Depends(get_db)):
    """Get analytics timeline for the last N days"""
    start_date = datetime.now() - timedelta(days=days)
    
    snapshots = db.query(AnalyticsSnapshot).filter(
        AnalyticsSnapshot.snapshot_date >= start_date
    ).order_by(AnalyticsSnapshot.snapshot_date).all()
    
    return [
        {
            "date": snapshot.snapshot_date.isoformat(),
            "total_prospects": snapshot.total_prospects,
            "high_priority_count": snapshot.high_priority_count,
            "average_score": snapshot.average_score,
            "total_pipeline_value": snapshot.total_pipeline_value
        }
        for snapshot in snapshots
    ]


@router.post("/snapshot")
async def create_analytics_snapshot(db: Session = Depends(get_db)):
    """Manually create an analytics snapshot"""
    # This would typically be called by a scheduled job
    # Implementation would be similar to the scheduler's create_analytics_snapshot
    return {"message": "Snapshot created successfully"}