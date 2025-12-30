# Trading Coach POC

A Python application for trading analysis and coaching using Tiger Brokers API.

## Project Structure

```
trading-coach-poc/
├── src/
│   ├── __init__.py
│   └── tiger_client.py      # Tiger Brokers API client
├── tests/
│   └── __init__.py
├── .env                      # Environment variables (not in git)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Prerequisites

- Python 3.8 or higher
- Tiger Brokers API credentials

### 2. Get Tiger Brokers Credentials

1. Sign up for a Tiger Brokers account at https://www.tigerbrokers.com.sg/
2. Apply for API access through their developer portal
3. Obtain your:
   - `TIGER_ID`: Your Tiger Brokers user ID
   - `PRIVATE_KEY`: Your API private key
   - `ACCOUNT_ID`: Your trading account ID

### 3. Install Dependencies

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the `.env` file and add your Tiger Brokers credentials:

```bash
TIGER_ID=your_tiger_id_here
PRIVATE_KEY=your_private_key_here
ACCOUNT_ID=your_account_id_here
```

⚠️ **Important**: Never commit your `.env` file to version control!

## Usage

### Command-Line Interface

The easiest way to use Trading Coach is via the command-line interface:

```bash
# Basic usage - analyze a trade
python main.py AAPL 150.00 2025-12-01

# With behavioral analysis (position size, beta, sector)
python main.py TSLA 250.50 2025-12-15 --position-size 15000 --beta 1.8 --sector Automotive

# Short form
python main.py MSFT 380.00 2025-12-20 -p 10000 -b 1.1 -s Technology

# Initialize database first time
python main.py AAPL 150.00 2025-12-01 --init-db

# Analyze without saving to database
python main.py AAPL 150.00 2025-12-01 --no-save
```

### Python API Example

```python
from src.tiger_client import get_historical_data

# Fetch 30 days of historical data for AAPL
df = get_historical_data('AAPL', 30)

print(df.head())
# Output:
#         date    open    high     low   close    volume
# 0 2025-12-01  150.25  152.30  149.80  151.45  50000000
# 1 2025-12-02  151.50  153.20  150.90  152.80  48000000
# ...
```

### Using the TigerClientManager Class

```python
from src.tiger_client import TigerClientManager

# Initialize client
client = TigerClientManager()

# Fetch historical data
df = client.get_historical_data('TSLA', horizon_days=60)

# Analyze the data
print(f"Average closing price: ${df['close'].mean():.2f}")
print(f"Max volume: {df['volume'].max():,}")
```

### Test the Setup

Run the example script:

```bash
python src/tiger_client.py
```

This will fetch 30 days of AAPL data and display the results.

## API Reference

### Command-Line Arguments

```
usage: main.py [-h] [-p POSITION_SIZE] [-b BETA] [-s SECTOR] [-H HORIZON]
               [--no-save] [--init-db]
               symbol price date

positional arguments:
  symbol                Stock symbol (e.g., AAPL, TSLA, MSFT)
  price                 Entry price of the trade
  date                  Entry date in YYYY-MM-DD format

optional arguments:
  -p, --position-size   Position size in dollars
  -b, --beta           Stock beta value
  -s, --sector         Stock sector
  -H, --horizon        Days of historical data (default: 30)
  --no-save            Do not save trade to database
  --init-db            Initialize the database
```

### `get_historical_data(symbol, horizon_days)`

Fetch historical daily bars for a given stock symbol.

**Parameters:**
- `symbol` (str): Stock symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
- `horizon_days` (int): Number of days of historical data to fetch

**Returns:**
- `pandas.DataFrame`: DataFrame with columns:
  - `date`: Trading date (datetime)
  - `open`: Opening price (float)
  - `high`: Highest price (float)
  - `low`: Lowest price (float)
  - `close`: Closing price (float)
  - `volume`: Trading volume (int)

## Troubleshooting

### Authentication Errors

If you see authentication errors, verify:
1. Your credentials are correct in the `.env` file
2. Your Tiger Brokers API account is active
3. You have the necessary permissions for market data

### Module Import Errors

If imports fail, ensure you've:
1. Activated your virtual environment
2. Installed all requirements: `pip install -r requirements.txt`

### No Data Returned

If no data is returned:
1. Check if the symbol is valid
2. Verify market hours and trading days
3. Ensure your API subscription includes the requested market data

## License

Private POC - All rights reserved

## Support

For Tiger Brokers API documentation, visit:
- https://www.tigerbrokers.com.sg/developer/
- https://quant.itigerup.com/openapi/en/python/overview/introduction.html
