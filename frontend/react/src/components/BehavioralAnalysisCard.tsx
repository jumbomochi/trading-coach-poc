import React from 'react';
import { BehavioralAnalysis } from '../types';
import './AnalysisResults.css';

interface BehavioralAnalysisProps {
  analysis: BehavioralAnalysis;
  currentTrade: {
    position_size: number;
    stock_beta: number;
    sector: string;
  };
}

const BehavioralAnalysisCard: React.FC<BehavioralAnalysisProps> = ({ analysis, currentTrade }) => {
  return (
    <div className="analysis-card">
      <h3>🧠 Behavioral Analysis</h3>

      {analysis.is_anomaly ? (
        <>
          <div className="verdict warning">
            ⚠️ <strong>ANOMALIES DETECTED</strong> - {analysis.anomalies.length} issue(s) found
          </div>

          <ul className="anomaly-list">
            {analysis.anomalies.map((anomaly, index) => (
              <li key={index} className="anomaly-item">
                <strong>{anomaly.message}</strong>
                <div className="anomaly-details">
                  Current Value: <strong>${anomaly.current_value.toLocaleString()}</strong>
                </div>
                <div className="anomaly-details">
                  Historical Mean: <strong>${anomaly.historical_mean.toLocaleString()}</strong>
                </div>
                <div className="anomaly-details">
                  Z-Score: <strong>{anomaly.z_score.toFixed(2)}σ</strong>
                </div>
                
                {anomaly.type === 'position_size' && (
                  <div className="insight" style={{ marginTop: '0.5rem' }}>
                    💡 {anomaly.z_score > 0 
                      ? 'This position is unusually large. Ensure adequate risk management.' 
                      : 'This position is unusually small. Consider if this aligns with your strategy.'}
                  </div>
                )}
                
                {anomaly.type === 'stock_beta' && (
                  <div className="insight" style={{ marginTop: '0.5rem' }}>
                    💡 {anomaly.z_score > 0 
                      ? 'This stock is significantly more volatile. Be prepared for larger price swings.' 
                      : 'This stock is less volatile. Returns may be more modest.'}
                  </div>
                )}
              </li>
            ))}
          </ul>
        </>
      ) : (
        <div className="no-anomalies">
          ✅ <strong>WITHIN NORMAL PARAMETERS</strong>
          <p style={{ marginTop: '0.5rem', marginBottom: 0 }}>
            This trade aligns with your typical trading behavior.
          </p>
        </div>
      )}

      {analysis.metrics && Object.keys(analysis.metrics).length > 0 && (
        <div className="metrics">
          <h4>Historical Comparison</h4>
          {analysis.metrics.position_size_mean && (
            <div className="metric-item">
              <span className="metric-label">Position Size:</span>
              <span className="metric-value">
                ${currentTrade.position_size.toLocaleString()} 
                (avg: ${analysis.metrics.position_size_mean.toLocaleString()})
              </span>
            </div>
          )}
          {analysis.metrics.stock_beta_mean && (
            <div className="metric-item">
              <span className="metric-label">Stock Beta:</span>
              <span className="metric-value">
                {currentTrade.stock_beta.toFixed(2)} 
                (avg: {analysis.metrics.stock_beta_mean.toFixed(2)})
              </span>
            </div>
          )}
        </div>
      )}

      {analysis.warnings && analysis.warnings.length > 0 && (
        <>
          <h4>⚡ Warnings</h4>
          <ul className="warning-list">
            {analysis.warnings.map((warning, index) => (
              <li key={index} className="warning-item">
                {typeof warning === 'string' ? (
                  warning
                ) : (
                  <>
                    🆕 {warning.message}
                    {warning.known_sectors && (
                      <div style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
                        Your typical sectors: {warning.known_sectors.join(', ')}
                      </div>
                    )}
                  </>
                )}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default BehavioralAnalysisCard;
