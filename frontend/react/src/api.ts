import axios from 'axios';
import { Trade, TradeAnalysisResult, TradeFormData } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const tradeApi = {
  // Analyze a new trade
  analyzeTrade: async (data: TradeFormData): Promise<TradeAnalysisResult> => {
    const response = await api.post('/trades/analyze', data);
    return response.data;
  },

  // Get recent trades
  getRecentTrades: async (limit: number = 5): Promise<Trade[]> => {
    const response = await api.get(`/trades/recent?limit=${limit}`);
    return response.data;
  },

  // Get a specific trade by ID
  getTrade: async (tradeId: number): Promise<Trade> => {
    const response = await api.get(`/trades/${tradeId}`);
    return response.data;
  },

  // Get analysis for a specific trade
  getTradeAnalysis: async (tradeId: number): Promise<TradeAnalysisResult> => {
    const response = await api.get(`/trades/${tradeId}/analysis`);
    return response.data;
  },
};

export default api;
