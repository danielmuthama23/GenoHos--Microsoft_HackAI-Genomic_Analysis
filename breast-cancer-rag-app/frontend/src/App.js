import React from 'react';
import QueryInterface from './components/QueryInterface';
import './styles.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Biospecimen RAG Interface</h1>
      </header>
      <main>
        <QueryInterface />
      </main>
      <footer className="app-footer">
        <p>© {new Date().getFullYear()} Genomic Analysis Platform</p>
      </footer>
    </div>
  );
}

export default App;