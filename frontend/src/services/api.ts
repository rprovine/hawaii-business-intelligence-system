import axios from 'axios';

// Use Supabase Edge Function URL directly (fallback if env vars not working)
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  'https://giefuhaiojygbtnenbph.supabase.co/functions/v1/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdpZWZ1aGFpb2p5Z2J0bmVuYnBoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUwOTU2MDAsImV4cCI6MjA1MDY3MTYwMH0.PQKXo1O8pz83cTMFOxbGvnpvzFMbI9Z97WdP2wbXgvQ',
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdpZWZ1aGFpb2p5Z2J0bmVuYnBoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUwOTU2MDAsImV4cCI6MjA1MDY3MTYwMH0.PQKXo1O8pz83cTMFOxbGvnpvzFMbI9Z97WdP2wbXgvQ'
  },
});

// Dashboard
export const fetchDashboardData = async () => {
  const response = await api.get('/analytics/dashboard');
  return response.data;
};

// Prospects
export const fetchProspects = async (filters: any = {}) => {
  const response = await api.get('/prospects', { params: filters });
  return response.data;
};

export const fetchProspectById = async (id: string) => {
  const response = await api.get(`/prospects/${id}`);
  return response.data;
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
  const response = await api.get('/companies', { params: filters });
  return response.data;
};

export const createCompany = async (data: any) => {
  const response = await api.post('/companies', data);
  return response.data;
};

// Interactions
export const fetchInteractions = async (prospectId: string) => {
  const response = await api.get(`/interactions`, { 
    params: { prospect_id: prospectId } 
  });
  return response.data;
};

export const createInteraction = async (data: any) => {
  const response = await api.post('/interactions', data);
  return response.data;
};

// Analytics
export const fetchAnalyticsByIsland = async () => {
  const response = await api.get('/analytics/by-island');
  return response.data;
};

export const fetchAnalyticsByIndustry = async () => {
  const response = await api.get('/analytics/by-industry');
  return response.data;
};

export const fetchAnalyticsTimeline = async (days: number = 30) => {
  const response = await api.get(`/analytics/timeline`, { 
    params: { days } 
  });
  return response.data;
};

// Workflows
export const triggerWorkflow = async (workflow: any) => {
  const response = await api.post('/workflows/trigger', workflow);
  return response.data;
};

export const fetchWorkflowStatus = async () => {
  const response = await api.get('/workflows/status');
  return response.data;
};

export const fetchDataCollectionLogs = async () => {
  const response = await api.get('/workflows/logs');
  return response.data;
};

export default api;