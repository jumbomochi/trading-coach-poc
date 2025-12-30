import React, { useState } from 'react';
import { TradeFormData } from '../types';
import './TradeForm.css';

interface TradeFormProps {
  onSubmit: (data: TradeFormData) => void;
  loading?: boolean;
}

const TradeForm: React.FC<TradeFormProps> = ({ onSubmit, loading = false }) => {
  const [formData, setFormData] = useState<TradeFormData>({
    symbol: 'AAPL',
    entry_price: 150.0,
    entry_date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    horizon: 7,
    position_size: 10000,
    stock_beta: 1.2,
    sector: 'Technology',
    use_mock: false,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else if (type === 'number') {
      setFormData(prev => ({ ...prev, [name]: parseFloat(value) || 0 }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form className="trade-form" onSubmit={handleSubmit}>
      <h2>🔧 Log New Trade</h2>
      
      <div className="form-section">
        <h3>Trade Details</h3>
        
        <div className="form-group">
          <label htmlFor="symbol">Ticker Symbol</label>
          <input
            type="text"
            id="symbol"
            name="symbol"
            value={formData.symbol}
            onChange={handleChange}
            placeholder="e.g., AAPL, TSLA"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="entry_price">Entry Price ($)</label>
          <input
            type="number"
            id="entry_price"
            name="entry_price"
            value={formData.entry_price}
            onChange={handleChange}
            step="0.01"
            min="0.01"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="entry_date">Entry Date</label>
          <input
            type="date"
            id="entry_date"
            name="entry_date"
            value={formData.entry_date}
            onChange={handleChange}
            max={new Date().toISOString().split('T')[0]}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="horizon">Horizon (days)</label>
          <select
            id="horizon"
            name="horizon"
            value={formData.horizon}
            onChange={handleChange}
            required
          >
            <option value={7}>7 days</option>
            <option value={30}>30 days</option>
            <option value={90}>90 days</option>
          </select>
        </div>
      </div>

      <div className="form-section">
        <h3>Position Details</h3>
        
        <div className="form-group">
          <label htmlFor="position_size">Position Size ($)</label>
          <input
            type="number"
            id="position_size"
            name="position_size"
            value={formData.position_size}
            onChange={handleChange}
            step="100"
            min="0"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="stock_beta">Stock Beta</label>
          <input
            type="number"
            id="stock_beta"
            name="stock_beta"
            value={formData.stock_beta}
            onChange={handleChange}
            step="0.1"
            min="0"
            max="5"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="sector">Sector</label>
          <input
            type="text"
            id="sector"
            name="sector"
            value={formData.sector}
            onChange={handleChange}
            placeholder="e.g., Technology, Healthcare"
            required
          />
        </div>
      </div>

      <div className="form-section">
        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="use_mock"
              checked={formData.use_mock}
              onChange={handleChange}
            />
            <span>Use Mock Data (for testing)</span>
          </label>
        </div>
      </div>

      <button type="submit" className="submit-button" disabled={loading}>
        {loading ? '🔄 Analyzing...' : '🚀 Analyze Trade'}
      </button>
    </form>
  );
};

export default TradeForm;
