// Type definitions for Trading Coach app

export interface Trade {
  id: number;
  symbol: string;
  entry_price: number;
  entry_date: string;
  horizon: number;
  position_size?: number;
  stock_beta?: number;
  sector?: string;
  created_at?: string;
}

export interface TimingAnalysis {
  mfe: number;
  mae: number;
  mfe_percent: number;
  mae_percent: number;
  ideal_entry: number;
  entry_timing_score: number;
  missed_profit_potential: number;
}

export interface Anomaly {
  type: string;
  message: string;
  current_value: number;
  historical_mean: number;
  z_score: number;
}

export interface BehavioralAnalysis {
  is_anomaly: boolean;
  anomalies: Anomaly[];
  warnings: (string | {
    type: string;
    message: string;
    current_sector: string;
    known_sectors: string[];
  })[];
  metrics: {
    position_size_mean?: number;
    position_size_std?: number;
    position_size_z_score?: number;
    stock_beta_mean?: number;
    stock_beta_std?: number;
    stock_beta_z_score?: number;
  };
}

export interface TradeAnalysisResult {
  trade_id: number;
  trade: Trade;
  timing_analysis: TimingAnalysis;
  behavioral_analysis: BehavioralAnalysis;
  historical_data: HistoricalDataPoint[];
}

export interface HistoricalDataPoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface TradeFormData {
  symbol: string;
  entry_price: number;
  entry_date: string;
  horizon: 7 | 30 | 90;
  position_size: number;
  stock_beta: number;
  sector: string;
  use_mock?: boolean;
}
