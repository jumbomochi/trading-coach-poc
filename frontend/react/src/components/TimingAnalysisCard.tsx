import React from 'react';
import { TimingAnalysis } from '../types';
import './AnalysisResults.css';

interface TimingAnalysisProps {
  analysis: TimingAnalysis;
  entryPrice: number;
}

const TimingAnalysisCard: React.FC<TimingAnalysisProps> = ({ analysis, entryPrice }) => {
  const getVerdict = (score: number) => {
    if (score >= 0) return { text: 'EXCELLENT', color: 'success', emoji: '✅' };
    if (score >= -5) return { text: 'GOOD', color: 'info', emoji: 'ℹ️' };
    if (score >= -10) return { text: 'FAIR', color: 'warning', emoji: '⚠️' };
    return { text: 'POOR', color: 'error', emoji: '❌' };
  };

  const verdict = getVerdict(analysis.entry_timing_score);

  return (
    <div className="analysis-card">
      <h3>⏱️ Timing Analysis</h3>
      
      <div className={`verdict ${verdict.color}`}>
        {verdict.emoji} <strong>{verdict.text}</strong>
      </div>

      <div className="metrics">
        <div className="metric-item">
          <span className="metric-label">Actual Entry:</span>
          <span className="metric-value">${entryPrice.toFixed(2)}</span>
        </div>
        
        <div className="metric-item">
          <span className="metric-label">Ideal Entry:</span>
          <span className="metric-value">${analysis.ideal_entry.toFixed(2)}</span>
        </div>
        
        <div className="metric-item">
          <span className="metric-label">Difference:</span>
          <span className="metric-value">
            ${(entryPrice - analysis.ideal_entry).toFixed(2)}
          </span>
        </div>
        
        <div className="metric-item">
          <span className="metric-label">Entry Timing Score:</span>
          <span className={`metric-value ${analysis.entry_timing_score >= 0 ? 'positive' : 'negative'}`}>
            {analysis.entry_timing_score.toFixed(2)}%
          </span>
        </div>
        
        <div className="metric-item">
          <span className="metric-label">MFE (Max Profit):</span>
          <span className="metric-value positive">
            ${analysis.mfe.toFixed(2)} (+{analysis.mfe_percent.toFixed(2)}%)
          </span>
        </div>
        
        <div className="metric-item">
          <span className="metric-label">MAE (Max Drawdown):</span>
          <span className="metric-value negative">
            ${analysis.mae.toFixed(2)} ({analysis.mae_percent.toFixed(2)}%)
          </span>
        </div>
        
        <div className="metric-item">
          <span className="metric-label">Missed Profit Potential:</span>
          <span className="metric-value">
            {analysis.missed_profit_potential.toFixed(2)}%
          </span>
        </div>
      </div>

      {analysis.entry_timing_score < 0 && (
        <div className="insight">
          <p>
            💡 You entered <strong>{Math.abs(analysis.entry_timing_score).toFixed(2)}%</strong> above 
            the ideal entry price. Consider waiting for better entry points.
          </p>
        </div>
      )}
      
      {analysis.entry_timing_score >= 0 && (
        <div className="insight success">
          <p>
            ✨ Great timing! You entered at or below the ideal price. This maximizes your profit potential.
          </p>
        </div>
      )}
    </div>
  );
};

export default TimingAnalysisCard;
