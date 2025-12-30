"""Mock data generator for testing Trading Coach without Tiger API"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_mock_historical_data(symbol: str, horizon_days: int, base_price: float = 150.0) -> pd.DataFrame:
    """
    Generate realistic mock historical stock data for testing.
    
    Args:
        symbol: Stock symbol (not used, for compatibility)
        horizon_days: Number of days of data to generate
        base_price: Starting price for the stock
        
    Returns:
        pandas.DataFrame with columns: date, open, high, low, close, volume
    """
    np.random.seed(hash(symbol) % 2**32)  # Consistent data per symbol
    
    dates = []
    data = []
    
    current_price = base_price
    current_date = datetime.now() - timedelta(days=horizon_days)
    
    for i in range(horizon_days):
        # Skip weekends
        if current_date.weekday() >= 5:  # Saturday or Sunday
            current_date += timedelta(days=1)
            continue
        
        # Generate realistic price movements
        daily_return = np.random.normal(0.001, 0.02)  # 0.1% mean return, 2% volatility
        current_price = current_price * (1 + daily_return)
        
        # Generate OHLC data
        daily_volatility = current_price * 0.015  # 1.5% intraday range
        
        open_price = current_price + np.random.normal(0, daily_volatility * 0.5)
        close_price = current_price + np.random.normal(0, daily_volatility * 0.5)
        
        high_price = max(open_price, close_price) + abs(np.random.normal(0, daily_volatility * 0.3))
        low_price = min(open_price, close_price) - abs(np.random.normal(0, daily_volatility * 0.3))
        
        # Generate volume
        base_volume = 50_000_000
        volume = int(base_volume * np.random.uniform(0.7, 1.3))
        
        data.append({
            'date': current_date,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
        
        current_date += timedelta(days=1)
    
    df = pd.DataFrame(data)
    return df.sort_values('date').reset_index(drop=True)


if __name__ == "__main__":
    # Test the mock data generator
    print("Generating mock data for AAPL (30 days)...")
    df = generate_mock_historical_data('AAPL', 30, base_price=150.0)
    
    print(f"\nGenerated {len(df)} trading days")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nLast 5 rows:")
    print(df.tail())
    print(f"\nPrice range: ${df['low'].min():.2f} - ${df['high'].max():.2f}")
    print(f"Average volume: {df['volume'].mean():,.0f}")
