from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import logging

from models.database import get_db
from models.models import DataCollectionLog
from api.schemas import WorkflowTrigger

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/trigger")
async def trigger_workflow(
    workflow: WorkflowTrigger,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger a workflow action"""
    if workflow.action == "scrape":
        # In production, this would trigger the actual scraping
        background_tasks.add_task(run_scraping, workflow.source or "all")
        return {"message": f"Scraping workflow triggered for {workflow.source or 'all sources'}"}
        
    elif workflow.action == "analyze":
        # In production, this would trigger analysis of unanalyzed prospects
        background_tasks.add_task(run_analysis)
        return {"message": "Analysis workflow triggered"}
        
    elif workflow.action == "alert":
        # In production, this would send pending alerts
        background_tasks.add_task(send_alerts)
        return {"message": "Alert workflow triggered"}
        
    else:
        raise HTTPException(status_code=400, detail="Invalid workflow action")


@router.get("/status")
async def get_workflow_status(db: Session = Depends(get_db)):
    """Get current workflow status"""
    # Get latest collection logs
    latest_logs = db.query(DataCollectionLog).order_by(
        DataCollectionLog.run_date.desc()
    ).limit(5).all()
    
    # Check if any collections are currently running (mock for now)
    running_workflows = []
    
    return {
        "running_workflows": running_workflows,
        "recent_runs": [
            {
                "id": log.id,
                "source": log.source,
                "run_date": log.run_date,
                "status": log.status,
                "records_found": log.records_found,
                "records_added": log.records_added,
                "duration_seconds": log.duration_seconds
            }
            for log in latest_logs
        ]
    }


@router.get("/logs")
async def get_data_collection_logs(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get data collection logs"""
    logs = db.query(DataCollectionLog).order_by(
        DataCollectionLog.run_date.desc()
    ).offset(offset).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "source": log.source,
            "run_date": log.run_date,
            "records_found": log.records_found,
            "records_processed": log.records_processed,
            "records_added": log.records_added,
            "errors": log.errors,
            "error_details": log.error_details,
            "duration_seconds": log.duration_seconds,
            "status": log.status
        }
        for log in logs
    ]


@router.get("/schedule")
async def get_workflow_schedule():
    """Get the current workflow schedule"""
    return {
        "schedules": [
            {
                "name": "Daily Collection",
                "frequency": "Daily at 6:00 AM and 6:00 PM HST",
                "description": "Full data collection from all sources"
            },
            {
                "name": "Hourly Quick Scan",
                "frequency": "Every hour",
                "description": "Quick scan of high-priority sources"
            },
            {
                "name": "Weekly Analytics",
                "frequency": "Every Monday at 9:00 AM HST",
                "description": "Generate weekly analytics snapshot"
            }
        ]
    }


# Background task functions
async def run_scraping(source: str):
    """Run data collection in background"""
    import subprocess
    import os
    
    # Get the path to data collectors
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    collectors_dir = os.path.join(backend_dir, 'data-collectors')
    
    # Map source names to collect_data.py arguments
    source_map = {
        'all': 'real',
        'yelp': 'yelp',
        'google': 'google',
        'linkedin': 'linkedin',
        'news': 'news'
    }
    
    cmd_arg = source_map.get(source, 'test')
    
    # Run data collection as subprocess
    try:
        subprocess.Popen(
            ['python', 'collect_data.py', cmd_arg],
            cwd=collectors_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info(f"Started data collection for {source}")
    except Exception as e:
        logger.error(f"Failed to start data collection: {e}")


async def run_analysis():
    """Run prospect analysis in background"""
    # This would re-analyze all prospects with score 0
    from models.database import SessionLocal
    from models.models import Prospect
    
    db = SessionLocal()
    try:
        # Get prospects that need analysis
        prospects = db.query(Prospect).filter(Prospect.score == 0).all()
        logger.info(f"Found {len(prospects)} prospects needing analysis")
        # In production, this would trigger the AI analysis
    finally:
        db.close()


async def send_alerts():
    """Send alerts for high-priority prospects"""
    from models.database import SessionLocal
    from models.models import Prospect
    
    db = SessionLocal()
    try:
        # Get high priority prospects from last 24 hours
        high_priority = db.query(Prospect).filter(
            Prospect.priority_level == 'High',
            Prospect.score >= 80
        ).all()
        logger.info(f"Found {len(high_priority)} high-priority prospects for alerts")
        # In production, this would send email alerts
    finally:
        db.close()