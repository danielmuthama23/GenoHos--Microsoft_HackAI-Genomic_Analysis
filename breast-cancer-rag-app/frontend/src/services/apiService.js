import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'https://genohos-microsoft-hackai-genomic-analysis.onrender.com/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
    'Access-Control-Allow-Origin': '*' // Add CORS header

  }
});

// Add request interceptor for auth tokens if needed
api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const queryBiospecimen = (question) => {
  return api.post('/query', { question });
};

export const getSystemStatus = () => {
  return api.get('/status');
};