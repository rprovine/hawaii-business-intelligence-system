from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any, List
from datetime import datetime, timedelta

from models.database import get_db

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard analytics using raw SQL to avoid enum issues"""
    
    # Basic stats
    stats_query = text("""
        SELECT 
            COUNT(*) as total_prospects,
            COUNT(*) FILTER (WHERE priority_level = 'High') as high_priority_count,
            COALESCE(SUM(estimated_deal_value), 0) as total_pipeline_value,
            COALESCE(AVG(score), 0) as average_score
        FROM prospects
    """)
    stats_result = db.execute(stats_query).fetchone()
    
    # By island
    island_query = text("""
        SELECT 
            c.island,
            COUNT(p.id) as prospect_count,
            COALESCE(AVG(p.score), 0) as average_score,
            COUNT(p.id) FILTER (WHERE p.priority_level = 'High') as high_priority_count,
            COALESCE(SUM(p.estimated_deal_value), 0) as total_pipeline_value
        FROM companies c
        JOIN prospects p ON c.id = p.company_id
        GROUP BY c.island
        ORDER BY prospect_count DESC
    """)
    island_results = db.execute(island_query).fetchall()
    
    # By industry
    industry_query = text("""
        SELECT 
            c.industry,
            COUNT(p.id) as prospect_count,
            COALESCE(AVG(p.score), 0) as average_score
        FROM companies c
        JOIN prospects p ON c.id = p.company_id
        GROUP BY c.industry
        ORDER BY prospect_count DESC
        LIMIT 10
    """)
    industry_results = db.execute(industry_query).fetchall()
    
    # Recent high scores
    recent_query = text("""
        SELECT 
            p.id,
            p.score,
            p.priority_level,
            p.estimated_deal_value,
            p.recommended_services,
            c.name as company_name,
            c.island,
            c.industry
        FROM prospects p
        JOIN companies c ON p.company_id = c.id
        WHERE p.score >= 80
        ORDER BY p.created_at DESC
        LIMIT 10
    """)
    recent_results = db.execute(recent_query).fetchall()
    
    return {
        "total_prospects": stats_result[0],
        "high_priority_count": stats_result[1],
        "total_pipeline_value": float(stats_result[2]),
        "average_score": float(stats_result[3]),
        "conversion_rate": 0,  # Placeholder
        "by_island": [
            {
                "island": row[0],
                "prospect_count": row[1],
                "average_score": float(row[2]),
                "high_priority_count": row[3],
                "total_pipeline_value": float(row[4])
            }
            for row in island_results
        ],
        "by_industry": [
            {
                "industry": row[0],
                "prospect_count": row[1],
                "average_score": float(row[2]),
                "top_services": []
            }
            for row in industry_results
        ],
        "recent_high_scores": [
            {
                "id": row[0],
                "score": row[1],
                "priority_level": row[2],
                "estimated_deal_value": float(row[3]) if row[3] else 0,
                "recommended_services": list(row[4]) if row[4] and isinstance(row[4], (list, tuple)) else [s.strip('" ') for s in row[4].strip('{}').split(',')] if row[4] and isinstance(row[4], str) else [],
                "company": {
                    "name": row[5],
                    "island": row[6],
                    "industry": row[7]
                }
            }
            for row in recent_results
        ]
    }


@router.get("/by-island")
async def get_analytics_by_island(db: Session = Depends(get_db)):
    """Get analytics grouped by island"""
    
    query = text("""
        SELECT 
            c.island,
            COUNT(p.id) as prospect_count,
            COALESCE(AVG(p.score), 0) as average_score,
            COUNT(p.id) FILTER (WHERE p.priority_level = 'High') as high_priority_count,
            COALESCE(SUM(p.estimated_deal_value), 0) as total_pipeline_value
        FROM companies c
        JOIN prospects p ON c.id = p.company_id
        GROUP BY c.island
        ORDER BY total_pipeline_value DESC
    """)
    
    results = db.execute(query).fetchall()
    
    return [
        {
            "island": row[0],
            "prospect_count": row[1],
            "average_score": float(row[2]),
            "high_priority_count": row[3],
            "total_pipeline_value": float(row[4])
        }
        for row in results
    ]


@router.get("/by-industry")
async def get_analytics_by_industry(db: Session = Depends(get_db)):
    """Get analytics grouped by industry"""
    
    query = text("""
        SELECT 
            c.industry,
            COUNT(p.id) as prospect_count,
            COALESCE(AVG(p.score), 0) as average_score,
            COALESCE(SUM(p.estimated_deal_value), 0) as total_pipeline_value
        FROM companies c
        JOIN prospects p ON c.id = p.company_id
        GROUP BY c.industry
        ORDER BY prospect_count DESC
        LIMIT 15
    """)
    
    results = db.execute(query).fetchall()
    
    return [
        {
            "industry": row[0],
            "prospect_count": row[1],
            "average_score": float(row[2]),
            "total_pipeline_value": float(row[3])
        }
        for row in results
    ]


@router.get("/timeline")
async def get_analytics_timeline(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get timeline analytics for the specified number of days"""
    
    # Calculate start date
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get daily stats
    query = text("""
        WITH date_series AS (
            SELECT generate_series(
                CAST(:start_date AS date),
                CAST(:end_date AS date),
                '1 day'::interval
            )::date AS date
        ),
        daily_stats AS (
            SELECT 
                DATE(p.created_at) as date,
                COUNT(*) as new_prospects,
                COALESCE(SUM(p.estimated_deal_value), 0) as pipeline_value
            FROM prospects p
            WHERE p.created_at >= :start_date
            GROUP BY DATE(p.created_at)
        )
        SELECT 
            ds.date,
            COALESCE(d.new_prospects, 0) as new_prospects,
            COALESCE(d.pipeline_value, 0) as pipeline_value
        FROM date_series ds
        LEFT JOIN daily_stats d ON ds.date = d.date
        ORDER BY ds.date
    """)
    
    results = db.execute(query, {
        "start_date": start_date,
        "end_date": end_date
    }).fetchall()
    
    return [
        {
            "date": row[0].isoformat(),
            "new_prospects": row[1],
            "pipeline_value": float(row[2])
        }
        for row in results
    ]