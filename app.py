"""
Single-file FastAPI app for Render deployment
This avoids all import path issues
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup - Railway provides DATABASE_URL
# Log all database-related env vars for debugging
logger.info("=== Environment Variables ===")
for key in os.environ:
    if 'DATABASE' in key or 'POSTGRES' in key or 'DB' in key:
        # Don't log the full URL for security, just the key
        logger.info(f"{key}: {'[SET]' if os.getenv(key) else '[NOT SET]'}")

DATABASE_URL = os.getenv("DATABASE_URL")

# Railway's postgres URLs need to be updated to postgresql
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Also check for Railway's specific database URL format
if not DATABASE_URL:
    # Try Railway's PostgreSQL URL pattern
    DATABASE_URL = os.getenv("DATABASE_PRIVATE_URL") or os.getenv("DATABASE_PUBLIC_URL")
    
if DATABASE_URL:
    logger.info(f"Connecting to database (URL found)")
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        # Fall back to SQLite
        logger.warning("Falling back to SQLite")
        engine = create_engine("sqlite:///./test.db")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    logger.warning("No DATABASE_URL found, using SQLite")
    engine = create_engine("sqlite:///./test.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Hawaii Business Intelligence System API")
    logger.info(f"Running on port: {os.getenv('PORT', 'not set')}")
    
    # Create tables if they don't exist
    try:
        with engine.connect() as conn:
            # Create basic tables
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    website VARCHAR(255),
                    island VARCHAR(50),
                    industry VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS prospects (
                    id SERIAL PRIMARY KEY,
                    company_id INTEGER REFERENCES companies(id),
                    score INTEGER,
                    ai_analysis TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            conn.commit()
            logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down API")

# Create FastAPI app
app = FastAPI(
    title="Hawaii Business Intelligence System",
    description="AI-powered business prospecting for Hawaii",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins + ["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic routes
@app.get("/")
async def root():
    return {
        "message": "Hawaii Business Intelligence System API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "environment": "production" if DATABASE_URL else "development"
    }

@app.get("/api/analytics/dashboard")
async def dashboard(db: Session = Depends(get_db)):
    """Get dashboard data"""
    try:
        # Get counts from database
        companies_count = db.execute(text("SELECT COUNT(*) FROM companies")).scalar() or 0
        prospects_count = db.execute(text("SELECT COUNT(*) FROM prospects")).scalar() or 0
        
        return {
            "total_companies": companies_count,
            "total_prospects": prospects_count,
            "active_workflows": 0,
            "recent_interactions": 0,
            "high_score_prospects": prospects_count,
            "average_score": 75
        }
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return {
            "total_companies": 0,
            "total_prospects": 0,
            "active_workflows": 0,
            "recent_interactions": 0,
            "high_score_prospects": 0,
            "average_score": 0
        }

@app.get("/api/companies")
async def get_companies(db: Session = Depends(get_db)):
    """Get all companies"""
    try:
        result = db.execute(text("SELECT * FROM companies LIMIT 100"))
        companies = []
        for row in result:
            companies.append({
                "id": row[0],
                "name": row[1],
                "website": row[2],
                "island": row[3],
                "industry": row[4]
            })
        return companies
    except Exception as e:
        logger.error(f"Error fetching companies: {e}")
        return []

@app.get("/api/prospects")
async def get_prospects(db: Session = Depends(get_db)):
    """Get all prospects"""
    try:
        result = db.execute(text("""
            SELECT p.*, c.name as company_name 
            FROM prospects p 
            LEFT JOIN companies c ON p.company_id = c.id 
            LIMIT 100
        """))
        prospects = []
        for row in result:
            prospects.append({
                "id": row[0],
                "company_id": row[1],
                "score": row[2],
                "ai_analysis": row[3],
                "company_name": row[5] if len(row) > 5 else None
            })
        return prospects
    except Exception as e:
        logger.error(f"Error fetching prospects: {e}")
        return []

@app.post("/api/test/seed")
async def seed_data(db: Session = Depends(get_db)):
    """Seed demo data"""
    try:
        # Add demo companies
        demo_companies = [
            ("Aloha Medical Center", "https://alohamedical.com", "Oahu", "Healthcare"),
            ("Pacific Paradise Resort", "https://pacificparadise.com", "Maui", "Tourism"),
            ("Kona Coffee Collective", "https://konacoffee.com", "Big Island", "Food Service"),
            ("Island Tech Solutions", "https://islandtech.com", "Oahu", "Technology"),
            ("Kauai Adventure Tours", "https://kauaiadventure.com", "Kauai", "Tourism")
        ]
        
        for name, website, island, industry in demo_companies:
            db.execute(text("""
                INSERT INTO companies (name, website, island, industry) 
                VALUES (:name, :website, :island, :industry)
                ON CONFLICT DO NOTHING
            """), {"name": name, "website": website, "island": island, "industry": industry})
        
        db.commit()
        
        # Add prospects for each company
        companies = db.execute(text("SELECT id FROM companies")).fetchall()
        for company in companies:
            db.execute(text("""
                INSERT INTO prospects (company_id, score, ai_analysis)
                VALUES (:company_id, :score, :ai_analysis)
                ON CONFLICT DO NOTHING
            """), {
                "company_id": company[0],
                "score": 85,
                "ai_analysis": "High potential for AI integration. Strong digital presence."
            })
        
        db.commit()
        
        return {"message": "Demo data seeded successfully"}
    except Exception as e:
        logger.error(f"Seed error: {e}")
        db.rollback()
        return {"error": str(e)}

# Placeholder routes for compatibility
@app.get("/api/analytics/by-island")
async def analytics_by_island():
    return {"Oahu": 5, "Maui": 3, "Big Island": 2, "Kauai": 2}

@app.get("/api/analytics/by-industry")
async def analytics_by_industry():
    return {"Tourism": 4, "Healthcare": 3, "Technology": 3, "Food Service": 2}

@app.get("/api/workflows/status")
async def workflow_status():
    return {"active": 0, "completed": 0, "failed": 0}

@app.get("/api/interactions")
async def get_interactions():
    return []

# Run the app if called directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))