const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'https://genohos-microsoft-hackai-genomic-analysis.onrender.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',  // Added missing comma here
    'Access-Control-Allow-Origin': '*'
  }
});

// Update query function to match backend expectations
export const queryBiospecimen = (question, top_results = 3) => {
  return api.post('/query', { question, top_results });  // Added top_results
};

