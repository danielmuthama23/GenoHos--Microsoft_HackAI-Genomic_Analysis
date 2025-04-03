// src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.min.css';

// Create a root element for React 18's concurrent rendering
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the main App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Performance monitoring (optional)
// Learn more: https://bit.ly/CRA-vitals
reportWebVitals();