"""Tiger Brokers API Client for Trading Coach POC"""

import os
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
from dotenv import load_dotenv
from tigeropen.common.consts import Language, Market
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.tiger_open_config import TigerOpenClientConfig

# Load environment variables
load_dotenv()


class TigerClientManager:
    """Manager class for Tiger Brokers QuoteClient"""
    
    def __init__(self, sandbox: bool = False):
        """
        Initialize the Tiger Brokers QuoteClient
        
        Args:
            sandbox: Whether to use sandbox mode (default: False)
        """
        # Get credentials from environment variables
        self.tiger_id = os.getenv('tiger_id')
        self.private_key = os.getenv('private_key_pk1')  # Using pk1 as in user's working code
        self.account_id = os.getenv('account')
        
        if not self.tiger_id or not self.private_key:
            raise ValueError(
                "Missing Tiger Brokers credentials. "
                "Please set tiger_id and private_key_pk1 in .env file"
            )
        
        # Configure Tiger Open API client (matching user's working code)
        self.client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
        self.client_config.private_key = self.private_key
        self.client_config.tiger_id = self.tiger_id
        self.client_config.language = Language.en_US
        
        # Set account if provided
        if self.account_id:
            self.client_config.account = self.account_id
        
        # Initialize QuoteClient
        self.quote_client = QuoteClient(self.client_config)
    
    def get_historical_data(
        self, 
        symbol: str, 
        horizon_days: int,
        market: Market = Market.US
    ) -> pd.DataFrame:
        """
        Fetch historical daily bars for a given symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'TSLA')
            horizon_days: Number of days of historical data to fetch
            market: Market to query (default: US)
        
        Returns:
            pandas.DataFrame with columns: date, open, high, low, close, volume
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=horizon_days)
        
        # Format dates for Tiger API
        begin_time = int(start_date.timestamp() * 1000)  # milliseconds
        end_time = int(end_date.timestamp() * 1000)
        
        # Fetch data from Tiger API
        bars = self.quote_client.get_bars(
            symbols=[symbol],
            period='day',
            begin_time=begin_time,
            end_time=end_time
        )
        
        # Check if bars is a DataFrame or list
        if isinstance(bars, pd.DataFrame):
            if bars.empty:
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            # Convert Tiger API DataFrame format to our format
            df = pd.DataFrame({
                'date': pd.to_datetime(bars['time'], unit='ms'),
                'open': bars['open'],
                'high': bars['high'],
                'low': bars['low'],
                'close': bars['close'],
                'volume': bars['volume']
            })
        else:
            # bars is a list of bar objects
            if not bars or len(bars) == 0:
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            
            # Convert to DataFrame
            data_list = []
            for bar in bars:
                data_list.append({
                    'date': datetime.fromtimestamp(bar.time / 1000),
                    'open': bar.open,
                    'high': bar.high,
                    'low': bar.low,
                    'close': bar.close,
                    'volume': bar.volume
                })
            df = pd.DataFrame(data_list)
        
        df = df.sort_values('date').reset_index(drop=True)
        
        return df


def get_historical_data(symbol: str, horizon_days: int) -> pd.DataFrame:
    """
    Helper function to fetch historical data for a symbol.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'TSLA')
        horizon_days: Number of days of historical data to fetch
    
    Returns:
        pandas.DataFrame with columns: date, open, high, low, close, volume
    
    Example:
        >>> df = get_historical_data('AAPL', 30)
        >>> print(df.head())
    """
    client = TigerClientManager()
    return client.get_historical_data(symbol, horizon_days)


if __name__ == "__main__":
    # Example usage
    try:
        print("Fetching historical data for AAPL (last 30 days)...")
        df = get_historical_data('AAPL', 30)
        print(f"\nRetrieved {len(df)} records")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nLast 5 rows:")
        print(df.tail())
        print(f"\nColumns: {list(df.columns)}")
    except Exception as e:
        print(f"Error: {e}")
