import React, { useState } from 'react';
import EmbedSection from './components/EmbedSection';
import ExtractSection from './components/ExtractSection';
import './index.css';

const App = () => {
  const [activeTab, setActiveTab] = useState('embed');

  return (
    <div className="container">
      <header>
        <h1>Secure Data Hiding</h1>
        <p>Hide secret messages in newly created pixels during image resizing.</p>
      </header>

      <div className="tabs">
        <button 
          className={`tab-btn ${activeTab === 'embed' ? 'active' : ''}`}
          onClick={() => setActiveTab('embed')}
        >
          Hide Message (Embed)
        </button>
        <button 
          className={`tab-btn ${activeTab === 'extract' ? 'active' : ''}`}
          onClick={() => setActiveTab('extract')}
        >
          Recover Message (Extract)
        </button>
      </div>

      <main>
        {activeTab === 'embed' ? (
          <div className="content-wrapper">
            <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Step 1: Embed your secret</h2>
            <EmbedSection />
          </div>
        ) : (
          <div className="content-wrapper">
            <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Step 2: Recover your secret</h2>
            <ExtractSection />
          </div>
        )}
      </main>

      <footer style={{ marginTop: '5rem', textAlign: 'center', color: 'var(--text-dim)', fontSize: '0.9rem' }}>
        <p>© 2026 Image Vision Project | Powered by Prediction Error Expansion & XOR Encryption</p>
      </footer>
    </div>
  );
};

export default App;
