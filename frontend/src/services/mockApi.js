// Mock API service for when backend is unavailable
const mockData = {
  dashboard: {
    total_companies: 15,
    total_prospects: 15,
    active_workflows: 3,
    recent_interactions: 8,
    high_score_prospects: 12,
    average_score: 85
  },
  companies: [
    {id: 1, name: "Aloha Medical Center", website: "https://alohamedical.com", island: "Oahu", industry: "Healthcare", employee_count_estimate: 450},
    {id: 2, name: "Pacific Paradise Resort", website: "https://pacificparadise.com", island: "Maui", industry: "Tourism", employee_count_estimate: 320},
    {id: 3, name: "Kona Coffee Collective", website: "https://konacoffee.com", island: "Big Island", industry: "Food Service", employee_count_estimate: 85},
    {id: 4, name: "Island Tech Solutions", website: "https://islandtech.com", island: "Oahu", industry: "Technology", employee_count_estimate: 150},
    {id: 5, name: "Kauai Adventure Tours", website: "https://kauaiadventure.com", island: "Kauai", industry: "Tourism", employee_count_estimate: 65},
    {id: 6, name: "Honolulu Construction Group", island: "Oahu", industry: "Real Estate", employee_count_estimate: 280},
    {id: 7, name: "Ohana Dental Care", island: "Oahu", industry: "Healthcare", employee_count_estimate: 45},
    {id: 8, name: "Big Island Solar", island: "Big Island", industry: "Technology", employee_count_estimate: 75},
    {id: 9, name: "Maui Ocean Center", island: "Maui", industry: "Tourism", employee_count_estimate: 120},
    {id: 10, name: "Lanai Luxury Properties", island: "Lanai", industry: "Real Estate", employee_count_estimate: 35},
    {id: 11, name: "Molokai Fish & Dive", island: "Molokai", industry: "Tourism", employee_count_estimate: 25},
    {id: 12, name: "Waikiki Beach Hotel", island: "Oahu", industry: "Tourism", employee_count_estimate: 380},
    {id: 13, name: "Kauai Medical Clinic", island: "Kauai", industry: "Healthcare", employee_count_estimate: 95},
    {id: 14, name: "Maui Fresh Produce", island: "Maui", industry: "Food Service", employee_count_estimate: 60},
    {id: 15, name: "Hawaii Digital Marketing", island: "Oahu", industry: "Technology", employee_count_estimate: 40}
  ],
  prospects: [
    {id: 1, company_id: 1, score: 92, priority_level: "High", company_name: "Aloha Medical Center", ai_analysis: "High potential for AI integration in patient management, appointment scheduling, and diagnostic assistance. Strong digital presence indicates readiness.", pain_points: ["Long patient wait times", "Manual record keeping", "Staff scheduling complexity"], recommended_services: ["AI Scheduling System", "Predictive Analytics", "Patient Chatbot"]},
    {id: 2, company_id: 2, score: 88, priority_level: "High", company_name: "Pacific Paradise Resort", ai_analysis: "Excellent candidate for AI-powered booking optimization and guest experience enhancement. Tourism sector with high automation potential.", pain_points: ["Seasonal demand fluctuations", "Guest service response time", "Revenue optimization"], recommended_services: ["Dynamic Pricing AI", "Guest Experience Bot", "Predictive Maintenance"]},
    {id: 3, company_id: 3, score: 85, priority_level: "Medium", company_name: "Kona Coffee Collective", ai_analysis: "Could benefit from AI in supply chain optimization and customer preference analytics. Growing business with scalability needs.", pain_points: ["Inventory management", "Demand forecasting", "Customer retention"], recommended_services: ["Inventory AI", "Customer Analytics", "Quality Control ML"]},
    {id: 4, company_id: 4, score: 95, priority_level: "High", company_name: "Island Tech Solutions", ai_analysis: "Already tech-savvy, perfect for advanced AI solutions and could be a strategic partner for implementations.", pain_points: ["Project resource allocation", "Client requirement analysis", "Code quality assurance"], recommended_services: ["AI Development Tools", "Automated Testing", "Project Management AI"]},
    {id: 5, company_id: 5, score: 87, priority_level: "High", company_name: "Kauai Adventure Tours", ai_analysis: "AI can significantly optimize tour scheduling, weather-based planning, and personalized recommendations.", pain_points: ["Weather-dependent scheduling", "Group size optimization", "Marketing reach"], recommended_services: ["Booking Optimization", "Weather Prediction AI", "Marketing Automation"]}
  ],
  analyticsByIsland: {
    "Oahu": 6,
    "Maui": 3,
    "Big Island": 2,
    "Kauai": 2,
    "Molokai": 1,
    "Lanai": 1
  },
  analyticsByIndustry: {
    "Tourism": 5,
    "Healthcare": 3,
    "Technology": 3,
    "Food Service": 2,
    "Real Estate": 2
  }
};

export const mockApi = {
  isAvailable: false,
  
  // Check if real API is available
  async checkAvailability() {
    try {
      const response = await fetch('/api/health', { method: 'GET', timeout: 3000 });
      this.isAvailable = response.ok;
      return this.isAvailable;
    } catch {
      this.isAvailable = false;
      return false;
    }
  },
  
  // Get dashboard data
  async getDashboard() {
    return mockData.dashboard;
  },
  
  // Get companies
  async getCompanies(filters = {}) {
    let companies = [...mockData.companies];
    if (filters.island) {
      companies = companies.filter(c => c.island === filters.island);
    }
    if (filters.industry) {
      companies = companies.filter(c => c.industry === filters.industry);
    }
    return companies;
  },
  
  // Get prospects
  async getProspects(filters = {}) {
    let prospects = [...mockData.prospects];
    if (filters.priority) {
      prospects = prospects.filter(p => p.priority_level === filters.priority);
    }
    if (filters.min_score) {
      prospects = prospects.filter(p => p.score >= filters.min_score);
    }
    return prospects;
  },
  
  // Get analytics by island
  async getAnalyticsByIsland() {
    return mockData.analyticsByIsland;
  },
  
  // Get analytics by industry
  async getAnalyticsByIndustry() {
    return mockData.analyticsByIndustry;
  }
};

export default mockApi;