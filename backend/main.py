from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

from api.routes import simple_prospects, simple_prospects_fixed, companies, simple_analytics, interactions, workflows, test_data
from models.database import engine, Base

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Hawaii Business Intelligence System API")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Shutting down API")


app = FastAPI(
    title="Hawaii Business Intelligence System",
    description="AI-powered business prospecting for LeniLani Consulting",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(simple_prospects.router, prefix="/api/prospects", tags=["prospects"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(simple_analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(interactions.router, prefix="/api/interactions", tags=["interactions"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(test_data.router, prefix="/api/test", tags=["test"])


@app.get("/")
async def root():
    return {
        "message": "Hawaii Business Intelligence System API",
        "version": "1.0.0",
        "company": "LeniLani Consulting"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )