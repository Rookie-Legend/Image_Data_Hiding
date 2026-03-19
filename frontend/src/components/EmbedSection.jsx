import React, { useState } from 'react';
import { embedImage } from '../utils/api';

const EmbedSection = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [secret, setSecret] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !secret) return;

    setLoading(true);
    setError(null);
    try {
      const { blob, key } = await embedImage(file, secret);
      const url = URL.createObjectURL(blob);
      setResult({ url, key });
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
          <label>Source Image</label>
          <div 
            className="dropzone"
            onClick={() => document.getElementById('fileInput').click()}
          >
            {preview ? (
              <img src={preview} alt="Preview" className="preview-img" />
            ) : (
              <p>Click or drag to upload image</p>
            )}
            <input 
              id="fileInput"
              type="file" 
              hidden 
              accept="image/*"
              onChange={handleFileChange}
            />
          </div>
        </div>

        <div className="form-group">
          <label>Secret Message</label>
          <textarea 
            placeholder="Enter the message you want to hide..."
            rows="4"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
            required
          />
        </div>

        <button 
          type="submit" 
          className="btn-primary"
          disabled={loading || !file || !secret}
        >
          {loading ? 'Embedding...' : 'Embed Secret Data'}
        </button>
      </form>

      {error && <p style={{ color: 'var(--error)', marginTop: '1rem' }}>{error}</p>}

      {result && (
        <div className="result-card">
          <h3 style={{ color: 'var(--success)', marginBottom: '1rem' }}>🎉 Success!</h3>
          <p>Message embedded successfully into the new pixels.</p>
          
          <div style={{ marginTop: '1.5rem' }}>
            <label>1. Download Stego Image</label>
            <a 
              href={result.url} 
              download={`stego_${file?.name || 'image.png'}`}
              className="btn-primary"
              style={{ display: 'block', textAlign: 'center', textDecoration: 'none', background: 'var(--success)', marginTop: '0.5rem' }}
            >
              Download Stego
            </a>
          </div>

          <div style={{ marginTop: '1.5rem' }}>
            <label>2. Copy Secure Key String (Required for Extraction)</label>
            <div className="key-box">
              {result.key}
            </div>
            <button 
              className="tab-btn" 
              style={{ marginTop: '0.5rem', width: '100%', fontSize: '0.9rem' }}
              onClick={() => {
                navigator.clipboard.writeText(result.key);
                alert('Key copied to clipboard!');
              }}
            >
              Copy Key
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmbedSection;
