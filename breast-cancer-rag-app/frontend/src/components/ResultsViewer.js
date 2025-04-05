import React from 'react';

const ResultsViewer = ({ answer, sources, processingTime }) => {
  return (
    <div className="results-viewer">
      <div className="answer-section">
        <h2>Answer</h2>
        <p>{answer}</p>
        <div className="meta-info">
          <span>Processed in {processingTime}</span>
        </div>
      </div>
      
      {sources.length > 0 && (
        <div className="sources-section">
          <h2>Supporting References</h2>
          <div className="sources-grid">
            {sources.map((source, index) => (
              <div key={index} className="source-card">
                <div className="similarity-badge">
                  Similarity: {(source.similarity * 100).toFixed(1)}%
                </div>
                <div className="source-content">
                  <p>{source.content}</p>
                </div>
                <div className="source-meta">
                  <span><strong>Type:</strong> {source.metadata?.sample_type || 'Unknown'}</span>
                  <span><strong>Site:</strong> {source.metadata?.primary_site || 'Unknown'}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsViewer;