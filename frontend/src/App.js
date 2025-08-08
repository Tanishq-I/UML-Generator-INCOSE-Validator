import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import { graphviz } from 'd3-graphviz';

const UML_TYPES = [
  { value: 'class', label: 'Class Diagram' },
  { value: 'object', label: 'Object Diagram' },
  { value: 'composite', label: 'Composite Structure Diagram' },
  { value: 'sequence', label: 'Sequence Diagram' },
  { value: 'usecase', label: 'Use Case Diagram' }
];

const DEFAULT_MODELS = [
  { id: "llama3-8b-8192", name: "LLAMA3 8B", description: "Fast and efficient 8B parameter model" },
  { id: "llama3-70b-8192", name: "LLAMA3 70B", description: "More powerful 70B parameter model" },
  { id: "mixtral-8x7b-32768", name: "Mixtral 8x7B", description: "Mixture of experts model with 32k context" },
  { id: "gemma-7b-it", name: "Gemma 7B", description: "Google's Gemma 7B instruction-tuned model" },
  { id: "gemma2-9b-it", name: "Gemma 2 9B", description: "Latest Gemma 2 9B instruction-tuned model" }
];

// Login Component
function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    if (username === "admin" && password === "admin") {
      onLogin();
      setError("");
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Login to UML Generator & Requirement Validator</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [scenario, setScenario] = useState("");
  const [umlType, setUmlType] = useState(UML_TYPES[0].value);
  const [selectedModel, setSelectedModel] = useState("llama3-8b-8192");
  const [availableModels, setAvailableModels] = useState(DEFAULT_MODELS);
  const [umlResult, setUmlResult] = useState(null);
  const [umlLoading, setUmlLoading] = useState(false);
  const [umlError, setUmlError] = useState("");

  const [requirement, setRequirement] = useState("");
  const [reqSelectedModel, setReqSelectedModel] = useState("llama3-8b-8192");
  const [reqResult, setReqResult] = useState(null);
  const [reqLoading, setReqLoading] = useState(false);
  const [reqError, setReqError] = useState("");

  const diagramRef = useRef(null);

  useEffect(() => {
    if (umlResult && umlResult.dot_source && diagramRef.current) {
      graphviz(diagramRef.current).renderDot(umlResult.dot_source);
    }
  }, [umlResult]);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const res = await fetch("http://localhost:8000/models");
        if (res.ok) {
          const data = await res.json();
          setAvailableModels(data.models);
        }
      } catch (err) {
        console.error("Error fetching models:", err);
      }
    };
    fetchModels();
  }, []);

  const handleUmlSubmit = async (e) => {
    e.preventDefault();
    setUmlLoading(true);
    setUmlError("");
    setUmlResult(null);
    try {
      const res = await fetch("http://localhost:8000/generate-uml", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          scenario, 
          uml_type: umlType,
          model: selectedModel
        }),
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Error generating UML");
      const data = await res.json();
      setUmlResult(data);
    } catch (err) {
      setUmlError(err.message);
    } finally {
      setUmlLoading(false);
    }
  };

  const handleReqSubmit = async (e) => {
    e.preventDefault();
    setReqLoading(true);
    setReqError("");
    setReqResult(null);
    try {
      const res = await fetch("http://localhost:8000/evaluate-requirement", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          requirement,
          model: reqSelectedModel
        }),
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Error evaluating requirement");
      const data = await res.json();
      setReqResult(data);
    } catch (err) {
      setReqError(err.message);
    } finally {
      setReqLoading(false);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  // Show login page if not logged in
  if (!isLoggedIn) {
    return <LoginPage onLogin={() => setIsLoggedIn(true)} />;
  }

  return (
    <div className="App">
      <div className="header">
        <h1>UML Generator & Requirement Validator</h1>
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      </div>
      <div className="feature-container">
        <div className="feature-box">
          <h2>UML Diagram Generator</h2>
          <form onSubmit={handleUmlSubmit}>
            <label htmlFor="uml-type-select"><b>Diagram Type:</b></label>
            <select
              id="uml-type-select"
              value={umlType}
              onChange={e => setUmlType(e.target.value)}
              style={{ marginBottom: '1rem', marginLeft: '0.5rem' }}
            >
              {UML_TYPES.map(type => (
                <option key={type.value} value={type.value}>{type.label}</option>
              ))}
            </select>
            <br />
            <label htmlFor="uml-model-select"><b>AI Model:</b></label>
            <select
              id="uml-model-select"
              value={selectedModel}
              onChange={e => setSelectedModel(e.target.value)}
              style={{ marginBottom: '1rem', marginLeft: '0.5rem' }}
            >
              {availableModels.map(model => (
                <option key={model.id} value={model.id} title={model.description}>
                  {model.name}
                </option>
              ))}
            </select>
            <br />
            <textarea
              value={scenario}
              onChange={e => setScenario(e.target.value)}
              placeholder="Describe your system or scenario..."
              rows={5}
              style={{ width: '100%' }}
            />
            <br />
            <button type="submit" disabled={umlLoading}>Generate UML</button>
          </form>
          {umlLoading && <p>Generating UML...</p>}
          {umlError && <p style={{ color: 'red' }}>{umlError}</p>}
          {umlResult && (
            <div className="uml-result">
              {umlResult.error && <p style={{ color: 'red' }}>{umlResult.error}</p>}
              <div>
                <h4>Visual Diagram:</h4>
                <div ref={diagramRef} style={{ width: '100%', minHeight: 300, background: '#fff', border: '1px solid #b0c4de', borderRadius: 8, marginTop: 10, overflow: 'auto' }} />
              </div>
            </div>
          )}
        </div>
        
        <div className="feature-box">
          <h2>Requirement Validator (INCOSE)</h2>
          <form onSubmit={handleReqSubmit}>
            <label htmlFor="req-model-select"><b>AI Model:</b></label>
            <select
              id="req-model-select"
              value={reqSelectedModel}
              onChange={e => setReqSelectedModel(e.target.value)}
              style={{ marginBottom: '1rem', marginLeft: '0.5rem' }}
            >
              {availableModels.map(model => (
                <option key={model.id} value={model.id} title={model.description}>
                  {model.name}
                </option>
              ))}
            </select>
            <br />
            <textarea
              value={requirement}
              onChange={e => setRequirement(e.target.value)}
              placeholder="Enter a system requirement to validate against INCOSE standards..."
              rows={4}
              style={{ width: '100%' }}
            />
            <br />
            <button type="submit" disabled={reqLoading}>Validate Requirement</button>
          </form>
          {reqLoading && <p>Evaluating requirement...</p>}
          {reqError && <p style={{ color: 'red' }}>{reqError}</p>}
          {reqResult && (
            <div className="req-result">
              <div style={{ 
                padding: '15px', 
                border: reqResult.result === 'VALID' ? '2px solid #4CAF50' : '2px solid #f44336',
                borderRadius: '8px',
                backgroundColor: reqResult.result === 'VALID' ? '#e8f5e8' : '#ffebee',
                marginTop: '10px'
              }}>
                <h4 style={{ 
                  margin: '0 0 10px 0', 
                  color: reqResult.result === 'VALID' ? '#2e7d32' : '#c62828' 
                }}>
                  {reqResult.result === 'VALID' ? '✓ Valid Requirement' : '✗ Invalid Requirement'}
                </h4>
                
                <div style={{ marginTop: '15px' }}>
                  <h5 style={{ margin: '0 0 5px 0', color: '#666' }}>Analysis:</h5>
                  <div style={{ 
                    backgroundColor: '#f5f5f5', 
                    padding: '10px', 
                    borderRadius: '4px',
                    fontSize: '14px',
                    lineHeight: '1.4',
                    whiteSpace: 'pre-wrap'
                  }}>
                    {reqResult.reason}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
