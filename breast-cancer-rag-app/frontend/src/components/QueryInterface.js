import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ResultsViewer from './ResultsViewer';
import StatusIndicator from './StatusIndicator';

const QueryInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [systemStatus, setSystemStatus] = useState('checking');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const { data } = await axios.get('/api/status');
        setSystemStatus(data.status === 'ready' ? 'ready' : 'error');
      } catch (err) {
        setSystemStatus('error');
        setError('Failed to connect to backend service');
      }
    };
    checkStatus();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || systemStatus !== 'ready') return;
    
    setLoading(true);
    setError(null);
    
    try {
      const { data } = await axios.post('/api/query', { question: query });
      setResponse(data);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="query-container">
      <h1>Biospecimen Research Assistant</h1>
      
      <StatusIndicator status={systemStatus} />
      
      <form onSubmit={handleSubmit} className="query-form">
        <div className="input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about biospecimen samples..."
            disabled={loading || systemStatus !== 'ready'}
            aria-label="Enter your research question"
          />
          <button 
            type="submit" 
            disabled={loading || !query.trim() || systemStatus !== 'ready'}
          >
            {loading ? 'Processing...' : 'Ask'}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}

      {response && (
        <ResultsViewer 
          answer={response.answer}
          sources={response.sources}
          processingTime={response.processing_time}
        />
      )}

      <div className="examples">
        <h3>Try asking:</h3>
        <ul>
          <li onClick={() => setQuery("Show breast tissue samples with volume > 1ml")}>
            Show breast tissue samples with volume > 1ml
          </li>
          <li onClick={() => setQuery("What lung cancer samples are available?")}>
            What lung cancer samples are available?
          </li>
          <li onClick={() => setQuery("Find samples with high concentration from female patients")}>
            Find samples with high concentration from female patients
          </li>
        </ul>
      </div>
    </div>
  );
};

export default QueryInterface;