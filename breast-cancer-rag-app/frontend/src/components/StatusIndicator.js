import React from 'react';

const StatusIndicator = ({ status }) => {
  const statusMap = {
    'ready': { text: 'System Ready', color: 'green' },
    'checking': { text: 'Checking System...', color: 'orange' },
    'error': { text: 'System Error', color: 'red' }
  };

  return (
    <div className="status-indicator">
      <span 
        className="status-dot" 
        style={{ backgroundColor: statusMap[status]?.color || 'gray' }}
        aria-label={`System status: ${status}`}
      />
      <span className="status-text">{statusMap[status]?.text || 'Unknown Status'}</span>
    </div>
  );
};

export default StatusIndicator;