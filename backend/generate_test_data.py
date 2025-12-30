"""Generate test datasets for different investor profiles"""

import random
import numpy as np
from datetime import datetime, timedelta
from src.database import save_trade, init_database, get_database_stats

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


# Define investor profiles
PROFILES = {
    'institutional': {
        'name': 'Institutional Investor - Balanced, Tech Focused',
        'position_size': {
            'mean': 500000,
            'std': 150000,
            'min': 200000,
            'max': 1000000
        },
        'stocks': {
            # Tech giants and established companies
            'AAPL': {'weight': 15, 'beta': 1.2, 'sector': 'Technology'},
            'MSFT': {'weight': 15, 'beta': 1.1, 'sector': 'Technology'},
            'GOOGL': {'weight': 12, 'beta': 1.0, 'sector': 'Technology'},
            'AMZN': {'weight': 10, 'beta': 1.3, 'sector': 'Technology'},
            'META': {'weight': 10, 'beta': 1.4, 'sector': 'Technology'},
            'NVDA': {'weight': 8, 'beta': 1.8, 'sector': 'Technology'},
            'JPM': {'weight': 8, 'beta': 1.2, 'sector': 'Finance'},
            'BAC': {'weight': 7, 'beta': 1.3, 'sector': 'Finance'},
            'JNJ': {'weight': 5, 'beta': 0.7, 'sector': 'Healthcare'},
            'PFE': {'weight': 5, 'beta': 0.8, 'sector': 'Healthcare'},
            'XOM': {'weight': 5, 'beta': 1.0, 'sector': 'Energy'},
        },
        'horizon_days': 60
    },
    
    'retail_speculative': {
        'name': 'Retail Investor - Speculative, Concept Stocks',
        'position_size': {
            'mean': 5000,
            'std': 3000,
            'min': 1000,
            'max': 15000
        },
        'stocks': {
            # High-growth, speculative stocks
            'TSLA': {'weight': 20, 'beta': 2.0, 'sector': 'Automotive'},
            'NVDA': {'weight': 15, 'beta': 1.8, 'sector': 'Technology'},
            'AMD': {'weight': 12, 'beta': 1.9, 'sector': 'Technology'},
            'COIN': {'weight': 10, 'beta': 3.5, 'sector': 'Finance'},
            'PLTR': {'weight': 10, 'beta': 2.8, 'sector': 'Technology'},
            'SNOW': {'weight': 8, 'beta': 2.5, 'sector': 'Technology'},
            'RIVN': {'weight': 7, 'beta': 3.2, 'sector': 'Automotive'},
            'ARKK': {'weight': 6, 'beta': 2.2, 'sector': 'ETF'},
            'SOFI': {'weight': 5, 'beta': 2.6, 'sector': 'Finance'},
            'HOOD': {'weight': 4, 'beta': 3.0, 'sector': 'Finance'},
            'NIO': {'weight': 3, 'beta': 2.9, 'sector': 'Automotive'},
        },
        'horizon_days': 30
    },
    
    'retail_conservative': {
        'name': 'Retail Investor - Conservative, DCA, ETFs',
        'position_size': {
            'mean': 2000,
            'std': 500,
            'min': 1000,
            'max': 3500
        },
        'stocks': {
            # Conservative ETFs and blue chips
            'SPY': {'weight': 20, 'beta': 1.0, 'sector': 'ETF'},
            'VTI': {'weight': 18, 'beta': 1.0, 'sector': 'ETF'},
            'QQQ': {'weight': 15, 'beta': 1.1, 'sector': 'ETF'},
            'VOO': {'weight': 12, 'beta': 1.0, 'sector': 'ETF'},
            'VIG': {'weight': 10, 'beta': 0.9, 'sector': 'ETF'},
            'BND': {'weight': 8, 'beta': 0.3, 'sector': 'ETF'},
            'AAPL': {'weight': 5, 'beta': 1.2, 'sector': 'Technology'},
            'JNJ': {'weight': 4, 'beta': 0.7, 'sector': 'Healthcare'},
            'PG': {'weight': 4, 'beta': 0.6, 'sector': 'Consumer'},
            'KO': {'weight': 2, 'beta': 0.5, 'sector': 'Consumer'},
            'T': {'weight': 2, 'beta': 0.7, 'sector': 'Telecom'},
        },
        'horizon_days': 90
    }
}


def generate_position_size(profile):
    """Generate a realistic position size based on profile"""
    mean = profile['position_size']['mean']
    std = profile['position_size']['std']
    min_size = profile['position_size']['min']
    max_size = profile['position_size']['max']
    
    # Generate with some skew (more smaller positions)
    size = np.random.lognormal(np.log(mean), 0.5)
    size = np.clip(size, min_size, max_size)
    
    return round(size, 2)


def select_stock(profile):
    """Select a stock based on weighted probabilities"""
    stocks = profile['stocks']
    symbols = list(stocks.keys())
    weights = [stocks[s]['weight'] for s in symbols]
    
    symbol = random.choices(symbols, weights=weights, k=1)[0]
    return symbol, stocks[symbol]


def generate_entry_price(symbol, base_prices):
    """Generate a realistic entry price for a symbol"""
    base_price = base_prices.get(symbol, 100.0)
    # Add some randomness (±20% variation)
    variation = random.uniform(-0.20, 0.20)
    price = base_price * (1 + variation)
    return round(price, 2)


def generate_entry_date(start_date, end_date):
    """Generate a random date between start and end"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)


def generate_trades_for_profile(profile_key, num_trades=100):
    """Generate trades for a specific investor profile"""
    profile = PROFILES[profile_key]
    
    print(f"\n{'='*80}")
    print(f"Generating {num_trades} trades for: {profile['name']}")
    print(f"{'='*80}")
    
    # Base prices for common stocks (approximate real values)
    base_prices = {
        'AAPL': 275, 'MSFT': 485, 'GOOGL': 195, 'AMZN': 225, 'META': 650,
        'NVDA': 875, 'TSLA': 385, 'AMD': 135, 'JPM': 240, 'BAC': 45,
        'JNJ': 160, 'PFE': 26, 'XOM': 110, 'COIN': 235, 'PLTR': 70,
        'SNOW': 165, 'RIVN': 12, 'ARKK': 48, 'SOFI': 15, 'HOOD': 32,
        'NIO': 4, 'SPY': 600, 'VTI': 285, 'QQQ': 525, 'VOO': 555,
        'VIG': 205, 'BND': 70, 'PG': 170, 'KO': 62, 'T': 22
    }
    
    # Date range: last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    trades_data = []
    
    for i in range(num_trades):
        # Select stock
        symbol, stock_info = select_stock(profile)
        
        # Generate trade parameters
        position_size = generate_position_size(profile)
        entry_price = generate_entry_price(symbol, base_prices)
        entry_date = generate_entry_date(start_date, end_date)
        
        # Add some variation to beta (±10%)
        beta_variation = random.uniform(-0.1, 0.1)
        stock_beta = round(stock_info['beta'] * (1 + beta_variation), 2)
        
        trades_data.append({
            'symbol': symbol,
            'entry_price': entry_price,
            'entry_date': entry_date.strftime('%Y-%m-%d'),
            'horizon': profile['horizon_days'],
            'position_size': position_size,
            'stock_beta': stock_beta,
            'sector': stock_info['sector']
        })
    
    # Sort by date
    trades_data.sort(key=lambda x: x['entry_date'])
    
    # Save to database
    trade_ids = []
    for i, trade in enumerate(trades_data, 1):
        trade_id = save_trade(**trade)
        trade_ids.append(trade_id)
        if i % 20 == 0:
            print(f"  Saved {i}/{num_trades} trades...")
    
    print(f"✅ Completed! Saved {num_trades} trades (IDs: {trade_ids[0]}-{trade_ids[-1]})")
    
    # Print summary statistics
    print(f"\nProfile Summary:")
    print(f"  Avg Position Size: ${np.mean([t['position_size'] for t in trades_data]):,.2f}")
    print(f"  Position Size Range: ${min([t['position_size'] for t in trades_data]):,.2f} - ${max([t['position_size'] for t in trades_data]):,.2f}")
    print(f"  Avg Beta: {np.mean([t['stock_beta'] for t in trades_data]):.2f}")
    print(f"  Beta Range: {min([t['stock_beta'] for t in trades_data]):.2f} - {max([t['stock_beta'] for t in trades_data]):.2f}")
    
    # Count by sector
    sectors = {}
    for trade in trades_data:
        sector = trade['sector']
        sectors[sector] = sectors.get(sector, 0) + 1
    print(f"  Sector Distribution:")
    for sector, count in sorted(sectors.items(), key=lambda x: -x[1]):
        print(f"    {sector}: {count} trades ({count/num_trades*100:.1f}%)")
    
    return trade_ids


def main():
    """Generate all test datasets"""
    print("Initializing database...")
    init_database()
    
    print("\nStarting test data generation...")
    print("="*80)
    
    all_trade_ids = {}
    
    # Generate trades for each profile
    for profile_key in ['institutional', 'retail_speculative', 'retail_conservative']:
        trade_ids = generate_trades_for_profile(profile_key, num_trades=100)
        all_trade_ids[profile_key] = trade_ids
    
    # Final summary
    print("\n" + "="*80)
    print("GENERATION COMPLETE")
    print("="*80)
    
    stats = get_database_stats()
    print(f"\nDatabase Statistics:")
    print(f"  Total Trades: {stats['total_trades']}")
    print(f"  Unique Symbols: {stats['unique_symbols']}")
    print(f"  Unique Sectors: {stats['unique_sectors']}")
    print(f"  Date Range: {stats['first_trade_date']} to {stats['last_trade_date']}")
    
    print("\nTrade ID Ranges by Profile:")
    for profile_key, trade_ids in all_trade_ids.items():
        profile_name = PROFILES[profile_key]['name']
        print(f"  {profile_name}:")
        print(f"    Trade IDs: {trade_ids[0]} - {trade_ids[-1]}")
    
    print("\n" + "="*80)
    print("You can now test behavioral analysis with these realistic datasets!")
    print("="*80)


if __name__ == "__main__":
    main()
