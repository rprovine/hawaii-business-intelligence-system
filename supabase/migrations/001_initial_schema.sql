-- Create companies table
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    website VARCHAR(255),
    island VARCHAR(100),
    industry VARCHAR(100),
    employee_count_estimate INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create prospects table
CREATE TABLE IF NOT EXISTS prospects (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    score INTEGER DEFAULT 0,
    priority_level VARCHAR(50) DEFAULT 'Medium',
    ai_analysis TEXT,
    pain_points TEXT[],
    recommended_services TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_companies_island ON companies(island);
CREATE INDEX idx_companies_industry ON companies(industry);
CREATE INDEX idx_prospects_score ON prospects(score);
CREATE INDEX idx_prospects_company ON prospects(company_id);

-- Enable Row Level Security
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE prospects ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for now, can be restricted later)
CREATE POLICY "Allow all operations on companies" ON companies
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on prospects" ON prospects
    FOR ALL USING (true);

-- Insert demo data
INSERT INTO companies (name, website, island, industry, employee_count_estimate) VALUES
    ('Aloha Medical Center', 'https://alohamedical.com', 'Oahu', 'Healthcare', 450),
    ('Pacific Paradise Resort', 'https://pacificparadise.com', 'Maui', 'Tourism', 320),
    ('Kona Coffee Collective', 'https://konacoffee.com', 'Big Island', 'Food Service', 85),
    ('Island Tech Solutions', 'https://islandtech.com', 'Oahu', 'Technology', 150),
    ('Kauai Adventure Tours', 'https://kauaiadventure.com', 'Kauai', 'Tourism', 65),
    ('Honolulu Construction Group', NULL, 'Oahu', 'Real Estate', 280),
    ('Ohana Dental Care', NULL, 'Oahu', 'Healthcare', 45),
    ('Big Island Solar', NULL, 'Big Island', 'Technology', 75),
    ('Maui Ocean Center', NULL, 'Maui', 'Tourism', 120),
    ('Lanai Luxury Properties', NULL, 'Lanai', 'Real Estate', 35),
    ('Molokai Fish & Dive', NULL, 'Molokai', 'Tourism', 25),
    ('Waikiki Beach Hotel', NULL, 'Oahu', 'Tourism', 380),
    ('Kauai Medical Clinic', NULL, 'Kauai', 'Healthcare', 95),
    ('Maui Fresh Produce', NULL, 'Maui', 'Food Service', 60),
    ('Hawaii Digital Marketing', NULL, 'Oahu', 'Technology', 40);

-- Insert prospects for each company
INSERT INTO prospects (company_id, score, priority_level, ai_analysis, pain_points, recommended_services)
SELECT 
    id,
    80 + (RANDOM() * 20)::INT,
    CASE 
        WHEN RANDOM() > 0.7 THEN 'High'
        WHEN RANDOM() > 0.4 THEN 'Medium'
        ELSE 'Low'
    END,
    'High potential for AI integration. Strong digital presence indicates readiness for automation and AI solutions.',
    ARRAY['Manual processes', 'Data management', 'Customer engagement'],
    ARRAY['AI Automation', 'Data Analytics', 'Customer Chatbot']
FROM companies;