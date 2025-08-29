#!/bin/bash

# Hawaii Business Intelligence System - Startup Script
echo "🌺 Starting Hawaii Business Intelligence System..."

# Set default environment variables if not provided
export PYTHONPATH=/app:${PYTHONPATH}
export PYTHONUNBUFFERED=1

# Wait for database if DATABASE_URL is set
if [ ! -z "$DATABASE_URL" ]; then
    echo "⏳ Waiting for database connection..."
    python -c "
import time
import psycopg2
from urllib.parse import urlparse
import os

db_url = os.getenv('DATABASE_URL')
if db_url:
    # Handle Render's postgres:// URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    result = urlparse(db_url)
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                database=result.path[1:],
                user=result.username,
                password=result.password,
                host=result.hostname,
                port=result.port
            )
            conn.close()
            print('✅ Database is ready!')
            break
        except Exception as e:
            retry_count += 1
            print(f'Waiting for database... ({retry_count}/{max_retries})')
            time.sleep(2)
    else:
        print('❌ Could not connect to database after 30 attempts')
        exit(1)
    "
    
    # Initialize database tables
    echo "🔨 Creating database tables..."
    python -c "
from models.database import engine, Base
from models.models import Company, Prospect, DecisionMaker, DataCollectionLog
Base.metadata.create_all(bind=engine)
print('✅ Database tables created/verified')
    "
    
    # Check if database is empty and seed if needed
    echo "🌱 Checking for initial data..."
    python -c "
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Company

# Fix DATABASE_URL for SQLAlchemy
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
    os.environ['DATABASE_URL'] = db_url

engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

company_count = db.query(Company).count()
db.close()

if company_count == 0:
    print('📦 Database is empty. Seeding with demo data...')
    import seed_demo_data
    seed_demo_data.seed_demo_data()
else:
    print(f'✅ Database already has {company_count} companies')
    "
else
    echo "⚠️  No DATABASE_URL set - running without database"
fi

# Start the FastAPI application
echo "🚀 Starting FastAPI server on port ${PORT:-8000}..."
exec uvicorn main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --log-level ${LOG_LEVEL:-info}