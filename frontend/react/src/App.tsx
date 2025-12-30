import { useState } from 'react';
import TradeForm from './components/TradeForm';
import TimingAnalysisCard from './components/TimingAnalysisCard';
import BehavioralAnalysisCard from './components/BehavioralAnalysisCard';
import { TradeFormData, TradeAnalysisResult } from './types';
import { tradeApi } from './api';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<TradeAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyzeTrade = async (formData: TradeFormData) => {
    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      // Note: Until backend API is ready, this will show mock UI
      // const result = await tradeApi.analyzeTrade(formData);
      // setAnalysisResult(result);
      
      // For now, show a message that the backend API is needed
      setError('Backend API not yet implemented. Use Streamlit dashboard for full functionality.');
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze trade');
      console.error('Error analyzing trade:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📈 Trading Coach</h1>
        <p>Analyze your trades with AI-powered insights</p>
      </header>

      <div className="app-content">
        <aside className="sidebar">
          <TradeForm onSubmit={handleAnalyzeTrade} loading={loading} />
        </aside>

        <main className="main-content">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>🔍 Analyzing trade...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <h3>❌ Error</h3>
              <p>{error}</p>
              <div className="info-box">
                <h4>💡 Available Now: Streamlit Dashboard</h4>
                <p>The full Trading Coach functionality is available in the Streamlit dashboard:</p>
                <pre>cd frontend/streamlit
streamlit run app.py</pre>
                <p>The React frontend requires a REST API backend (coming soon).</p>
              </div>
            </div>
          )}

          {analysisResult && (
            <div className="results-container">
              <div className="results-header">
                <h2>Analysis Results for {analysisResult.trade.symbol}</h2>
                <p className="trade-id">Trade #{analysisResult.trade_id}</p>
              </div>

              <div className="key-metrics">
                <div className="metric-card">
                  <div className="metric-label">Timing Score</div>
                  <div className={`metric-value ${analysisResult.timing_analysis.entry_timing_score >= 0 ? 'positive' : 'negative'}`}>
                    {analysisResult.timing_analysis.entry_timing_score.toFixed(2)}%
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Ideal Entry</div>
                  <div className="metric-value">
                    ${analysisResult.timing_analysis.ideal_entry.toFixed(2)}
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">MFE %</div>
                  <div className="metric-value positive">
                    {analysisResult.timing_analysis.mfe_percent.toFixed(2)}%
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">MAE %</div>
                  <div className="metric-value negative">
                    {analysisResult.timing_analysis.mae_percent.toFixed(2)}%
                  </div>
                </div>
              </div>

              <TimingAnalysisCard 
                analysis={analysisResult.timing_analysis}
                entryPrice={analysisResult.trade.entry_price}
              />

              <BehavioralAnalysisCard
                analysis={analysisResult.behavioral_analysis}
                currentTrade={{
                  position_size: analysisResult.trade.position_size || 0,
                  stock_beta: analysisResult.trade.stock_beta || 1.0,
                  sector: analysisResult.trade.sector || 'Unknown',
                }}
              />
            </div>
          )}

          {!loading && !error && !analysisResult && (
            <div className="empty-state">
              <div className="empty-state-icon">📊</div>
              <h3>Ready to Analyze</h3>
              <p>Fill out the form on the left and click "Analyze Trade" to get started.</p>
              
              <div className="info-box">
                <h4>🚀 Two Ways to Use Trading Coach</h4>
                
                <div className="option">
                  <h5>1. Streamlit Dashboard (Recommended)</h5>
                  <p>✅ Fully functional with real-time analysis<br/>
                     ✅ Candlestick charts with entry markers<br/>
                     ✅ Tiger API and mock data support</p>
                  <pre>cd frontend/streamlit
streamlit run app.py</pre>
                </div>

                <div className="option">
                  <h5>2. React Frontend (In Development)</h5>
                  <p>⚠️ Requires REST API backend<br/>
                     🚧 Modern UI components ready<br/>
                     🔜 API integration coming soon</p>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
