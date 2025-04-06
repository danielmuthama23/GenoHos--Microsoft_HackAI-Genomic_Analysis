import axios from 'axios';

const api = axios.create({
  baseURL: 'https://genohos-microsoft-hackai-genomic-analysis.onrender.com/api', // set the full base URL directly
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
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
