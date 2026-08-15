import { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [timePeriod, setTimePeriod] = useState('not specified')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Progress tracker state for active agents
  const [progress, setProgress] = useState({
    analyzing: 'waiting',  // waiting, active, completed
    researching: 'waiting',
    verifying: 'waiting',
    writing: 'waiting'
  })
  const [currentMessage, setCurrentMessage] = useState('')

  // Final report results state
  const [report, setReport] = useState(null)
  const [expandedSubClaim, setExpandedSubClaim] = useState(null)

  // Suggestion list
  const suggestions = [
    {
      query: "Did the Tamil Nadu Government announced daily PT period for school students",
      timePeriod: "August 2026",
      label: "Sports for govt school students"
    },
    {
      query: "Did the government cancelled 100 units of free electricity to users who use more than 500 units bi-monthly?",
      timePeriod: "May 2026 onwards",
      label: "100 units of free electricity"
    },
    {
      query: "Did the TVK Government cancelled the Kalaignar Magalir Urimai Thogai Thittam giving Rs 1,000 monthly to women?",
      timePeriod: "May 2026 onwards",
      label: "Magalir Urimai Thogai Scheme"
    }
  ]

  const handleSuggestionClick = (sug) => {
    setQuery(sug.query)
    setTimePeriod(sug.timePeriod)
  }

  const handleFactCheck = (e) => {
    if (e) e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError(null)
    setReport(null)
    setExpandedSubClaim(null)
    setProgress({
      analyzing: 'active',
      researching: 'waiting',
      verifying: 'waiting',
      writing: 'waiting'
    })
    setCurrentMessage('Connecting to TN Fact Check AI Desk...')

    const userQueryEscaped = encodeURIComponent(query)
    const timePeriodEscaped = encodeURIComponent(timePeriod)

    // Create EventSource to listen to Server-Sent Events (SSE)
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
    const url = `${apiBaseUrl}/api/fact-check-stream?user_query=${userQueryEscaped}&time_period=${timePeriodEscaped}`
    const eventSource = new EventSource(url)

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.status === "analyzing") {
          setProgress({
            analyzing: 'active',
            researching: 'waiting',
            verifying: 'waiting',
            writing: 'waiting'
          })
          setCurrentMessage(data.message)
        } else if (data.status === "researching") {
          setProgress({
            analyzing: 'completed',
            researching: 'active',
            verifying: 'waiting',
            writing: 'waiting'
          })
          setCurrentMessage(data.message)
        } else if (data.status === "verifying") {
          setProgress({
            analyzing: 'completed',
            researching: 'completed',
            verifying: 'active',
            writing: 'waiting'
          })
          setCurrentMessage(data.message)
        } else if (data.status === "writing") {
          setProgress({
            analyzing: 'completed',
            researching: 'completed',
            verifying: 'completed',
            writing: 'active'
          })
          setCurrentMessage(data.message)
        } else if (data.status === "completed") {
          setProgress({
            analyzing: 'completed',
            researching: 'completed',
            verifying: 'completed',
            writing: 'completed'
          })
          setCurrentMessage('Verification report generated successfully!')
          setReport(data.result)
          setLoading(false)
          eventSource.close()
        } else if (data.status === "error") {
          setError(data.message || 'An error occurred during agent verification.')
          setLoading(false)
          eventSource.close()
        }
      } catch (err) {
        console.error("Error parsing stream message:", err)
      }
    }

    eventSource.onerror = (err) => {
      console.error("EventSource failed:", err)
      setError("Unable to connect to the fact-checking service. Please verify the backend is running.")
      setLoading(false)
      eventSource.close()
    }
  }

  // Get color gradient & class for overall verdict
  const getVerdictStyle = (verdict) => {
    const v = (verdict || '').toUpperCase()
    if (v.includes('TRUE')) return { gradient: 'verdict-gradient-true', label: 'True / மெய்' }
    if (v.includes('FALSE')) return { gradient: 'verdict-gradient-false', label: 'False / பொய்' }
    if (v.includes('MISLEADING')) return { gradient: 'verdict-gradient-misleading', label: 'Misleading / திசைதிருப்பல்' }
    return { gradient: 'verdict-gradient-unverified', label: verdict || 'Unverified / சரிபார்க்கப்படவில்லை' }
  }

  // Get sub-claim status badge style class
  const getSubClaimBadgeClass = (status) => {
    const s = (status || '').toUpperCase()
    if (s.includes('VERIFIED') && !s.includes('PARTIALLY')) return 'badge-verified'
    if (s.includes('PARTIALLY')) return 'badge-partially'
    if (s.includes('FALSE')) return 'badge-false'
    if (s.includes('OUTDATED')) return 'badge-outdated'
    return 'badge-unverified'
  }

  return (
    <div className="app-container">
      {/* Tamil Nadu Govt Header */}
      <header className="gov-header">
        <div className="header-brand">
          <div className="emblem-placeholder">
            <img src="/assets/logo.jpeg" alt="TN Govt Fact Check Logo" className="emblem-img" />
          </div>
          <div className="brand-text">
            <h1>TAMIL NADU FACT CHECK AI</h1>
            <p>AI, Information Technology and Digital Services Dept • Government of Tamil Nadu</p>
          </div>
        </div>

        <div className="header-badge">
          <div className="badge-dot"></div>
          <span>Active Agent Desk</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="chat-main">
        {/* Suggestion & Welcome panel (visible when not loading and no report yet) */}
        {!loading && !report && (
          <div className="welcome-card">
            <h2>Verify News & Social Media Claims</h2>
            <p>
              Submit any public claim, rumor, news article, or historical myth concerning
              Tamil Nadu. Our multi-agent AI verification desk will analyze the query, research the web,
              cross-reference official government databases, and compile a structured report.
            </p>
            <div className="suggestion-grid">
              {suggestions.map((sug, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestionClick(sug)}
                  className="suggestion-btn"
                >
                  <span className="suggestion-tag">{sug.label}</span>
                  <span>"{sug.query}"</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Form */}
        <div className="input-card">
          <form onSubmit={handleFactCheck}>
            <div className="form-group">
              <label htmlFor="claim-input">Claim / News to Verify</label>
              <textarea
                id="claim-input"
                className="text-area-input"
                placeholder="Paste the claim, news post, WhatsApp message or question here..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="context-input">Target Time Period / Context (Optional)</label>
                <input
                  id="context-input"
                  type="text"
                  className="select-input"
                  placeholder="e.g. August 2026, Current week, Year 2024, or leave empty"
                  value={timePeriod}
                  onChange={(e) => setTimePeriod(e.target.value)}
                  disabled={loading}
                />
              </div>

              <div className="form-group" style={{ justifyContent: 'flex-end' }}>
                <button
                  type="submit"
                  className="submit-btn"
                  disabled={loading || !query.trim()}
                >
                  {loading ? (
                    <>
                      <div className="step-spinner"></div>
                      <span>Verifying...</span>
                    </>
                  ) : (
                    <span>Initiate Verification</span>
                  )}
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* Stepper Widget (Visible during loading) */}
        {loading && (
          <div className="stepper-card">
            <div className="stepper-title">
              <h3>
                <div className="step-spinner"></div>
                <span>Executing Multi-Agent Fact Checking Pipeline</span>
              </h3>
              <span className="current-toast-msg" style={{ fontSize: '0.85rem', color: '#64748b' }}>
                {currentMessage}
              </span>
            </div>

            <div className="stepper-steps">
              <div className={`step-item ${progress.analyzing}`}>
                <div className="step-indicator">
                  {progress.analyzing === 'completed' ? '✓' : '1'}
                </div>
                <div className="step-content">
                  <h4>Fact-Check Query Analyzer (Desk Editor)</h4>
                  <p>Triaging query, identifying entities involved, and classifying era (Historical vs Current).</p>
                </div>
              </div>

              <div className={`step-item ${progress.researching}`}>
                <div className="step-indicator">
                  {progress.researching === 'completed' ? '✓' : '2'}
                </div>
                <div className="step-content">
                  <h4>Research Investigator (News Researcher)</h4>
                  <p>Searching primary documents, public archives, and search databases for evidence.</p>
                </div>
              </div>

              <div className={`step-item ${progress.verifying}`}>
                <div className="step-indicator">
                  {progress.verifying === 'completed' ? '✓' : '3'}
                </div>
                <div className="step-content">
                  <h4>Fact Verification Specialist (Verification Desk)</h4>
                  <p>Cross-checking claims, checking publish dates, and rating source reliability.</p>
                </div>
              </div>

              <div className={`step-item ${progress.writing}`}>
                <div className="step-indicator">
                  {progress.writing === 'completed' ? '✓' : '4'}
                </div>
                <div className="step-content">
                  <h4>Fact-Check Report Writer (Chief Editor)</h4>
                  <p>Formulating overall verdict, writing summary, and cataloging source citations.</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="welcome-card" style={{ borderColor: '#fca3a5', backgroundColor: '#fef2f2' }}>
            <h3 style={{ color: '#991b1b', margin: 0 }}>Verification Failed</h3>
            <p style={{ color: '#7f1d1d', marginTop: '0.5rem' }}>{error}</p>
            <button
              onClick={() => setLoading(false) || setError(null)}
              className="source-pill-link"
              style={{ marginTop: '0.5rem', backgroundColor: '#fee2e2', border: '1px solid #fca5a5' }}
            >
              Retry
            </button>
          </div>
        )}

        {/* Verification Report Card */}
        {report && (
          <div className="result-card">
            {/* Header with verdict color */}
            <div className={`result-header ${getVerdictStyle(report.overall_verdict).gradient}`}>
              <span className="verdict-badge">
                {getVerdictStyle(report.overall_verdict).label}
              </span>
              <h2>{report.user_query}</h2>
            </div>

            {/* Meta Information */}
            <div className="meta-info-bar">
              <div className="meta-item">
                <span>Confidence:</span>
                <strong className={`reliability-badge ${report.confidence?.toLowerCase()}`} style={{ padding: '0.1rem 0.5rem', borderRadius: '4px' }}>
                  {report.confidence || 'Medium'}
                </strong>
              </div>
              <div className="meta-item">
                <span>Classification:</span>
                <span className={`meta-tag ${report.is_historical ? 'historical' : 'current'}`}>
                  {report.is_historical ? 'Historical Claim' : 'Current News'}
                </span>
              </div>
              <div className="meta-item">
                <span>Time Window Grounding:</span>
                <strong>{report.time_window_used || 'as of latest date'}</strong>
              </div>
              <div className="meta-item" style={{ marginLeft: 'auto' }}>
                <span>Verified On:</span>
                <strong>{report.report_generated_on || new Date().toLocaleDateString('en-IN')}</strong>
              </div>
            </div>

            {/* Executive Summary */}
            <div className="summary-section">
              <h3>Executive Summary / சுருக்கம்</h3>
              <div className="summary-text">
                {report.executive_summary}
              </div>
            </div>

            {/* Subclaims Accordion */}
            {report.sub_claims && report.sub_claims.length > 0 && (
              <div className="subclaims-section">
                <h3>Sub-Claims Verification Breakdown</h3>
                <div className="subclaims-list">
                  {report.sub_claims.map((sub, idx) => {
                    const isExpanded = expandedSubClaim === idx
                    return (
                      <div key={idx} className="subclaim-item">
                        <div
                          className="subclaim-header"
                          style={{ cursor: 'pointer' }}
                          onClick={() => setExpandedSubClaim(isExpanded ? null : idx)}
                        >
                          <span>{idx + 1}. {sub.sub_claim}</span>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <span className={`subclaim-status-badge ${getSubClaimBadgeClass(sub.status)}`}>
                              {sub.status}
                            </span>
                            <span>{isExpanded ? '▲' : '▼'}</span>
                          </div>
                        </div>

                        {isExpanded && (
                          <div className="subclaim-body">
                            <div className="subclaim-explanation">
                              <strong>Explanation: </strong>
                              {sub.explanation}
                            </div>
                            {sub.sources && sub.sources.length > 0 && (
                              <div>
                                <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#4b5563', marginBottom: '0.25rem' }}>
                                  Evidence Supporting Status:
                                </div>
                                <div className="subclaim-sources">
                                  {sub.sources.map((src, sidx) => (
                                    <a
                                      key={sidx}
                                      href={src.url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="source-pill-link"
                                      title={src.title}
                                    >
                                      <span>🔗 {src.publisher || 'Source'}</span>
                                      <span className={`reliability-badge ${src.reliability?.toLowerCase()}`} style={{ fontSize: '0.65rem', padding: '0 0.3rem', borderRadius: '2px' }}>
                                        {src.reliability}
                                      </span>
                                    </a>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* General Citations Directory */}
            {report.all_sources && report.all_sources.length > 0 && (
              <div className="sources-section">
                <h3>Deduplicated Source Reference Directory</h3>
                <div className="sources-list">
                  {report.all_sources.slice(0, 5).map((src, idx) => (
                    <div key={idx} className="minimal-source-row">
                      <div className="source-main-info">
                        <span className="source-index">{idx + 1}</span>
                        <a
                          href={src.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="source-link-text"
                        >
                          {src.title || 'Source Reference'}
                        </a>
                      </div>

                      <div className="source-meta-row">
                        <span className="source-meta-badge">{src.publisher}</span>
                        {src.published_date && src.published_date !== 'unknown' && (
                          <span className="source-meta-badge">📅 {src.published_date}</span>
                        )}
                        <span className={`source-meta-badge reliability-badge ${src.reliability?.toLowerCase()}`}>
                          {src.reliability} Reliability
                        </span>
                        {src.supports && (
                          <span className="source-meta-badge" style={{ backgroundColor: src.supports.toLowerCase().includes('confirm') ? '#d1fae5' : '#fee2e2', color: src.supports.toLowerCase().includes('confirm') ? '#065f46' : '#991b1b' }}>
                            {src.supports}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Tamil Nadu Govt Footer */}
      <footer className="gov-footer">
        <div className="footer-content">
          <div className="footer-top">
            <div>
              <h3 style={{ color: '#ffffff', margin: 0, fontSize: '1.2rem' }}>TN Fact Check AI</h3>
              <p style={{ color: '#6ee7b7', margin: '0.25rem 0 0', fontSize: '0.8rem' }}>An Initiative to Counter Disinformation and Fake News</p>
            </div>

            <div className="footer-links">
              <a href="https://www.tn.gov.in/" target="_blank" rel="noopener noreferrer">Government Portal</a>
              <a href="mailto:harish.ai.engineer@gmail.com">Contact Developer</a>
            </div>

            <div className="footer-attribution" style={{ color: '#94a3b8', fontSize: '0.85rem', fontWeight: 500 }}>
              Developed by Harish R, AI&DS student, MIT Campus, Anna University
            </div>
          </div>

          <div className="footer-bottom">
            <p>© {new Date().getFullYear()} AI, Information Technology and Digital Services Department, Government of Tamil Nadu. All Rights Reserved.</p>
            <p style={{ opacity: 0.6 }}>AI-powered fact verification system.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
