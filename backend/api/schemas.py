from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum


class IslandEnum(str, Enum):
    OAHU = "Oahu"
    MAUI = "Maui"
    BIG_ISLAND = "Big Island"
    KAUAI = "Kauai"
    MOLOKAI = "Molokai"
    LANAI = "Lanai"
    ALL_ISLANDS = "All Islands"


class IndustryEnum(str, Enum):
    TOURISM = "Tourism"
    HOSPITALITY = "Hospitality"
    AGRICULTURE = "Agriculture"
    RETAIL = "Retail"
    HEALTHCARE = "Healthcare"
    REAL_ESTATE = "Real Estate"
    TECHNOLOGY = "Technology"
    CONSTRUCTION = "Construction"
    FOOD_SERVICE = "Food Service"
    TRANSPORTATION = "Transportation"
    PROFESSIONAL_SERVICES = "Professional Services"
    OTHER = "Other"


class ServiceEnum(str, Enum):
    DATA_ANALYTICS = "Data Analytics"
    CUSTOM_CHATBOTS = "Custom Chatbots"
    FRACTIONAL_CTO = "Fractional CTO"
    HUBSPOT_DIGITAL_MARKETING = "HubSpot Digital Marketing"


# Company Schemas
class CompanyBase(BaseModel):
    name: str
    address: Optional[str] = None
    island: IslandEnum
    industry: IndustryEnum
    website: Optional[str] = None
    phone: Optional[str] = None
    employee_count_estimate: Optional[int] = None
    annual_revenue_estimate: Optional[float] = None
    description: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    island: Optional[IslandEnum] = None
    industry: Optional[IndustryEnum] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    employee_count_estimate: Optional[int] = None
    annual_revenue_estimate: Optional[float] = None
    description: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Prospect Schemas
class ProspectBase(BaseModel):
    company_id: int
    score: int = Field(ge=0, le=100)
    ai_analysis: Optional[str] = None
    pain_points: Optional[List[str]] = []
    recommended_services: Optional[List[ServiceEnum]] = []
    estimated_deal_value: Optional[float] = None
    growth_signals: Optional[List[str]] = []
    technology_readiness: Optional[str] = None
    priority_level: Optional[str] = Field(None, pattern="^(High|Medium|Low)$")


class ProspectCreate(ProspectBase):
    pass


class ProspectUpdate(BaseModel):
    score: Optional[int] = Field(None, ge=0, le=100)
    ai_analysis: Optional[str] = None
    pain_points: Optional[List[str]] = None
    recommended_services: Optional[List[ServiceEnum]] = None
    estimated_deal_value: Optional[float] = None
    growth_signals: Optional[List[str]] = None
    technology_readiness: Optional[str] = None
    priority_level: Optional[str] = Field(None, pattern="^(High|Medium|Low)$")


class ProspectResponse(ProspectBase):
    id: int
    company: CompanyResponse
    last_analyzed: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Decision Maker Schemas
class DecisionMakerBase(BaseModel):
    company_id: int
    name: str
    title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_primary: bool = False


class DecisionMakerCreate(DecisionMakerBase):
    pass


class DecisionMakerResponse(DecisionMakerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Interaction Schemas
class InteractionBase(BaseModel):
    prospect_id: int
    interaction_type: str
    notes: Optional[str] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[date] = None
    created_by: Optional[str] = None


class InteractionCreate(InteractionBase):
    pass


class InteractionResponse(InteractionBase):
    id: int
    interaction_date: datetime

    class Config:
        from_attributes = True


# Analytics Schemas
class AnalyticsIslandSummary(BaseModel):
    island: str
    prospect_count: int
    average_score: float
    high_priority_count: int
    total_pipeline_value: float


class AnalyticsIndustrySummary(BaseModel):
    industry: str
    prospect_count: int
    average_score: float
    top_services: List[str]


class AnalyticsDashboard(BaseModel):
    total_prospects: int
    high_priority_count: int
    total_pipeline_value: float
    average_score: float
    conversion_rate: float
    by_island: List[AnalyticsIslandSummary]
    by_industry: List[AnalyticsIndustrySummary]
    recent_high_scores: List[ProspectResponse]


# Workflow Schemas
class WorkflowTrigger(BaseModel):
    action: str = Field(..., pattern="^(scrape|analyze|alert)$")
    source: Optional[str] = None
    island_filter: Optional[IslandEnum] = None
    industry_filter: Optional[IndustryEnum] = None