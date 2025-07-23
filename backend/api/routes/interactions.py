from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.database import get_db
from models.models import Interaction, Prospect
from api.schemas import InteractionResponse, InteractionCreate

router = APIRouter()


@router.get("/", response_model=List[InteractionResponse])
async def get_interactions(
    prospect_id: Optional[int] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get interactions, optionally filtered by prospect"""
    query = db.query(Interaction)
    
    if prospect_id:
        query = query.filter(Interaction.prospect_id == prospect_id)
        
    interactions = query.order_by(Interaction.interaction_date.desc()).offset(offset).limit(limit).all()
    return interactions


@router.get("/{interaction_id}", response_model=InteractionResponse)
async def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific interaction by ID"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.post("/", response_model=InteractionResponse)
async def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """Create a new interaction"""
    # Verify prospect exists
    prospect = db.query(Prospect).filter(Prospect.id == interaction.prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
        
    db_interaction = Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


@router.put("/{interaction_id}", response_model=InteractionResponse)
async def update_interaction(
    interaction_id: int,
    interaction_update: InteractionCreate,
    db: Session = Depends(get_db)
):
    """Update an interaction"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
        
    for field, value in interaction_update.dict(exclude_unset=True).items():
        setattr(interaction, field, value)
        
    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/{interaction_id}")
async def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete an interaction"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
        
    db.delete(interaction)
    db.commit()
    return {"message": "Interaction deleted successfully"}


@router.get("/upcoming/tasks")
async def get_upcoming_tasks(db: Session = Depends(get_db)):
    """Get interactions with upcoming next actions"""
    upcoming = db.query(Interaction).filter(
        Interaction.next_action_date >= datetime.now().date(),
        Interaction.next_action.isnot(None)
    ).order_by(Interaction.next_action_date).all()
    
    return [
        {
            "interaction_id": i.id,
            "prospect_id": i.prospect_id,
            "next_action": i.next_action,
            "next_action_date": i.next_action_date,
            "prospect_name": i.prospect.company.name if i.prospect and i.prospect.company else "Unknown"
        }
        for i in upcoming
    ]