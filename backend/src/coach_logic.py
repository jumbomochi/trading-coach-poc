"""Trading Coach Logic - Analyze trade timing and execution quality"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Union, List


def analyze_trade_timing(
    entry_price: float,
    entry_date: Union[str, datetime],
    df_historical: pd.DataFrame
) -> Dict[str, float]:
    """
    Analyze trade timing by calculating Maximum Favorable/Adverse Excursion.
    
    This function helps traders understand:
    - How much better they could have entered (MAE-based ideal entry)
    - How much profit potential was available (MFE)
    
    Args:
        entry_price: The actual price at which the trade was entered
        entry_date: The date when the trade was entered (string or datetime)
        df_historical: DataFrame with columns: date, open, high, low, close, volume
    
    Returns:
        Dictionary containing:
            - 'mfe': Maximum Favorable Excursion (highest price reached)
            - 'mae': Maximum Adverse Excursion (lowest price reached)
            - 'mfe_percent': Percentage gain from entry to MFE
            - 'mae_percent': Percentage loss from entry to MAE
            - 'ideal_entry': The lowest price in the period (best possible entry)
            - 'entry_timing_score': Percentage difference between actual and ideal entry
            - 'missed_profit_potential': Percentage of profit that could have been captured
                                        if entered at ideal price and exited at MFE
    
    Example:
        >>> df = get_historical_data('AAPL', 30)
        >>> result = analyze_trade_timing(150.00, '2025-12-01', df)
        >>> print(f"Entry timing score: {result['entry_timing_score']:.2f}%")
    """
    # Convert entry_date to datetime if it's a string
    if isinstance(entry_date, str):
        entry_date = pd.to_datetime(entry_date)
    
    # Ensure df_historical date column is datetime
    df = df_historical.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter DataFrame to start from entry_date
    df_filtered = df[df['date'] >= entry_date].reset_index(drop=True)
    
    if len(df_filtered) == 0:
        raise ValueError(
            f"No data available from entry_date {entry_date}. "
            f"Historical data range: {df['date'].min()} to {df['date'].max()}"
        )
    
    # Calculate Maximum Favorable Excursion (MFE) - highest price reached
    mfe = df_filtered['high'].max()
    
    # Calculate Maximum Adverse Excursion (MAE) - lowest price reached
    mae = df_filtered['low'].min()
    
    # Ideal entry would be the lowest price in the period
    ideal_entry = mae
    
    # Calculate percentage metrics
    mfe_percent = ((mfe - entry_price) / entry_price) * 100
    mae_percent = ((mae - entry_price) / entry_price) * 100
    
    # Entry timing score: how much worse was actual entry vs ideal entry
    # Negative value means entered above ideal, positive means below (better than ideal)
    entry_timing_score = ((ideal_entry - entry_price) / entry_price) * 100
    
    # Missed profit potential: the additional profit that could have been captured
    # if entered at the ideal price (MAE) and exited at the best price (MFE)
    ideal_profit = ((mfe - ideal_entry) / ideal_entry) * 100
    actual_profit_potential = mfe_percent
    missed_profit_potential = ideal_profit - actual_profit_potential
    
    return {
        'mfe': round(mfe, 2),
        'mae': round(mae, 2),
        'mfe_percent': round(mfe_percent, 2),
        'mae_percent': round(mae_percent, 2),
        'ideal_entry': round(ideal_entry, 2),
        'entry_timing_score': round(entry_timing_score, 2),
        'missed_profit_potential': round(missed_profit_potential, 2)
    }


def format_trade_analysis(analysis: Dict[str, float], entry_price: float) -> str:
    """
    Format the trade analysis results into a human-readable report.
    
    Args:
        analysis: Dictionary returned from analyze_trade_timing
        entry_price: The actual entry price
    
    Returns:
        Formatted string report
    """
    report = []
    report.append("=" * 60)
    report.append("TRADE TIMING ANALYSIS")
    report.append("=" * 60)
    report.append(f"\nActual Entry Price: ${entry_price:.2f}")
    report.append(f"Ideal Entry Price:  ${analysis['ideal_entry']:.2f}")
    report.append(f"Entry Timing Score: {analysis['entry_timing_score']:.2f}%")
    
    if analysis['entry_timing_score'] < 0:
        report.append(f"  → You entered {abs(analysis['entry_timing_score']):.2f}% above the ideal entry")
    else:
        report.append(f"  → You entered {analysis['entry_timing_score']:.2f}% below the ideal entry (great timing!)")
    
    report.append(f"\nMaximum Favorable Excursion (MFE): ${analysis['mfe']:.2f}")
    report.append(f"  → Peak profit potential: {analysis['mfe_percent']:.2f}%")
    
    report.append(f"\nMaximum Adverse Excursion (MAE): ${analysis['mae']:.2f}")
    report.append(f"  → Maximum drawdown: {analysis['mae_percent']:.2f}%")
    
    report.append(f"\nMissed Profit Potential: {analysis['missed_profit_potential']:.2f}%")
    report.append(f"  → This is the additional profit you could have captured")
    report.append(f"    with better entry timing (entering at ${analysis['ideal_entry']:.2f})")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)


def detect_behavioral_anomaly(
    current_trade: Dict,
    trade_history: List[Dict]
) -> Dict:
    """
    Detect behavioral anomalies in trading patterns.
    
    Analyzes the current trade against historical trading behavior to identify:
    - Position sizing anomalies (>2 std deviations from mean)
    - Stock beta anomalies (>2 std deviations from mean)
    - New sector exposure (sectors not previously traded)
    
    Args:
        current_trade: Dictionary with keys: 'position_size', 'stock_beta', 'sector'
        trade_history: List of trade dictionaries with same keys as current_trade
    
    Returns:
        Dictionary containing:
            - 'is_anomaly': Boolean indicating if any anomaly detected
            - 'anomalies': List of specific anomalies detected
            - 'warnings': List of warnings (e.g., new sector)
            - 'metrics': Dict with statistical metrics for reference
    
    Example:
        >>> current = {'position_size': 50000, 'stock_beta': 2.5, 'sector': 'Technology'}
        >>> history = [
        ...     {'position_size': 10000, 'stock_beta': 1.2, 'sector': 'Technology'},
        ...     {'position_size': 12000, 'stock_beta': 1.1, 'sector': 'Healthcare'}
        ... ]
        >>> result = detect_behavioral_anomaly(current, history)
        >>> if result['is_anomaly']:
        ...     print("Anomalies detected:", result['anomalies'])
    """
    anomalies = []
    warnings = []
    metrics = {}
    
    # Validate inputs
    if not trade_history:
        return {
            'is_anomaly': False,
            'anomalies': [],
            'warnings': ['No trade history available for comparison'],
            'metrics': {}
        }
    
    # Required fields
    required_fields = ['position_size', 'stock_beta', 'sector']
    for field in required_fields:
        if field not in current_trade:
            raise ValueError(f"current_trade missing required field: {field}")
    
    # Extract historical data
    position_sizes = [t.get('position_size') for t in trade_history if t.get('position_size') is not None]
    stock_betas = [t.get('stock_beta') for t in trade_history if t.get('stock_beta') is not None]
    sectors = [t.get('sector') for t in trade_history if t.get('sector') is not None]
    
    # Check position size anomaly
    if len(position_sizes) >= 2:  # Need at least 2 data points for std
        mean_size = np.mean(position_sizes)
        std_size = np.std(position_sizes, ddof=1)  # Sample standard deviation
        
        metrics['position_size_mean'] = round(mean_size, 2)
        metrics['position_size_std'] = round(std_size, 2)
        
        if std_size > 0:  # Avoid division by zero
            z_score_size = (current_trade['position_size'] - mean_size) / std_size
            metrics['position_size_z_score'] = round(z_score_size, 2)
            
            if abs(z_score_size) > 2:
                direction = "larger" if z_score_size > 0 else "smaller"
                anomalies.append({
                    'type': 'position_size',
                    'message': f"Position size is {abs(z_score_size):.2f} standard deviations {direction} than usual",
                    'current_value': current_trade['position_size'],
                    'historical_mean': round(mean_size, 2),
                    'z_score': round(z_score_size, 2)
                })
    else:
        warnings.append('Insufficient trade history for position size analysis (need at least 2 trades)')
    
    # Check stock beta anomaly
    if len(stock_betas) >= 2:
        mean_beta = np.mean(stock_betas)
        std_beta = np.std(stock_betas, ddof=1)
        
        metrics['stock_beta_mean'] = round(mean_beta, 2)
        metrics['stock_beta_std'] = round(std_beta, 2)
        
        if std_beta > 0:  # Avoid division by zero
            z_score_beta = (current_trade['stock_beta'] - mean_beta) / std_beta
            metrics['stock_beta_z_score'] = round(z_score_beta, 2)
            
            if abs(z_score_beta) > 2:
                direction = "higher" if z_score_beta > 0 else "lower"
                risk_level = "riskier" if z_score_beta > 0 else "less risky"
                anomalies.append({
                    'type': 'stock_beta',
                    'message': f"Stock beta is {abs(z_score_beta):.2f} standard deviations {direction} than usual ({risk_level})",
                    'current_value': current_trade['stock_beta'],
                    'historical_mean': round(mean_beta, 2),
                    'z_score': round(z_score_beta, 2)
                })
    else:
        warnings.append('Insufficient trade history for stock beta analysis (need at least 2 trades)')
    
    # Check for new sector exposure
    if sectors:
        current_sector = current_trade.get('sector')
        if current_sector and current_sector not in sectors:
            warnings.append({
                'type': 'new_sector',
                'message': f"New Sector Warning: '{current_sector}' is not in your trading history",
                'current_sector': current_sector,
                'known_sectors': list(set(sectors))
            })
    
    return {
        'is_anomaly': len(anomalies) > 0,
        'anomalies': anomalies,
        'warnings': warnings,
        'metrics': metrics
    }


def format_behavioral_analysis(analysis: Dict, current_trade: Dict) -> str:
    """
    Format the behavioral anomaly analysis into a human-readable report.
    
    Args:
        analysis: Dictionary returned from detect_behavioral_anomaly
        current_trade: The current trade being analyzed
    
    Returns:
        Formatted string report
    """
    report = []
    report.append("=" * 60)
    report.append("BEHAVIORAL ANOMALY DETECTION")
    report.append("=" * 60)
    
    report.append(f"\nCurrent Trade:")
    report.append(f"  Position Size: ${current_trade.get('position_size', 'N/A'):,.2f}")
    report.append(f"  Stock Beta: {current_trade.get('stock_beta', 'N/A')}")
    report.append(f"  Sector: {current_trade.get('sector', 'N/A')}")
    
    if analysis['metrics']:
        report.append(f"\nHistorical Averages:")
        if 'position_size_mean' in analysis['metrics']:
            report.append(f"  Mean Position Size: ${analysis['metrics']['position_size_mean']:,.2f}")
        if 'stock_beta_mean' in analysis['metrics']:
            report.append(f"  Mean Stock Beta: {analysis['metrics']['stock_beta_mean']:.2f}")
    
    if analysis['is_anomaly']:
        report.append(f"\n⚠️  ANOMALIES DETECTED: {len(analysis['anomalies'])}")
        for i, anomaly in enumerate(analysis['anomalies'], 1):
            report.append(f"\n  {i}. {anomaly['message']}")
            report.append(f"     Current: {anomaly['current_value']}")
            report.append(f"     Historical Mean: {anomaly['historical_mean']}")
    else:
        report.append(f"\n✓ No anomalies detected - trade is within normal parameters")
    
    if analysis['warnings']:
        report.append(f"\nWarnings:")
        for warning in analysis['warnings']:
            if isinstance(warning, dict):
                report.append(f"  • {warning['message']}")
                if 'known_sectors' in warning:
                    report.append(f"    Known sectors: {', '.join(warning['known_sectors'])}")
            else:
                report.append(f"  • {warning}")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)


if __name__ == "__main__":
    # Example usage with sample data
    from tiger_client import get_historical_data
    
    print("=" * 70)
    print("EXAMPLE 1: Trade Timing Analysis")
    print("=" * 70)
    
    try:
        print("\nFetching historical data for AAPL...")
        df = get_historical_data('AAPL', 60)
        
        # Simulate a trade entry
        # Let's say we entered 30 days ago at a specific price
        if len(df) > 30:
            entry_date = df.iloc[-30]['date']
            # Enter at the close price of that day
            entry_price = df.iloc[-30]['close']
            
            print(f"\nAnalyzing trade entered on {entry_date.strftime('%Y-%m-%d')} at ${entry_price:.2f}")
            
            # Analyze the trade
            analysis = analyze_trade_timing(entry_price, entry_date, df)
            
            # Print formatted report
            print(format_trade_analysis(analysis, entry_price))
        else:
            print("Not enough historical data for example. Need at least 30 days.")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Behavioral Anomaly Detection")
    print("=" * 70)
    
    # Sample trade history
    trade_history = [
        {'position_size': 10000, 'stock_beta': 1.2, 'sector': 'Technology'},
        {'position_size': 12000, 'stock_beta': 1.1, 'sector': 'Healthcare'},
        {'position_size': 11000, 'stock_beta': 1.3, 'sector': 'Technology'},
        {'position_size': 9500, 'stock_beta': 1.0, 'sector': 'Finance'},
        {'position_size': 10500, 'stock_beta': 1.15, 'sector': 'Healthcare'}
    ]
    
    # Test case 1: Normal trade
    print("\nTest Case 1: Normal trade (should pass)")
    current_trade_normal = {
        'position_size': 10200,
        'stock_beta': 1.25,
        'sector': 'Technology'
    }
    result = detect_behavioral_anomaly(current_trade_normal, trade_history)
    print(format_behavioral_analysis(result, current_trade_normal))
    
    # Test case 2: Anomalous position size
    print("\nTest Case 2: Anomalous position size")
    current_trade_large = {
        'position_size': 50000,  # Much larger than usual
        'stock_beta': 1.2,
        'sector': 'Technology'
    }
    result = detect_behavioral_anomaly(current_trade_large, trade_history)
    print(format_behavioral_analysis(result, current_trade_large))
    
    # Test case 3: High beta + new sector
    print("\nTest Case 3: High beta stock + new sector")
    current_trade_risky = {
        'position_size': 11000,
        'stock_beta': 3.5,  # Much higher beta than usual
        'sector': 'Cryptocurrency'  # New sector
    }
    result = detect_behavioral_anomaly(current_trade_risky, trade_history)
    print(format_behavioral_analysis(result, current_trade_risky))
