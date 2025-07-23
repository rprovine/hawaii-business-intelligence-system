# Hawaii Business Intelligence System - Deployment Guide

This guide covers deployment options for the Hawaii Business Intelligence System, from local development to production deployment.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Database Setup](#database-setup)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **CPU**: 2+ cores (4+ recommended for production)
- **RAM**: 4GB minimum (8GB+ recommended)
- **Storage**: 10GB available space (50GB+ for production)
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2

### Required Software
- **Docker**: 20.10+ with Docker Compose v2
- **Node.js**: 18+ (for local development)
- **Python**: 3.9+ (for local development)
- **PostgreSQL**: 14+ (if not using Docker)

### API Keys Required
- **Anthropic Claude API**: For AI business analysis
- **Google Places API**: For business discovery and verification

## Environment Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/hawaii_business_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hawaii_business_db
DB_USER=postgres
DB_PASSWORD=your_secure_password

# =============================================================================
# API KEYS (REQUIRED)
# =============================================================================
# Anthropic Claude API Key for AI analysis
CLAUDE_API_KEY=sk-ant-api03-your-claude-api-key
ANTHROPIC_API_KEY=sk-ant-api03-your-claude-api-key

# Google Places API Key for business discovery
GOOGLE_PLACES_API_KEY=your-google-places-api-key

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
# Environment: development, staging, production
ENVIRONMENT=development

# Debug mode (set to False in production)
DEBUG=True

# Secret key for session management (generate a secure key for production)
SECRET_KEY=your-super-secret-key-change-this-in-production

# Allowed CORS origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3002,http://127.0.0.1:3000

# =============================================================================
# API CONFIGURATION
# =============================================================================
# Backend API settings
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# Frontend settings
FRONTEND_PORT=3000
REACT_APP_API_URL=http://localhost:8000

# =============================================================================
# EXTERNAL SERVICES (OPTIONAL)
# =============================================================================
# Redis for caching (optional)
REDIS_URL=redis://localhost:6379/0

# Sentry for error tracking (production)
SENTRY_DSN=your-sentry-dsn

# Logging level
LOG_LEVEL=INFO

# =============================================================================
# SECURITY SETTINGS (PRODUCTION)
# =============================================================================
# SSL/TLS settings for production
SSL_CERT_PATH=/path/to/certificate.crt
SSL_KEY_PATH=/path/to/private.key

# Rate limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# =============================================================================
# HAWAII BUSINESS INTELLIGENCE SPECIFIC
# =============================================================================
# Data collection settings
MAX_BUSINESSES_PER_SCRAPE=50
SCRAPING_DELAY_SECONDS=2
WEB_SCRAPING_TIMEOUT=15

# AI Analysis settings
CLAUDE_MODEL=claude-3-haiku-20240307
CLAUDE_MAX_TOKENS=2000
CLAUDE_TEMPERATURE=0.7

# Business analysis thresholds
MIN_PROSPECT_SCORE=50
HIGH_PRIORITY_THRESHOLD=80
```

### Production Environment Variables

For production, create `.env.production`:

```env
# =============================================================================
# PRODUCTION CONFIGURATION
# =============================================================================
ENVIRONMENT=production
DEBUG=False

# Database (use managed PostgreSQL service in production)
DATABASE_URL=postgresql://username:password@your-db-host:5432/hawaii_business_db

# API Keys (production keys)
CLAUDE_API_KEY=sk-ant-api03-production-claude-key
GOOGLE_PLACES_API_KEY=production-google-places-key

# Security
SECRET_KEY=your-extremely-secure-production-secret-key
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Performance
API_WORKERS=4
GUNICORN_TIMEOUT=120

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
LOG_LEVEL=WARNING

# SSL
SSL_CERT_PATH=/etc/ssl/certs/yourdomain.crt
SSL_KEY_PATH=/etc/ssl/private/yourdomain.key

# Rate limiting (stricter in production)
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW=60
```

## Local Development

### Quick Start with Docker

1. **Clone and Setup**
   ```bash
   git clone https://github.com/yourusername/hawaii-business-intelligence-system.git
   cd hawaii-business-intelligence-system
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Verify Services**
   ```bash
   # Check all services are running
   docker-compose ps
   
   # Check logs
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

4. **Initialize Database**
   ```bash
   # Run database migrations
   docker-compose exec backend alembic upgrade head
   
   # Load initial data (optional)
   docker-compose exec backend python comprehensive_scraper.py
   ```

5. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Development Setup

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Setup database
   createdb hawaii_business_db
   alembic upgrade head
   
   # Start backend
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

## Docker Deployment

### Development with Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  database:
    image: postgres:14
    environment:
      POSTGRES_DB: hawaii_business_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql
    ports:
      - "5432:5432"

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://postgres:password@database:5432/hawaii_business_db
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - GOOGLE_PLACES_API_KEY=${GOOGLE_PLACES_API_KEY}
    depends_on:
      - database
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  database:
    image: postgres:14
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - GOOGLE_PLACES_API_KEY=${GOOGLE_PLACES_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - ENVIRONMENT=production
    depends_on:
      - database
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    environment:
      - REACT_APP_API_URL=https://yourdomain.com/api
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
```

## Production Deployment

### Option 1: VPS/Dedicated Server

1. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Application Deployment**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/hawaii-business-intelligence-system.git
   cd hawaii-business-intelligence-system
   
   # Setup environment
   cp .env.example .env.production
   # Edit .env.production with production values
   
   # Deploy
   docker-compose -f docker-compose.prod.yml up -d
   
   # Initialize database
   docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
   ```

3. **SSL Certificate Setup**
   ```bash
   # Using Let's Encrypt with Certbot
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

### Option 2: Cloud Deployment (AWS)

1. **Infrastructure Setup**
   ```bash
   # Using AWS CLI and CloudFormation
   aws cloudformation create-stack \
     --stack-name hawaii-business-intelligence \
     --template-body file://aws/cloudformation.yaml \
     --parameters ParameterKey=KeyName,ParameterValue=your-key-pair
   ```

2. **RDS Database Setup**
   ```bash
   # Create RDS PostgreSQL instance
   aws rds create-db-instance \
     --db-instance-identifier hawaii-business-db \
     --db-instance-class db.t3.micro \
     --engine postgres \
     --master-username postgres \
     --master-user-password YourSecurePassword \
     --allocated-storage 20
   ```

3. **ECS Service Deployment**
   ```bash
   # Build and push Docker images
   docker build -t hawaii-backend ./backend
   docker tag hawaii-backend:latest your-account.dkr.ecr.region.amazonaws.com/hawaii-backend:latest
   docker push your-account.dkr.ecr.region.amazonaws.com/hawaii-backend:latest
   
   # Deploy ECS service
   aws ecs create-service \
     --cluster hawaii-cluster \
     --service-name hawaii-backend \
     --task-definition hawaii-backend:1 \
     --desired-count 2
   ```

### Option 3: Kubernetes Deployment

1. **Create Kubernetes Manifests**
   ```yaml
   # k8s/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: hawaii-backend
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: hawaii-backend
     template:
       metadata:
         labels:
           app: hawaii-backend
       spec:
         containers:
         - name: backend
           image: hawaii-backend:latest
           ports:
           - containerPort: 8000
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: hawaii-secrets
                 key: database-url
           - name: CLAUDE_API_KEY
             valueFrom:
               secretKeyRef:
                 name: hawaii-secrets
                 key: claude-api-key
   ```

2. **Deploy to Kubernetes**
   ```bash
   # Apply manifests
   kubectl apply -f k8s/
   
   # Check deployment
   kubectl get pods -l app=hawaii-backend
   kubectl logs -f deployment/hawaii-backend
   ```

## Database Setup

### PostgreSQL Configuration

1. **Production Database Setup**
   ```sql
   -- Create database and user
   CREATE DATABASE hawaii_business_db;
   CREATE USER hawaii_user WITH ENCRYPTED PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE hawaii_business_db TO hawaii_user;
   
   -- Optimize for performance
   ALTER DATABASE hawaii_business_db SET shared_preload_libraries = 'pg_stat_statements';
   ALTER DATABASE hawaii_business_db SET track_activity_query_size = 2048;
   ```

2. **Database Migrations**
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Create new migration
   alembic revision --autogenerate -m "Add new feature"
   
   # Rollback migration
   alembic downgrade -1
   ```

3. **Database Backup**
   ```bash
   # Create backup
   pg_dump -h localhost -U postgres hawaii_business_db > backup_$(date +%Y%m%d_%H%M%S).sql
   
   # Restore backup
   psql -h localhost -U postgres hawaii_business_db < backup_20240115_120000.sql
   ```

### Database Indexes

```sql
-- Performance indexes for common queries
CREATE INDEX idx_companies_island ON companies(island);
CREATE INDEX idx_companies_industry ON companies(industry);
CREATE INDEX idx_prospects_score ON prospects(score);
CREATE INDEX idx_prospects_company_id ON prospects(company_id);
CREATE INDEX idx_decision_makers_company_id ON decision_makers(company_id);
CREATE INDEX idx_companies_created_at ON companies(created_at);
```

## Monitoring & Logging

### Application Monitoring

1. **Health Check Endpoints**
   ```python
   # Add to main.py
   @app.get("/health")
   async def health_check():
       return {
           "status": "healthy",
           "timestamp": datetime.utcnow(),
           "version": "1.0.0"
       }
   
   @app.get("/health/db")
   async def database_health():
       # Check database connection
       pass
   ```

2. **Logging Configuration**
   ```python
   # logging_config.py
   import logging
   from logging.handlers import RotatingFileHandler
   
   def setup_logging():
       logging.basicConfig(
           level=logging.INFO,
           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
           handlers=[
               RotatingFileHandler(
                   'app.log', 
                   maxBytes=10*1024*1024, 
                   backupCount=5
               ),
               logging.StreamHandler()
           ]
       )
   ```

3. **Metrics Collection**
   ```python
   # metrics.py
   from prometheus_client import Counter, Histogram, start_http_server
   
   REQUEST_COUNT = Counter('app_requests_total', 'Total app requests')
   REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency')
   
   # Start metrics server
   start_http_server(8001)
   ```

### External Monitoring Services

1. **Sentry Integration**
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.fastapi import FastApiIntegration
   
   sentry_sdk.init(
       dsn=os.getenv("SENTRY_DSN"),
       integrations=[FastApiIntegration()],
       traces_sample_rate=0.1,
   )
   ```

2. **Datadog Integration**
   ```python
   from datadog import initialize, statsd
   
   initialize(
       api_key=os.getenv("DATADOG_API_KEY"),
       app_key=os.getenv("DATADOG_APP_KEY")
   )
   
   # Track metrics
   statsd.increment('hawaii_business.prospects.created')
   ```

## Backup & Recovery

### Automated Backup Strategy

1. **Database Backup Script**
   ```bash
   #!/bin/bash
   # backup.sh
   
   DATE=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="/backups"
   DB_NAME="hawaii_business_db"
   
   # Create backup
   pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/backup_$DATE.sql.gz"
   
   # Keep only last 7 days of backups
   find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
   
   # Upload to S3 (optional)
   aws s3 cp "$BACKUP_DIR/backup_$DATE.sql.gz" "s3://your-backup-bucket/database/"
   ```

2. **Automated Backup with Cron**
   ```bash
   # Add to crontab
   0 2 * * * /path/to/backup.sh >> /var/log/backup.log 2>&1
   ```

### Disaster Recovery

1. **Recovery Procedures**
   ```bash
   # Stop application
   docker-compose down
   
   # Restore database from backup
   gunzip -c backup_20240115_020000.sql.gz | psql -h localhost -U postgres hawaii_business_db
   
   # Restart application
   docker-compose up -d
   
   # Verify data integrity
   docker-compose exec backend python verify_data.py
   ```

2. **Data Verification Script**
   ```python
   # verify_data.py
   from models.database import SessionLocal
   from sqlalchemy import text
   
   def verify_data_integrity():
       db = SessionLocal()
       
       # Check record counts
       companies = db.execute(text("SELECT COUNT(*) FROM companies")).scalar()
       prospects = db.execute(text("SELECT COUNT(*) FROM prospects")).scalar()
       decision_makers = db.execute(text("SELECT COUNT(*) FROM decision_makers")).scalar()
       
       print(f"Companies: {companies}")
       print(f"Prospects: {prospects}")
       print(f"Decision Makers: {decision_makers}")
       
       # Check data consistency
       orphaned_prospects = db.execute(text("""
           SELECT COUNT(*) FROM prospects p 
           LEFT JOIN companies c ON p.company_id = c.id 
           WHERE c.id IS NULL
       """)).scalar()
       
       if orphaned_prospects > 0:
           print(f"WARNING: {orphaned_prospects} orphaned prospects found")
       else:
           print("✅ Data integrity verified")
   
   if __name__ == "__main__":
       verify_data_integrity()
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose ps database
   
   # Check database logs
   docker-compose logs database
   
   # Test connection
   docker-compose exec backend python -c "
   from models.database import SessionLocal
   db = SessionLocal()
   print('Database connection: OK')
   "
   ```

2. **API Key Issues**
   ```bash
   # Test Claude API
   curl -X POST "https://api.anthropic.com/v1/messages" \
     -H "x-api-key: $CLAUDE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
   
   # Test Google Places API
   curl "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=21.3099,-157.8581&radius=1000&key=$GOOGLE_PLACES_API_KEY"
   ```

3. **Performance Issues**
   ```bash
   # Check system resources
   docker stats
   
   # Check application logs
   docker-compose logs -f backend | grep ERROR
   
   # Check database performance
   docker-compose exec database psql -U postgres -d hawaii_business_db -c "
   SELECT query, calls, total_time, mean_time 
   FROM pg_stat_statements 
   ORDER BY total_time DESC 
   LIMIT 10;
   "
   ```

### Debug Mode

1. **Enable Debug Logging**
   ```bash
   # Set environment variable
   export DEBUG=True
   export LOG_LEVEL=DEBUG
   
   # Restart services
   docker-compose restart backend
   ```

2. **Database Query Logging**
   ```python
   # Add to database.py
   engine = create_engine(
       DATABASE_URL,
       echo=True  # Enable SQL query logging
   )
   ```

### Performance Optimization

1. **Database Optimization**
   ```sql
   -- Analyze query performance
   EXPLAIN ANALYZE SELECT * FROM prospects WHERE score > 80;
   
   -- Update table statistics
   ANALYZE companies;
   ANALYZE prospects;
   ANALYZE decision_makers;
   ```

2. **Application Caching**
   ```python
   # Add Redis caching
   from redis import Redis
   import json
   
   redis_client = Redis.from_url(os.getenv("REDIS_URL"))
   
   def get_cached_prospects():
       cached = redis_client.get("prospects:high_score")
       if cached:
           return json.loads(cached)
       
       # Fetch from database and cache
       prospects = fetch_prospects_from_db()
       redis_client.setex("prospects:high_score", 300, json.dumps(prospects))
       return prospects
   ```

---

For additional deployment questions or issues, please create an issue in the repository or contact the development team.