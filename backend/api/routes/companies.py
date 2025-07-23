from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from models.database import get_db
from models.models import Company
from api.schemas import CompanyResponse, CompanyCreate, CompanyUpdate, IslandEnum, IndustryEnum

router = APIRouter()


@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    island: Optional[IslandEnum] = None,
    industry: Optional[IndustryEnum] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get filtered list of companies"""
    query = db.query(Company)
    
    if island:
        query = query.filter(Company.island == island)
    if industry:
        query = query.filter(Company.industry == industry)
        
    companies = query.offset(offset).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get a specific company by ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company"""
    # Check if company already exists
    existing = db.query(Company).filter(
        Company.name == company.name,
        Company.island == company.island
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")
        
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db)
):
    """Update a company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
        
    for field, value in company_update.dict(exclude_unset=True).items():
        setattr(company, field, value)
        
    db.commit()
    db.refresh(company)
    return company


@router.delete("/{company_id}")
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete a company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
        
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}