-- Hawaii Business Intelligence System Database Schema

-- Note: Database should be created before running this script
-- CREATE DATABASE hawaii_business_intel;

-- Islands enum
CREATE TYPE island_enum AS ENUM ('Oahu', 'Maui', 'Big Island', 'Kauai', 'Molokai', 'Lanai', 'All Islands');

-- Industry enum
CREATE TYPE industry_enum AS ENUM (
    'Tourism', 'Hospitality', 'Agriculture', 'Retail', 
    'Healthcare', 'Real Estate', 'Technology', 'Construction', 
    'Food Service', 'Transportation', 'Professional Services', 'Other'
);

-- Service type enum
CREATE TYPE service_enum AS ENUM (
    'Data Analytics', 'Custom Chatbots', 'Fractional CTO', 'HubSpot Digital Marketing'
);

-- Companies table
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    island island_enum NOT NULL,
    industry industry_enum NOT NULL,
    website VARCHAR(255),
    phone VARCHAR(20),
    employee_count_estimate INTEGER,
    annual_revenue_estimate DECIMAL(12, 2),
    description TEXT,
    source VARCHAR(100),
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, island)
);

-- Prospects table
CREATE TABLE prospects (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    score INTEGER CHECK (score >= 0 AND score <= 100),
    ai_analysis TEXT,
    pain_points TEXT[],
    recommended_services service_enum[],
    estimated_deal_value DECIMAL(10, 2),
    growth_signals TEXT[],
    technology_readiness VARCHAR(50),
    priority_level VARCHAR(20) CHECK (priority_level IN ('High', 'Medium', 'Low')),
    last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Decision makers table
CREATE TABLE decision_makers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    linkedin_url VARCHAR(255),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interactions table
CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    prospect_id INTEGER REFERENCES prospects(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50) NOT NULL,
    interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    outcome VARCHAR(100),
    next_action VARCHAR(255),
    next_action_date DATE,
    created_by VARCHAR(100)
);

-- Pipeline stages table
CREATE TABLE pipeline_stages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    order_position INTEGER NOT NULL,
    description TEXT,
    UNIQUE(name)
);

-- Insert default pipeline stages
INSERT INTO pipeline_stages (name, order_position, description) VALUES
('Lead', 1, 'Newly identified prospect'),
('Qualified', 2, 'Prospect has been qualified with high score'),
('Contacted', 3, 'Initial outreach completed'),
('Meeting Scheduled', 4, 'Discovery meeting scheduled'),
('Proposal Sent', 5, 'Service proposal delivered'),
('Negotiation', 6, 'Terms being negotiated'),
('Closed Won', 7, 'Deal closed successfully'),
('Closed Lost', 8, 'Deal lost or prospect declined');

-- Opportunities table
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    prospect_id INTEGER REFERENCES prospects(id) ON DELETE CASCADE,
    stage_id INTEGER REFERENCES pipeline_stages(id),
    services service_enum[],
    estimated_value DECIMAL(10, 2),
    probability INTEGER CHECK (probability >= 0 AND probability <= 100),
    expected_close_date DATE,
    actual_close_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics snapshots table
CREATE TABLE analytics_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_date DATE NOT NULL,
    total_prospects INTEGER,
    prospects_by_island JSONB,
    prospects_by_industry JSONB,
    average_score DECIMAL(5, 2),
    high_priority_count INTEGER,
    total_pipeline_value DECIMAL(12, 2),
    conversion_rate DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(snapshot_date)
);

-- Data collection logs table
CREATE TABLE data_collection_logs (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    records_found INTEGER,
    records_processed INTEGER,
    records_added INTEGER,
    errors INTEGER,
    error_details TEXT,
    duration_seconds INTEGER,
    status VARCHAR(20)
);

-- Email alerts table
CREATE TABLE email_alerts (
    id SERIAL PRIMARY KEY,
    prospect_id INTEGER REFERENCES prospects(id) ON DELETE CASCADE,
    alert_type VARCHAR(50),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recipient_email VARCHAR(255),
    subject TEXT,
    body TEXT,
    status VARCHAR(20)
);

-- Create indexes for better performance
CREATE INDEX idx_companies_island ON companies(island);
CREATE INDEX idx_companies_industry ON companies(industry);
CREATE INDEX idx_prospects_score ON prospects(score DESC);
CREATE INDEX idx_prospects_priority ON prospects(priority_level);
CREATE INDEX idx_opportunities_stage ON opportunities(stage_id);
CREATE INDEX idx_interactions_prospect ON interactions(prospect_id);
CREATE INDEX idx_interactions_date ON interactions(interaction_date);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_prospects_updated_at BEFORE UPDATE ON prospects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();