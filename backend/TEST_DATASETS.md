# Test Datasets - Investor Profiles Summary

## Overview

Generated 300 realistic trades across 3 distinct investor profiles to test behavioral analysis.

---

## Profile 1: Institutional Investor - Balanced, Tech Focused

**Trade IDs:** 14-113 (100 trades)  
**Date Range:** 2025-07-03 to 2025-12-30

### Characteristics
- **Position Size:** $200K - $1M (avg: $518K)
- **Beta Range:** 0.64 - 1.97 (avg: 1.18)
- **Investment Horizon:** 60 days

### Sector Distribution
- Technology: 69% (focus on AAPL, MSFT, GOOGL, AMZN, META, NVDA)
- Healthcare: 17% (JNJ, PFE)
- Finance: 10% (JPM, BAC)
- Energy: 4% (XOM)

### Behavioral Analysis Results

✅ **Normal Trade** (Position: $500K, Beta: 1.2, Tech)
- No anomalies detected
- Within expected institutional parameters

⚠️ **Oversized Position** (Position: $2M, Beta: 1.2, Tech)
- Flagged: 6.79 std dev above mean position size
- Warning: Position 4x larger than usual

⚠️ **High-Risk Crypto** (Position: $500K, Beta: 3.5, Crypto)
- Flagged: Beta 8.22 std dev above mean
- Warning: New sector (Cryptocurrency)
- Risk profile completely out of character

---

## Profile 2: Retail Investor - Speculative, Concept Stocks

**Trade IDs:** 114-213 (100 trades)  
**Date Range:** 2025-07-03 to 2025-12-30

### Characteristics
- **Position Size:** $1K - $15K (avg: $5.6K)
- **Beta Range:** 1.64 - 3.55 (avg: 2.39)
- **Investment Horizon:** 30 days

### Sector Distribution
- Technology: 54% (NVDA, AMD, PLTR, SNOW)
- Automotive: 26% (TSLA, RIVN, NIO)
- Finance: 18% (COIN, SOFI, HOOD)
- ETF: 2% (ARKK)

### Behavioral Analysis Results

✅ **Normal Speculative Trade** (Position: $5K, Beta: 2.5, Tech)
- No anomalies detected
- Typical high-risk, high-reward play

⚠️ **Institutional-Sized Position** (Position: $50K, Beta: 2.5, Tech)
- Flagged: 15.44 std dev above mean
- Warning: Position 10x larger than usual
- Risk management concern

⚠️ **Conservative Bond Play** (Position: $5K, Beta: 0.3, Fixed Income)
- Flagged: Beta 6.60 std dev below mean
- Warning: New sector
- Completely out of character for speculative trader

---

## Profile 3: Retail Investor - Conservative, DCA, ETFs

**Trade IDs:** 214-313 (100 trades)  
**Date Range:** 2025-07-03 to 2025-12-30

### Characteristics
- **Position Size:** $1K - $3.5K (avg: $2.2K)
- **Beta Range:** 0.28 - 1.27 (avg: 0.94)
- **Investment Horizon:** 90 days (long-term, DCA strategy)

### Sector Distribution
- ETF: 83% (SPY, VTI, QQQ, VOO, VIG, BND)
- Technology: 7% (AAPL)
- Healthcare: 4% (JNJ)
- Consumer: 3% (PG, KO)
- Telecom: 3% (T)

### Behavioral Analysis Results

✅ **Normal DCA Trade** (Position: $2K, Beta: 1.0, ETF)
- No anomalies detected
- Classic dollar-cost averaging into index funds

⚠️ **High-Risk Speculative Play** (Position: $2K, Beta: 3.2, Crypto)
- Flagged: Beta 10.32 std dev above mean
- Warning: New sector (Cryptocurrency)
- Extreme deviation from conservative strategy

⚠️ **Large Concentrated Bet** (Position: $10K, Beta: 1.8, Tech)
- Flagged: 2 anomalies
  - Position size: 9.25 std dev above mean (5x usual)
  - Beta: 3.91 std dev above mean
- Major departure from DCA strategy

---

## Key Insights

### 1. Profile-Specific Patterns
Each investor profile has distinct "normal" behavior:
- **Institutional:** Large positions, moderate risk, diversified
- **Speculative:** Small positions, high risk, concentrated
- **Conservative:** Small consistent positions, low risk, ETF-focused

### 2. Anomaly Detection Effectiveness
The system successfully identifies:
- **Position Size Anomalies:** 6.79 - 15.44 std dev
- **Risk Profile Changes:** 3.91 - 10.32 std dev in beta
- **Sector Drift:** New sectors flagged as warnings
- **Multi-Factor Anomalies:** Multiple flags for complex deviations

### 3. Coaching Applications
- **Risk Management:** Flags oversized positions early
- **Strategy Consistency:** Identifies behavioral drift
- **Emotional Trading:** Detects FOMO/panic trades
- **Portfolio Balance:** Warns about concentration risk

### 4. Statistical Rigor
- Uses 2 std dev threshold for anomaly detection
- Requires minimum 2 historical trades for analysis
- Calculates z-scores for precise deviation measurement
- Tracks sector exposure as behavioral indicator

---

## Usage Examples

```bash
# Test with institutional profile data (Trade IDs 14-113)
python main.py AAPL 275.00 2025-12-15 -p 500000 -b 1.2 -s Technology

# Test with speculative profile data (Trade IDs 114-213)
python main.py TSLA 385.00 2025-12-15 -p 5000 -b 2.5 -s Automotive

# Test with conservative profile data (Trade IDs 214-313)
python main.py SPY 600.00 2025-12-15 -p 2000 -b 1.0 -s ETF

# Run full behavioral test suite
python test_behavioral_profiles.py

# Generate new test data (warning: adds 300 more trades)
python generate_test_data.py
```

---

## Database Schema

**Trades Table (313 records)**
- Unique Symbols: 31
- Unique Sectors: 9
- Date Range: 2025-07-03 to 2025-12-30

**Trade Distribution**
- Institutional: 100 trades (~$518K avg position)
- Speculative: 100 trades (~$5.6K avg position)
- Conservative: 100 trades (~$2.2K avg position)

---

**Status:** Test datasets ready for behavioral analysis validation! ✅
