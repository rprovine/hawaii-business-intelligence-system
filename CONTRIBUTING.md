# Contributing to Hawaii Business Intelligence System

Thank you for your interest in contributing to the Hawaii Business Intelligence System! This document provides guidelines and instructions for contributors.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

## Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct. By participating, you are expected to uphold this code:

- **Be respectful**: Treat all community members with respect and kindness
- **Be inclusive**: Welcome newcomers and help them get started
- **Be collaborative**: Work together towards common goals
- **Be professional**: Maintain professional standards in all interactions
- **Focus on Hawaii businesses**: Remember our mission to serve Hawaii's business community

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Git**: Version control system
- **Docker & Docker Compose**: For consistent development environment
- **Node.js 18+**: For frontend development
- **Python 3.9+**: For backend development
- **API Keys**: Claude API and Google Places API keys for testing

### First-Time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/hawaii-business-intelligence-system.git
   cd hawaii-business-intelligence-system
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-repo/hawaii-business-intelligence-system.git
   ```
4. **Create environment file**:
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```
5. **Start development environment**:
   ```bash
   docker-compose up -d
   ```

## Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Database Setup

```bash
# Using Docker (recommended)
docker-compose up -d database

# Manual PostgreSQL setup
createdb hawaii_business_db
psql hawaii_business_db < database/schema.sql
```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

1. **Bug Reports**: Found an issue? Let us know!
2. **Feature Requests**: Have an idea for improvement?
3. **Code Contributions**: Bug fixes, new features, optimizations
4. **Documentation**: Improve docs, add examples, fix typos
5. **Testing**: Add test cases, improve test coverage
6. **Hawaii Business Data**: Help us identify new data sources

### Contribution Workflow

1. **Check existing issues** before starting work
2. **Create an issue** for new features or major changes
3. **Fork and create a branch** from `main`
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request** with clear description

### Branch Naming Convention

Use descriptive branch names:

- `feature/add-maui-business-scraper`
- `bugfix/fix-prospect-scoring-algorithm`
- `docs/update-api-documentation`
- `refactor/optimize-database-queries`

## Pull Request Process

### Before Submitting

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "feat: add new Hawaii business scraper for Maui"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Requirements

Your PR should include:

- **Clear title and description** explaining the changes
- **Reference to related issues** (e.g., "Fixes #123")
- **Test coverage** for new functionality
- **Documentation updates** if applicable
- **No breaking changes** unless discussed in advance

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Closes #[issue number]

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Checklist
- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment information**:
   - OS (macOS, Windows, Linux)
   - Python version
   - Node.js version
   - Browser (if frontend issue)
5. **Error messages** or logs
6. **Screenshots** if helpful

### Feature Requests

For feature requests, include:

1. **Clear description** of the proposed feature
2. **Use case** explaining why it's needed
3. **Proposed solution** if you have ideas
4. **Alternative solutions** considered
5. **Hawaii business context** if relevant

### Issue Labels

We use these labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `hawaii-specific`: Related to Hawaii business requirements
- `api`: Backend API related
- `frontend`: React frontend related
- `database`: Database related
- `scraping`: Web scraping related
- `ai-analysis`: Claude AI analysis related

## Coding Standards

### Python (Backend)

Follow **PEP 8** style guidelines:

```python
# Good
def analyze_hawaii_business(company_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a Hawaii business for AI consulting opportunities.
    
    Args:
        company_data: Dictionary containing business information
        
    Returns:
        Dictionary containing analysis results
    """
    if not company_data.get('name'):
        raise ValueError("Company name is required")
    
    return {
        'score': calculate_score(company_data),
        'analysis': generate_analysis(company_data)
    }

# Use type hints
from typing import List, Dict, Optional, Any

# Document classes and functions
class HawaiiBusinessAnalyzer:
    """Analyzes Hawaii businesses for AI consulting potential."""
    
    def __init__(self, claude_api_key: str):
        self.claude_client = Anthropic(api_key=claude_api_key)
```

### TypeScript (Frontend)

Follow consistent TypeScript practices:

```typescript
// Use interfaces for type definitions
interface Prospect {
  id: string;
  companyId: string;
  score: number;
  aiAnalysis: string;
  painPoints: string[];
  recommendedServices: Service[];
}

// Use proper component structure
interface ProspectCardProps {
  prospect: Prospect;
  onSelect: (prospect: Prospect) => void;
}

const ProspectCard: React.FC<ProspectCardProps> = ({ prospect, onSelect }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold">{prospect.company.name}</h3>
      <p className="text-gray-600">Score: {prospect.score}/100</p>
    </div>
  );
};

export default ProspectCard;
```

### Database

Follow these database conventions:

```sql
-- Use snake_case for table and column names
CREATE TABLE hawaii_businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name VARCHAR(255) NOT NULL,
    island_location island_enum NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add appropriate indexes
CREATE INDEX idx_hawaii_businesses_island ON hawaii_businesses(island_location);
CREATE INDEX idx_hawaii_businesses_created_at ON hawaii_businesses(created_at);

-- Use descriptive constraint names
ALTER TABLE hawaii_businesses 
ADD CONSTRAINT chk_company_name_not_empty 
CHECK (LENGTH(TRIM(company_name)) > 0);
```

### API Design

Follow RESTful API conventions:

```python
# Good endpoint design
@router.get("/companies/{company_id}/prospects")
async def get_company_prospects(
    company_id: UUID,
    min_score: Optional[int] = Query(None, ge=0, le=100),
    limit: int = Query(50, ge=1, le=100)
) -> ProspectListResponse:
    """Get prospects for a specific company."""
    pass

# Use appropriate HTTP methods
@router.post("/prospects")  # Create
@router.get("/prospects/{id}")  # Read
@router.put("/prospects/{id}")  # Update
@router.delete("/prospects/{id}")  # Delete

# Use consistent response formats
class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

## Testing

### Backend Testing

```python
# Write comprehensive tests
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_hawaii_prospects():
    """Test retrieving Hawaii business prospects."""
    response = client.get("/api/prospects?island=Oahu")
    
    assert response.status_code == 200
    data = response.json()
    assert "prospects" in data
    assert len(data["prospects"]) > 0
    
    # Test specific prospect data
    prospect = data["prospects"][0]
    assert "score" in prospect
    assert 0 <= prospect["score"] <= 100

def test_ai_analysis_with_real_data():
    """Test AI analysis with real Hawaii business data."""
    test_company = {
        "name": "Test Dental Practice",
        "island": "Oahu",
        "industry": "Healthcare",
        "employee_count": 15
    }
    
    response = client.post("/api/ai-analysis/analyze", json=test_company)
    assert response.status_code == 200
    
    analysis = response.json()["analysis"]
    assert len(analysis) > 100  # Ensure substantial analysis
    assert "Hawaii" in analysis  # Check for Hawaii context
```

### Frontend Testing

```typescript
// Component testing with React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';
import ProspectCard from '../components/ProspectCard';

const mockProspect = {
  id: '1',
  company: { name: 'Hawaii Dental Care' },
  score: 85,
  island: 'Oahu',
  industry: 'Healthcare'
};

test('displays prospect information correctly', () => {
  render(<ProspectCard prospect={mockProspect} onSelect={jest.fn()} />);
  
  expect(screen.getByText('Hawaii Dental Care')).toBeInTheDocument();
  expect(screen.getByText('Score: 85/100')).toBeInTheDocument();
  expect(screen.getByText('Oahu')).toBeInTheDocument();
});

test('calls onSelect when clicked', () => {
  const mockOnSelect = jest.fn();
  render(<ProspectCard prospect={mockProspect} onSelect={mockOnSelect} />);
  
  fireEvent.click(screen.getByTestId('prospect-card'));
  expect(mockOnSelect).toHaveBeenCalledWith(mockProspect);
});
```

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=.

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### Test Coverage

Maintain minimum test coverage:
- **Backend**: 80% code coverage
- **Frontend**: 70% code coverage
- **Critical paths**: 95% coverage (AI analysis, data scraping)

## Hawaii-Specific Considerations

When contributing, keep in mind:

### Cultural Sensitivity
- Respect Hawaiian culture and business practices
- Use inclusive language in code and documentation
- Consider the "Aloha spirit" in user interactions

### Local Business Context
- Understand unique Hawaii challenges (island logistics, tourism dependency)
- Consider inter-island business relationships
- Respect local business community connections

### Data Accuracy
- Ensure all scraped business data is accurate and current
- Verify Hawaii business addresses and contact information
- Respect rate limits when scraping local business websites

### Performance Considerations
- Consider slower internet connections on outer islands
- Optimize for mobile usage (common in Hawaii)
- Handle timezone considerations (Hawaii Standard Time)

## Recognition

Contributors will be recognized in:
- **README.md**: Major contributors listed
- **CHANGELOG.md**: Contributors mentioned in release notes
- **GitHub**: Contributor graph and commit history
- **LinkedIn posts**: Public recognition for significant contributions

## Questions?

If you have questions about contributing:

1. **Check existing documentation** first
2. **Search closed issues** for similar questions
3. **Create a new issue** with your question
4. **Join discussions** in existing issues
5. **Contact maintainers** directly if needed

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

**Mahalo for contributing to Hawaii's business intelligence future!** 🌺