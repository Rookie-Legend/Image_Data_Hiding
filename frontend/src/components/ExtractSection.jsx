import React, { useState } from 'react';
import { extractMessage } from '../utils/api';

const ExtractSection = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [key, setKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [recoveredMessage, setRecoveredMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setRecoveredMessage(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !key) return;

    setLoading(true);
    setError(null);
    try {
      const { recovered_message } = await extractMessage(file, key);
      setRecoveredMessage(recovered_message);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Stego Image</label>
          <div 
            className="dropzone"
            onClick={() => document.getElementById('extractFileInput').click()}
          >
            {preview ? (
              <img src={preview} alt="Preview" className="preview-img" />
            ) : (
              <p>Upload the image containing hidden data</p>
            )}
            <input 
              id="extractFileInput"
              type="file" 
              hidden 
              accept="image/*"
              onChange={handleFileChange}
            />
          </div>
        </div>

        <div className="form-group">
          <label>Secret Key String</label>
          <textarea 
            placeholder="Paste the secure key string you received during embedding..."
            rows="3"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            required
          />
        </div>

        <button 
          type="submit" 
          className="btn-primary"
          disabled={loading || !file || !key}
          style={{ background: 'linear-gradient(to right, var(--accent), #ff5e62)' }}
        >
          {loading ? 'Extracting...' : 'Decrypt & Extract Message'}
        </button>
      </form>

      {error && <p style={{ color: 'var(--error)', marginTop: '1rem' }}>{error}</p>}

      {recoveredMessage && (
        <div className="result-card" style={{ background: 'rgba(188, 78, 156, 0.1)', border: '1px solid var(--accent)' }}>
          <h3 style={{ color: 'var(--accent)', marginBottom: '1rem' }}>🕵️ Message Recovered!</h3>
          <p>The original message was:</p>
          <div className="key-box" style={{ background: 'rgba(255, 255, 255, 0.05)', fontSize: '1.2rem', fontWeight: 'bold' }}>
            {recoveredMessage}
          </div>
        </div>
      )}
    </div>
  );
};

export default ExtractSection;
