"""Database module for Trading Coach - SQLite3 storage"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
from contextlib import contextmanager
import os


# Default database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'trading_coach.db')


@contextmanager
def get_db_connection(db_path: str = DB_PATH):
    """
    Context manager for database connections.
    
    Args:
        db_path: Path to the SQLite database file
        
    Yields:
        sqlite3.Connection: Database connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database(db_path: str = DB_PATH):
    """
    Initialize the database with required tables.
    
    Args:
        db_path: Path to the SQLite database file
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Create trades table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                entry_price REAL NOT NULL,
                entry_date TEXT NOT NULL,
                horizon INTEGER NOT NULL,
                position_size REAL,
                stock_beta REAL,
                sector TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create analysis_results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER NOT NULL,
                analysis_type TEXT NOT NULL,
                result_data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trade_id) REFERENCES trades(id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trades_symbol 
            ON trades(symbol)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trades_entry_date 
            ON trades(entry_date)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analysis_trade_id 
            ON analysis_results(trade_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analysis_type 
            ON analysis_results(analysis_type)
        """)
        
        conn.commit()
        print(f"Database initialized at: {db_path}")


def save_trade(
    symbol: str,
    entry_price: float,
    entry_date: Union[str, datetime],
    horizon: int,
    position_size: Optional[float] = None,
    stock_beta: Optional[float] = None,
    sector: Optional[str] = None,
    db_path: str = DB_PATH
) -> int:
    """
    Save a new trade to the database.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL')
        entry_price: Entry price of the trade
        entry_date: Date of trade entry (string or datetime)
        horizon: Number of days for analysis horizon
        position_size: Size of the position (optional)
        stock_beta: Beta of the stock (optional)
        sector: Sector of the stock (optional)
        db_path: Path to the SQLite database file
        
    Returns:
        int: ID of the newly created trade
        
    Example:
        >>> trade_id = save_trade('AAPL', 150.00, '2025-12-01', 30, 
        ...                       position_size=10000, stock_beta=1.2, sector='Technology')
        >>> print(f"Trade saved with ID: {trade_id}")
    """
    # Convert datetime to string if needed
    if isinstance(entry_date, datetime):
        entry_date = entry_date.strftime('%Y-%m-%d')
    
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO trades (symbol, entry_price, entry_date, horizon, 
                              position_size, stock_beta, sector)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, entry_price, entry_date, horizon, position_size, stock_beta, sector))
        
        trade_id = cursor.lastrowid
        conn.commit()
        
    return trade_id


def save_analysis_result(
    trade_id: int,
    analysis_type: str,
    result_data: Dict,
    db_path: str = DB_PATH
) -> int:
    """
    Save analysis results to the database.
    
    Args:
        trade_id: ID of the trade being analyzed
        analysis_type: Type of analysis ('timing' or 'behavioral')
        result_data: Dictionary containing analysis results
        db_path: Path to the SQLite database file
        
    Returns:
        int: ID of the newly created analysis result
        
    Example:
        >>> timing_result = analyze_trade_timing(150.00, '2025-12-01', df)
        >>> result_id = save_analysis_result(trade_id, 'timing', timing_result)
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Convert dict to JSON string
        result_json = json.dumps(result_data)
        
        cursor.execute("""
            INSERT INTO analysis_results (trade_id, analysis_type, result_data)
            VALUES (?, ?, ?)
        """, (trade_id, analysis_type, result_json))
        
        result_id = cursor.lastrowid
        conn.commit()
        
    return result_id


def get_last_n_trades(n: int = 50, db_path: str = DB_PATH) -> List[Dict]:
    """
    Retrieve the last N trades from the database for baseline analysis.
    
    Args:
        n: Number of trades to retrieve (default: 50)
        db_path: Path to the SQLite database file
        
    Returns:
        List of dictionaries containing trade data
        
    Example:
        >>> recent_trades = get_last_n_trades(50)
        >>> print(f"Retrieved {len(recent_trades)} trades")
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, symbol, entry_price, entry_date, horizon,
                   position_size, stock_beta, sector, created_at
            FROM trades
            ORDER BY created_at DESC
            LIMIT ?
        """, (n,))
        
        rows = cursor.fetchall()
        
    # Convert to list of dictionaries
    trades = []
    for row in rows:
        trades.append({
            'id': row['id'],
            'symbol': row['symbol'],
            'entry_price': row['entry_price'],
            'entry_date': row['entry_date'],
            'horizon': row['horizon'],
            'position_size': row['position_size'],
            'stock_beta': row['stock_beta'],
            'sector': row['sector'],
            'created_at': row['created_at']
        })
    
    return trades


def get_trade_by_id(trade_id: int, db_path: str = DB_PATH) -> Optional[Dict]:
    """
    Retrieve a specific trade by ID.
    
    Args:
        trade_id: ID of the trade to retrieve
        db_path: Path to the SQLite database file
        
    Returns:
        Dictionary containing trade data or None if not found
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, symbol, entry_price, entry_date, horizon,
                   position_size, stock_beta, sector, created_at
            FROM trades
            WHERE id = ?
        """, (trade_id,))
        
        row = cursor.fetchone()
        
    if row is None:
        return None
    
    return {
        'id': row['id'],
        'symbol': row['symbol'],
        'entry_price': row['entry_price'],
        'entry_date': row['entry_date'],
        'horizon': row['horizon'],
        'position_size': row['position_size'],
        'stock_beta': row['stock_beta'],
        'sector': row['sector'],
        'created_at': row['created_at']
    }


def get_analysis_results(trade_id: int, db_path: str = DB_PATH) -> List[Dict]:
    """
    Retrieve all analysis results for a specific trade.
    
    Args:
        trade_id: ID of the trade
        db_path: Path to the SQLite database file
        
    Returns:
        List of dictionaries containing analysis results
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, analysis_type, result_data, created_at
            FROM analysis_results
            WHERE trade_id = ?
            ORDER BY created_at DESC
        """, (trade_id,))
        
        rows = cursor.fetchall()
        
    results = []
    for row in rows:
        results.append({
            'id': row['id'],
            'analysis_type': row['analysis_type'],
            'result_data': json.loads(row['result_data']),
            'created_at': row['created_at']
        })
    
    return results


def get_trades_for_behavioral_analysis(
    n: int = 50,
    exclude_trade_id: Optional[int] = None,
    db_path: str = DB_PATH
) -> List[Dict]:
    """
    Get recent trades formatted for behavioral anomaly detection.
    
    This function retrieves trades with position_size, stock_beta, and sector
    for use in the detect_behavioral_anomaly function.
    
    Args:
        n: Number of trades to retrieve (default: 50)
        exclude_trade_id: Optional trade ID to exclude (typically the current trade)
        db_path: Path to the SQLite database file
        
    Returns:
        List of dictionaries ready for behavioral analysis
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        if exclude_trade_id:
            cursor.execute("""
                SELECT position_size, stock_beta, sector
                FROM trades
                WHERE id != ? 
                  AND position_size IS NOT NULL 
                  AND stock_beta IS NOT NULL 
                  AND sector IS NOT NULL
                ORDER BY created_at DESC
                LIMIT ?
            """, (exclude_trade_id, n))
        else:
            cursor.execute("""
                SELECT position_size, stock_beta, sector
                FROM trades
                WHERE position_size IS NOT NULL 
                  AND stock_beta IS NOT NULL 
                  AND sector IS NOT NULL
                ORDER BY created_at DESC
                LIMIT ?
            """, (n,))
        
        rows = cursor.fetchall()
        
    trade_history = []
    for row in rows:
        trade_history.append({
            'position_size': row['position_size'],
            'stock_beta': row['stock_beta'],
            'sector': row['sector']
        })
    
    return trade_history


def get_database_stats(db_path: str = DB_PATH) -> Dict:
    """
    Get statistics about the database.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        Dictionary containing database statistics
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Count total trades
        cursor.execute("SELECT COUNT(*) as count FROM trades")
        total_trades = cursor.fetchone()['count']
        
        # Count total analyses
        cursor.execute("SELECT COUNT(*) as count FROM analysis_results")
        total_analyses = cursor.fetchone()['count']
        
        # Get date range
        cursor.execute("""
            SELECT MIN(entry_date) as first_trade, MAX(entry_date) as last_trade
            FROM trades
        """)
        date_range = cursor.fetchone()
        
        # Get unique symbols
        cursor.execute("SELECT COUNT(DISTINCT symbol) as count FROM trades")
        unique_symbols = cursor.fetchone()['count']
        
        # Get unique sectors
        cursor.execute("""
            SELECT COUNT(DISTINCT sector) as count 
            FROM trades 
            WHERE sector IS NOT NULL
        """)
        unique_sectors = cursor.fetchone()['count']
        
    return {
        'total_trades': total_trades,
        'total_analyses': total_analyses,
        'first_trade_date': date_range['first_trade'],
        'last_trade_date': date_range['last_trade'],
        'unique_symbols': unique_symbols,
        'unique_sectors': unique_sectors,
        'database_path': db_path
    }


if __name__ == "__main__":
    # Initialize database
    print("Initializing database...")
    init_database()
    
    # Example: Save some sample trades
    print("\nSaving sample trades...")
    
    sample_trades = [
        {'symbol': 'AAPL', 'entry_price': 150.00, 'entry_date': '2025-11-01', 
         'horizon': 30, 'position_size': 10000, 'stock_beta': 1.2, 'sector': 'Technology'},
        {'symbol': 'TSLA', 'entry_price': 250.00, 'entry_date': '2025-11-15', 
         'horizon': 30, 'position_size': 12000, 'stock_beta': 1.8, 'sector': 'Automotive'},
        {'symbol': 'MSFT', 'entry_price': 380.00, 'entry_date': '2025-12-01', 
         'horizon': 30, 'position_size': 11000, 'stock_beta': 1.1, 'sector': 'Technology'},
        {'symbol': 'JNJ', 'entry_price': 160.00, 'entry_date': '2025-12-10', 
         'horizon': 30, 'position_size': 9500, 'stock_beta': 0.8, 'sector': 'Healthcare'},
        {'symbol': 'JPM', 'entry_price': 145.00, 'entry_date': '2025-12-15', 
         'horizon': 30, 'position_size': 10500, 'stock_beta': 1.3, 'sector': 'Finance'},
    ]
    
    trade_ids = []
    for trade in sample_trades:
        trade_id = save_trade(**trade)
        trade_ids.append(trade_id)
        print(f"  Saved {trade['symbol']} with ID: {trade_id}")
    
    # Example: Save an analysis result
    print("\nSaving sample analysis result...")
    sample_analysis = {
        'mfe': 155.50,
        'mae': 148.00,
        'mfe_percent': 3.67,
        'mae_percent': -1.33,
        'ideal_entry': 148.00,
        'entry_timing_score': -1.33,
        'missed_profit_potential': 5.07
    }
    result_id = save_analysis_result(trade_ids[0], 'timing', sample_analysis)
    print(f"  Saved timing analysis with ID: {result_id}")
    
    # Example: Retrieve last 50 trades
    print("\nRetrieving last trades...")
    recent_trades = get_last_n_trades(5)
    print(f"  Retrieved {len(recent_trades)} trades:")
    for trade in recent_trades:
        print(f"    - {trade['symbol']} @ ${trade['entry_price']} on {trade['entry_date']}")
    
    # Example: Get behavioral analysis data
    print("\nRetrieving trades for behavioral analysis...")
    history = get_trades_for_behavioral_analysis(5)
    print(f"  Retrieved {len(history)} trades with behavioral data")
    
    # Display database statistics
    print("\nDatabase Statistics:")
    stats = get_database_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
