"""Test behavioral analysis with different investor profiles"""

from src.coach_logic import detect_behavioral_anomaly, format_behavioral_analysis
from src.database import get_last_n_trades

print("="*80)
print("BEHAVIORAL ANALYSIS TEST - Different Investor Profiles")
print("="*80)

# Define test scenarios for each profile
test_scenarios = {
    'Institutional Investor': {
        'trade_id_range': (14, 113),
        'test_trades': [
            {
                'name': 'Normal institutional trade',
                'trade': {'position_size': 500000, 'stock_beta': 1.2, 'sector': 'Technology'},
                'expected': 'Should pass - typical institutional trade'
            },
            {
                'name': 'Oversized position',
                'trade': {'position_size': 2000000, 'stock_beta': 1.2, 'sector': 'Technology'},
                'expected': 'Should flag - position 3-4x larger than normal'
            },
            {
                'name': 'High beta crypto play',
                'trade': {'position_size': 500000, 'stock_beta': 3.5, 'sector': 'Cryptocurrency'},
                'expected': 'Should flag - beta and sector anomalies'
            }
        ]
    },
    
    'Retail Speculative': {
        'trade_id_range': (114, 213),
        'test_trades': [
            {
                'name': 'Normal speculative trade',
                'trade': {'position_size': 5000, 'stock_beta': 2.5, 'sector': 'Technology'},
                'expected': 'Should pass - typical speculative trade'
            },
            {
                'name': 'Institutional-sized position',
                'trade': {'position_size': 50000, 'stock_beta': 2.5, 'sector': 'Technology'},
                'expected': 'Should flag - position 10x larger than normal'
            },
            {
                'name': 'Conservative bond position',
                'trade': {'position_size': 5000, 'stock_beta': 0.3, 'sector': 'Fixed Income'},
                'expected': 'Should flag - beta way too low for this trader'
            }
        ]
    },
    
    'Retail Conservative': {
        'trade_id_range': (214, 313),
        'test_trades': [
            {
                'name': 'Normal DCA trade',
                'trade': {'position_size': 2000, 'stock_beta': 1.0, 'sector': 'ETF'},
                'expected': 'Should pass - typical ETF investment'
            },
            {
                'name': 'High-risk speculative play',
                'trade': {'position_size': 2000, 'stock_beta': 3.2, 'sector': 'Cryptocurrency'},
                'expected': 'Should flag - beta and sector completely out of character'
            },
            {
                'name': 'Large concentrated bet',
                'trade': {'position_size': 10000, 'stock_beta': 1.8, 'sector': 'Technology'},
                'expected': 'Should flag - position size and beta anomalies'
            }
        ]
    }
}

# Test each profile
for profile_name, scenario in test_scenarios.items():
    print(f"\n{'='*80}")
    print(f"Testing Profile: {profile_name}")
    print(f"Trade ID Range: {scenario['trade_id_range'][0]} - {scenario['trade_id_range'][1]}")
    print(f"{'='*80}")
    
    # Get trade history for this profile
    start_id, end_id = scenario['trade_id_range']
    all_trades = get_last_n_trades(n=350)  # Get all trades
    
    # Filter trades for this profile
    profile_trades = [t for t in all_trades if start_id <= t['id'] <= end_id]
    
    if len(profile_trades) < 2:
        print(f"⚠️  Not enough trades found for profile (found {len(profile_trades)})")
        continue
    
    # Convert to format for behavioral analysis
    trade_history = [
        {
            'position_size': t['position_size'],
            'stock_beta': t['stock_beta'],
            'sector': t['sector']
        }
        for t in profile_trades
        if t['position_size'] and t['stock_beta'] and t['sector']
    ]
    
    print(f"✓ Loaded {len(trade_history)} historical trades")
    
    # Test each scenario
    for i, test in enumerate(scenario['test_trades'], 1):
        print(f"\n{'-'*80}")
        print(f"Test {i}: {test['name']}")
        print(f"Expected: {test['expected']}")
        print(f"{'-'*80}")
        
        # Run behavioral analysis
        result = detect_behavioral_anomaly(test['trade'], trade_history)
        
        # Print formatted analysis
        print(format_behavioral_analysis(result, test['trade']))

print("\n" + "="*80)
print("BEHAVIORAL ANALYSIS COMPLETE")
print("="*80)
print("\nKey Insights:")
print("1. Institutional: Flags large positions and crypto/high-beta plays")
print("2. Retail Speculative: Flags oversized positions and conservative plays")
print("3. Retail Conservative: Flags high-risk plays and large concentrated bets")
print("\nEach profile has distinct 'normal' behavior patterns!")
