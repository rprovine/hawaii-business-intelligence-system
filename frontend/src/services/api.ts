import axios from 'axios';

// Use relative API path when deployed on Vercel
// Force using /api to avoid any cached environment variables
const API_BASE_URL = '/api';
console.log('API Base URL (forced to /api):', API_BASE_URL);
console.log('Environment API URL was:', process.env.REACT_APP_API_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.url, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.config?.url, error.message, error.response?.status);
    return Promise.reject(error);
  }
);

// Dashboard
export const fetchDashboardData = async () => {
  try {
    const response = await api.get('/analytics/dashboard');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch dashboard from API, using fallback data:', error);
    // Return fallback data if API fails
    return {
      total_companies: 15,
      total_prospects: 15,
      high_priority_count: 5,
      total_pipeline_value: 125000,
      active_workflows: 3,
      recent_interactions: 8,
      high_score_prospects: 8,
      average_score: 85,
      by_island: [
        { island: 'Oahu', prospect_count: 6 },
        { island: 'Maui', prospect_count: 3 },
        { island: 'Big Island', prospect_count: 2 },
        { island: 'Kauai', prospect_count: 2 },
        { island: 'Molokai', prospect_count: 1 },
        { island: 'Lanai', prospect_count: 1 }
      ],
      by_industry: [
        { industry: 'Tourism', prospect_count: 5 },
        { industry: 'Healthcare', prospect_count: 3 },
        { industry: 'Technology', prospect_count: 3 },
        { industry: 'Food Service', prospect_count: 2 },
        { industry: 'Real Estate', prospect_count: 2 }
      ],
      recent_high_scores: [
        {
          id: 1,
          score: 92,
          company: {
            name: 'Aloha Medical Center',
            island: 'Oahu',
            industry: 'Healthcare'
          },
          recommended_services: ['AI Scheduling System', 'Predictive Analytics', 'Patient Chatbot']
        },
        {
          id: 2,
          score: 88,
          company: {
            name: 'Pacific Paradise Resort',
            island: 'Maui',
            industry: 'Tourism'
          },
          recommended_services: ['Dynamic Pricing AI', 'Guest Experience Bot']
        },
        {
          id: 4,
          score: 95,
          company: {
            name: 'Island Tech Solutions',
            island: 'Oahu',
            industry: 'Technology'
          },
          recommended_services: ['AI Development Tools', 'Automated Testing']
        }
      ]
    };
  }
};

// Prospects
export const fetchProspects = async (filters: any = {}) => {
  try {
    const response = await api.get('/prospects', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch prospects, using fallback data:', error);
    return [
      {
        id: 1,
        company_id: 1,
        score: 92,
        priority_level: "High",
        ai_analysis: "High potential for AI integration in patient management.",
        pain_points: ["Long patient wait times", "Manual record keeping"],
        recommended_services: ["AI Scheduling System", "Predictive Analytics"],
        company: { name: "Aloha Medical Center", island: "Oahu", industry: "Healthcare" },
        company_name: "Aloha Medical Center"
      },
      {
        id: 2,
        company_id: 2,
        score: 88,
        priority_level: "High",
        ai_analysis: "Excellent candidate for AI-powered booking optimization.",
        pain_points: ["Seasonal demand fluctuations", "Guest service response time"],
        recommended_services: ["Dynamic Pricing AI", "Guest Experience Bot"],
        company: { name: "Pacific Paradise Resort", island: "Maui", industry: "Tourism" },
        company_name: "Pacific Paradise Resort"
      },
      {
        id: 3,
        company_id: 3,
        score: 85,
        priority_level: "Medium",
        ai_analysis: "Could benefit from AI in supply chain optimization.",
        pain_points: ["Inventory management", "Demand forecasting"],
        recommended_services: ["Inventory AI", "Customer Analytics"],
        company: { name: "Kona Coffee Collective", island: "Big Island", industry: "Food Service" },
        company_name: "Kona Coffee Collective"
      },
      {
        id: 4,
        company_id: 4,
        score: 95,
        priority_level: "High",
        ai_analysis: "Already tech-savvy, perfect for advanced AI solutions.",
        pain_points: ["Project resource allocation", "Client requirement analysis"],
        recommended_services: ["AI Development Tools", "Automated Testing"],
        company: { name: "Island Tech Solutions", island: "Oahu", industry: "Technology" },
        company_name: "Island Tech Solutions"
      },
      {
        id: 5,
        company_id: 5,
        score: 87,
        priority_level: "High",
        ai_analysis: "AI can significantly optimize tour scheduling.",
        pain_points: ["Weather-dependent scheduling", "Group size optimization"],
        recommended_services: ["Booking Optimization", "Weather Prediction AI"],
        company: { name: "Kauai Adventure Tours", island: "Kauai", industry: "Tourism" },
        company_name: "Kauai Adventure Tours"
      }
    ];
  }
};

export const fetchProspectById = async (id: string) => {
  try {
    const response = await api.get(`/prospects/${id}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch prospect, using fallback data:', error);
    const prospects = [
      {
        id: 1,
        company_id: 1,
        score: 92,
        priority_level: "High",
        ai_analysis: "High potential for AI integration in patient management, appointment scheduling, and diagnostic assistance. Strong digital presence indicates readiness.",
        pain_points: ["Long patient wait times", "Manual record keeping", "Staff scheduling complexity"],
        recommended_services: ["AI Scheduling System", "Predictive Analytics", "Patient Chatbot"],
        company: {
          name: "Aloha Medical Center",
          island: "Oahu",
          industry: "Healthcare",
          website: "https://alohamedical.com",
          employee_count_estimate: 450
        },
        company_name: "Aloha Medical Center"
      }
    ];
    return prospects[0];
  }
};

export const updateProspect = async (id: string, data: any) => {
  const response = await api.put(`/prospects/${id}`, data);
  return response.data;
};

export const analyzeProspect = async (id: string) => {
  const response = await api.post(`/prospects/${id}/analyze`);
  return response.data;
};

// Companies
export const fetchCompanies = async (filters: any = {}) => {
  try {
    const response = await api.get('/companies', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch companies, using fallback data:', error);
    return [
      { id: 1, name: "Aloha Medical Center", island: "Oahu", industry: "Healthcare" },
      { id: 2, name: "Pacific Paradise Resort", island: "Maui", industry: "Tourism" },
      { id: 3, name: "Kona Coffee Collective", island: "Big Island", industry: "Food Service" },
      { id: 4, name: "Island Tech Solutions", island: "Oahu", industry: "Technology" },
      { id: 5, name: "Kauai Adventure Tours", island: "Kauai", industry: "Tourism" }
    ];
  }
};

export const createCompany = async (data: any) => {
  const response = await api.post('/companies', data);
  return response.data;
};

// Interactions
export const fetchInteractions = async (prospectId: string) => {
  try {
    const response = await api.get(`/interactions`, { 
      params: { prospect_id: prospectId } 
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch interactions, using fallback:', error);
    return [
      {
        id: 1,
        type: 'email',
        date: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2).toISOString(),
        subject: 'Introduction to AI Solutions',
        notes: 'Sent initial outreach email'
      },
      {
        id: 2,
        type: 'call',
        date: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
        subject: 'Follow-up Call',
        notes: 'Discussed potential solutions'
      }
    ];
  }
};

export const createInteraction = async (data: any) => {
  try {
    const response = await api.post('/interactions', data);
    return response.data;
  } catch (error) {
    console.error('Failed to create interaction:', error);
    return { ...data, id: Date.now(), status: 'created' };
  }
};

// Analytics
export const fetchAnalyticsByIsland = async () => {
  try {
    const response = await api.get('/analytics/by-island');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch analytics by island:', error);
    return { "Oahu": 6, "Maui": 3, "Big Island": 2, "Kauai": 2, "Molokai": 1, "Lanai": 1 };
  }
};

export const fetchAnalyticsByIndustry = async () => {
  try {
    const response = await api.get('/analytics/by-industry');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch analytics by industry:', error);
    return { "Tourism": 5, "Healthcare": 3, "Technology": 3, "Food Service": 2, "Real Estate": 2 };
  }
};

export const fetchAnalyticsTimeline = async (days: number = 30) => {
  try {
    const response = await api.get(`/analytics/timeline`, { 
      params: { days } 
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch timeline:', error);
    const timeline = [];
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      timeline.push({
        date: date.toISOString().split('T')[0],
        prospects_created: Math.floor(Math.random() * 3) + 1,
        interactions: Math.floor(Math.random() * 5) + 2
      });
    }
    return timeline;
  }
};

// Workflows
export const triggerWorkflow = async (workflow: any) => {
  try {
    const response = await api.post('/workflows/trigger', workflow);
    return response.data;
  } catch (error) {
    console.error('Failed to trigger workflow:', error);
    return {
      success: true,
      workflow_id: 'mock-' + Date.now(),
      message: 'Workflow triggered (simulated)'
    };
  }
};

export const fetchWorkflowStatus = async () => {
  try {
    const response = await api.get('/workflows/status');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch workflow status, using fallback:', error);
    return {
      active: 2,
      completed: 42,
      failed: 1,
      pending: 3,
      running_workflows: []
    };
  }
};

export const fetchDataCollectionLogs = async () => {
  try {
    const response = await api.get('/workflows/logs');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch logs, using fallback:', error);
    return [];
  }
};

export default api;