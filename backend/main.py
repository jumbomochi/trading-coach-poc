#!/usr/bin/env python
"""
Trading Coach - Main Entry Point

Analyze trades and provide coaching feedback based on timing and behavioral patterns.
"""

import argparse
import sys
from datetime import datetime
from typing import Optional

from src.coach_logic import analyze_trade_timing, detect_behavioral_anomaly
from src.database import (
    init_database, 
    save_trade, 
    save_analysis_result,
    get_trades_for_behavioral_analysis
)
from src.mock_data import generate_mock_historical_data


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Trading Coach - Analyze trade timing and behavioral patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s AAPL 150.00 2025-12-01
  %(prog)s TSLA 250.50 2025-12-15 --position-size 15000 --beta 1.8 --sector Automotive
  %(prog)s MSFT 380.00 2025-12-20 -p 10000 -b 1.1 -s Technology
        """
    )
    
    # Required arguments
    parser.add_argument(
        'symbol',
        type=str,
        help='Stock symbol (e.g., AAPL, TSLA, MSFT)'
    )
    
    parser.add_argument(
        'price',
        type=float,
        help='Entry price of the trade'
    )
    
    parser.add_argument(
        'date',
        type=str,
        help='Entry date in YYYY-MM-DD format (e.g., 2025-12-01)'
    )
    
    # Optional arguments
    parser.add_argument(
        '-p', '--position-size',
        type=float,
        default=None,
        help='Position size in dollars (optional, for behavioral analysis)'
    )
    
    parser.add_argument(
        '-b', '--beta',
        type=float,
        default=None,
        help='Stock beta value (optional, for behavioral analysis)'
    )
    
    parser.add_argument(
        '-s', '--sector',
        type=str,
        default=None,
        help='Stock sector (optional, for behavioral analysis)'
    )
    
    parser.add_argument(
        '-H', '--horizon',
        type=int,
        default=30,
        help='Number of days of historical data to fetch (default: 30)'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save trade to database'
    )
    
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize the database before running'
    )
    
    parser.add_argument(
        '--mock',
        action='store_true',
        help='Use mock data instead of Tiger API (for testing)'
    )
    
    return parser.parse_args()


def validate_date(date_string: str) -> datetime:
    """
    Validate and parse date string.
    
    Args:
        date_string: Date in YYYY-MM-DD format
        
    Returns:
        datetime object
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{date_string}'. "
            "Please use YYYY-MM-DD format (e.g., 2025-12-01)"
        )


def print_coaching_report(
    symbol: str,
    entry_price: float,
    entry_date: str,
    timing_analysis: dict,
    behavioral_analysis: Optional[dict] = None,
    trade_id: Optional[int] = None
):
    """
    Print a comprehensive coaching report to the terminal.
    
    Args:
        symbol: Stock symbol
        entry_price: Entry price
        entry_date: Entry date
        timing_analysis: Results from analyze_trade_timing
        behavioral_analysis: Results from detect_behavioral_anomaly (optional)
        trade_id: Database ID of the saved trade (optional)
    """
    print("\n" + "=" * 80)
    print(" " * 25 + "🎯 TRADING COACH REPORT")
    print("=" * 80)
    
    # Trade Summary
    print("\n📊 TRADE SUMMARY")
    print("-" * 80)
    print(f"  Symbol:           {symbol}")
    print(f"  Entry Price:      ${entry_price:.2f}")
    print(f"  Entry Date:       {entry_date}")
    if trade_id:
        print(f"  Trade ID:         #{trade_id}")
    
    # Timing Analysis
    print("\n⏱️  TIMING EFFICIENCY ANALYSIS")
    print("-" * 80)
    
    ideal_entry = timing_analysis['ideal_entry']
    entry_score = timing_analysis['entry_timing_score']
    
    print(f"  Actual Entry:     ${entry_price:.2f}")
    print(f"  Ideal Entry:      ${ideal_entry:.2f} (lowest price in period)")
    print(f"  Timing Score:     {entry_score:.2f}%")
    
    # Timing verdict
    if entry_score >= -1:
        verdict = "✅ EXCELLENT - Near optimal entry!"
        color = "green"
    elif entry_score >= -3:
        verdict = "✓ GOOD - Acceptable entry timing"
        color = "yellow"
    elif entry_score >= -5:
        verdict = "⚠️  FAIR - Could be improved"
        color = "orange"
    else:
        verdict = "❌ POOR - Significant timing improvement needed"
        color = "red"
    
    print(f"  Verdict:          {verdict}")
    
    if entry_score < 0:
        print(f"\n  💡 You entered {abs(entry_score):.2f}% above the ideal price.")
        print(f"     Waiting for better entry could have saved ${entry_price - ideal_entry:.2f} per share.")
    else:
        print(f"\n  🎉 Great job! You entered at an excellent price point.")
    
    # MFE/MAE Analysis
    print(f"\n  Peak Potential:   ${timing_analysis['mfe']:.2f} (+{timing_analysis['mfe_percent']:.2f}%)")
    print(f"  Maximum Risk:     ${timing_analysis['mae']:.2f} ({timing_analysis['mae_percent']:.2f}%)")
    print(f"  Missed Profit:    {timing_analysis['missed_profit_potential']:.2f}%")
    
    if timing_analysis['missed_profit_potential'] > 5:
        print(f"     ⚠️  Better entry timing could have captured {timing_analysis['missed_profit_potential']:.2f}% more profit")
    
    # Behavioral Analysis
    if behavioral_analysis:
        print("\n🧠 BEHAVIORAL PATTERN ANALYSIS")
        print("-" * 80)
        
        if behavioral_analysis['is_anomaly']:
            print("  Status:           ⚠️  ANOMALIES DETECTED")
            print(f"\n  {len(behavioral_analysis['anomalies'])} behavioral anomaly(ies) found:\n")
            
            for i, anomaly in enumerate(behavioral_analysis['anomalies'], 1):
                print(f"  {i}. {anomaly['type'].upper().replace('_', ' ')}")
                print(f"     Current:       {anomaly['current_value']}")
                print(f"     Historical:    {anomaly['historical_mean']} (mean)")
                print(f"     Z-Score:       {anomaly['z_score']}")
                print(f"     ⚠️  {anomaly['message']}")
                print()
        else:
            print("  Status:           ✅ NORMAL - Trade is within your typical patterns")
        
        # Display warnings
        if behavioral_analysis['warnings']:
            print("  Warnings:")
            for warning in behavioral_analysis['warnings']:
                if isinstance(warning, dict):
                    print(f"    🔔 {warning['message']}")
                    if 'known_sectors' in warning:
                        print(f"       Known sectors: {', '.join(warning['known_sectors'])}")
                else:
                    print(f"    ℹ️  {warning}")
        
        # Display metrics
        if behavioral_analysis['metrics']:
            print("\n  Your Trading Profile (Based on History):")
            metrics = behavioral_analysis['metrics']
            if 'position_size_mean' in metrics:
                print(f"    Avg Position Size: ${metrics['position_size_mean']:,.2f} " +
                      f"(±${metrics.get('position_size_std', 0):,.2f})")
            if 'stock_beta_mean' in metrics:
                print(f"    Avg Stock Beta:    {metrics['stock_beta_mean']:.2f} " +
                      f"(±{metrics.get('stock_beta_std', 0):.2f})")
    
    # Overall Coaching Advice
    print("\n💼 COACHING ADVICE")
    print("-" * 80)
    
    advice = []
    
    # Timing advice
    if entry_score < -5:
        advice.append("⚠️  Entry Timing: Consider using limit orders at support levels rather than market orders.")
        advice.append("   Practice patience and wait for pullbacks before entering positions.")
    elif entry_score < -2:
        advice.append("✓ Entry Timing: Your timing is acceptable but can be improved with better technical analysis.")
    else:
        advice.append("✅ Entry Timing: Excellent execution! Keep using your current entry strategy.")
    
    # Risk management advice
    if timing_analysis['mae_percent'] < -10:
        advice.append("⚠️  Risk Management: The position showed significant adverse movement.")
        advice.append("   Consider tighter stop losses or better entry points to reduce drawdown.")
    
    # Behavioral advice
    if behavioral_analysis and behavioral_analysis['is_anomaly']:
        for anomaly in behavioral_analysis['anomalies']:
            if anomaly['type'] == 'position_size':
                if anomaly['z_score'] > 2:
                    advice.append("⚠️  Position Size: You're risking more than usual. Ensure this is intentional.")
                else:
                    advice.append("ℹ️  Position Size: Unusually small position. Consider if you're being too cautious.")
            elif anomaly['type'] == 'stock_beta':
                if anomaly['z_score'] > 2:
                    advice.append("⚠️  Risk Profile: This stock is significantly more volatile than your typical picks.")
                    advice.append("   Consider reducing position size to maintain consistent risk exposure.")
    
    if not advice:
        advice.append("✅ Overall: This trade aligns well with your profile. Continue executing with discipline!")
    
    for line in advice:
        print(f"  {line}")
    
    print("\n" + "=" * 80)
    print()


def main():
    """Main entry point for the Trading Coach application."""
    args = parse_arguments()
    
    try:
        # Initialize database if requested
        if args.init_db:
            print("Initializing database...")
            init_database()
            print()
        
        # Validate date format
        entry_date = validate_date(args.date)
        
        # Display progress
        print(f"\n🔍 Analyzing trade: {args.symbol} @ ${args.price:.2f} on {args.date}")
        
        if args.mock:
            print("⚠️  Note: Using mock data (--mock flag set)")
        
        print(f"📈 Fetching {args.horizon} days of historical market data...")
        
        # Fetch historical data
        if args.mock:
            # Use mock data
            df_historical = generate_mock_historical_data(args.symbol, args.horizon, base_price=args.price)
        else:
            # Try to use Tiger API
            try:
                from src.tiger_client import get_historical_data
                df_historical = get_historical_data(args.symbol, args.horizon)
            except Exception as e:
                print(f"⚠️  Tiger API error: {str(e)[:100]}...")
                print("⚠️  Falling back to mock data")
                df_historical = generate_mock_historical_data(args.symbol, args.horizon, base_price=args.price)
        
        if df_historical.empty:
            print(f"❌ Error: No historical data available for {args.symbol}")
            sys.exit(1)
        
        print(f"✓ Retrieved {len(df_historical)} data points")
        
        # Analyze trade timing
        print(f"⚙️  Analyzing entry timing...")
        timing_analysis = analyze_trade_timing(args.price, entry_date, df_historical)
        
        # Behavioral analysis (if behavioral data provided)
        behavioral_analysis = None
        if args.position_size and args.beta and args.sector:
            print(f"🧠 Analyzing behavioral patterns...")
            
            # Get trade history for comparison
            trade_history = get_trades_for_behavioral_analysis(50)
            
            if trade_history:
                current_trade = {
                    'position_size': args.position_size,
                    'stock_beta': args.beta,
                    'sector': args.sector
                }
                behavioral_analysis = detect_behavioral_anomaly(current_trade, trade_history)
            else:
                print("ℹ️  No historical trades found for behavioral comparison")
        
        # Save to database (unless --no-save flag is set)
        trade_id = None
        if not args.no_save:
            print(f"💾 Saving trade to database...")
            trade_id = save_trade(
                symbol=args.symbol,
                entry_price=args.price,
                entry_date=args.date,
                horizon=args.horizon,
                position_size=args.position_size,
                stock_beta=args.beta,
                sector=args.sector
            )
            
            # Save analyses
            save_analysis_result(trade_id, 'timing', timing_analysis)
            if behavioral_analysis:
                save_analysis_result(trade_id, 'behavioral', behavioral_analysis)
        
        # Print comprehensive coaching report
        print_coaching_report(
            symbol=args.symbol,
            entry_price=args.price,
            entry_date=args.date,
            timing_analysis=timing_analysis,
            behavioral_analysis=behavioral_analysis,
            trade_id=trade_id
        )
        
    except ValueError as e:
        print(f"\n❌ Validation Error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\n❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
