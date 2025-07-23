import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard
export const fetchDashboardData = async () => {
  const response = await api.get('/api/analytics/dashboard');
  return response.data;
};

// Prospects
export const fetchProspects = async (filters: any = {}) => {
  const response = await api.get('/api/prospects', { params: filters });
  return response.data;
};

export const fetchProspectById = async (id: string) => {
  const response = await api.get(`/api/prospects/${id}`);
  return response.data;
};

export const updateProspect = async (id: string, data: any) => {
  const response = await api.put(`/api/prospects/${id}`, data);
  return response.data;
};

export const analyzeProspect = async (id: string) => {
  const response = await api.post(`/api/prospects/${id}/analyze`);
  return response.data;
};

// Companies
export const fetchCompanies = async (filters: any = {}) => {
  const response = await api.get('/api/companies', { params: filters });
  return response.data;
};

export const createCompany = async (data: any) => {
  const response = await api.post('/api/companies', data);
  return response.data;
};

// Interactions
export const fetchInteractions = async (prospectId: string) => {
  const response = await api.get(`/api/interactions`, { 
    params: { prospect_id: prospectId } 
  });
  return response.data;
};

export const createInteraction = async (data: any) => {
  const response = await api.post('/api/interactions', data);
  return response.data;
};

// Analytics
export const fetchAnalyticsByIsland = async () => {
  const response = await api.get('/api/analytics/by-island');
  return response.data;
};

export const fetchAnalyticsByIndustry = async () => {
  const response = await api.get('/api/analytics/by-industry');
  return response.data;
};

export const fetchAnalyticsTimeline = async (days: number = 30) => {
  const response = await api.get(`/api/analytics/timeline`, { 
    params: { days } 
  });
  return response.data;
};

// Workflows
export const triggerWorkflow = async (workflow: any) => {
  const response = await api.post('/api/workflows/trigger', workflow);
  return response.data;
};

export const fetchWorkflowStatus = async () => {
  const response = await api.get('/api/workflows/status');
  return response.data;
};

export const fetchDataCollectionLogs = async () => {
  const response = await api.get('/api/workflows/logs');
  return response.data;
};

export default api;