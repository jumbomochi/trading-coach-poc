# Trading Coach Streamlit Dashboard

Interactive web dashboard for analyzing trades with AI-powered insights and behavioral pattern detection.

## Features

### 📊 Trade Analysis
- **Candlestick Chart**: Visual price action with entry point markers
- **Timing Metrics**: Entry timing score, MFE/MAE analysis, ideal entry price
- **Behavioral Detection**: Anomaly detection for position sizing and risk parameters

### 🔧 Input Form
- Trade entry details (ticker, price, date)
- Position parameters (size, beta, sector)
- Support for both real Tiger API data and mock data

### 📜 Trade History
- View last 5 trades
- Quick reference to past trading activity

## Quick Start

### 1. Install Dependencies
```bash
cd frontend/streamlit
pip install -r requirements.txt
```

Note: Backend dependencies must also be installed:
```bash
cd ../../backend
pip install -r requirements.txt
```

### 2. Configure Environment
Ensure the backend `.env` file is configured with Tiger API credentials:
```
tiger_id=your_tiger_id
private_key_pk1=your_private_key
account=your_account
```

### 3. Run the Dashboard
```bash
# From frontend/streamlit directory
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Usage

1. **Enter Trade Details**: Use the sidebar form to input your trade information
2. **Select Data Source**: Choose between Tiger API or mock data
3. **Analyze**: Click "🚀 Analyze Trade" to run the analysis
4. **Review Results**:
   - Check the timing score and key metrics
   - Examine the candlestick chart with entry markers
   - Review behavioral anomalies
   - View recent trade history

## Dashboard Sections

### Key Metrics
- **Timing Score**: How your entry compares to ideal timing
- **Ideal Entry**: The optimal entry price during the period
- **MFE %**: Maximum profit potential reached
- **MAE %**: Maximum drawdown from entry

### Price Chart
- Interactive candlestick chart
- 🔶 Gold diamond: Your entry point
- ⭐ Green star: Ideal entry point
- Green dashed line: Maximum Favorable Excursion

### Timing Analysis
- Entry quality verdict (Excellent/Good/Fair/Poor)
- Detailed breakdown of missed opportunities
- Profit potential analysis

### Behavioral Analysis
- Anomaly detection (position size, stock beta)
- Z-score calculations vs historical trading behavior
- Sector exposure warnings
- Actionable tips for unusual patterns

## Mock Data Mode

For testing without Tiger API access:
- Check "Use Mock Data" in the sidebar
- System generates realistic OHLCV data
- All analysis features work identically

## Data Flow

```
Streamlit UI → Tiger API/Mock → Coach Logic → Analysis → Database → Display
```

1. User inputs trade in sidebar form
2. Fetch historical data (Tiger API or mock)
3. Run timing and behavioral analysis
4. Save trade and results to SQLite database
5. Display visualizations and insights

## Troubleshooting

**Import Errors**: Ensure backend is in Python path. The app automatically adds it, but if issues persist:
```python
import sys
sys.path.insert(0, '/absolute/path/to/backend')
```

**Tiger API Connection**: Check `.env` credentials and internet connection

**Database Issues**: Database is automatically initialized. Located at `backend/trading_coach.db`

**Empty Charts**: Verify date range includes trading days. Use mock data to test functionality.

## Customization

### Styling
Edit CSS in `st.markdown()` section for custom colors and fonts

### Metrics
Modify threshold values in coach_logic.py (default: 2 standard deviations)

### Chart Types
Replace Plotly candlestick with line/area charts as needed

## Performance

- Lightweight: <5MB memory footprint
- Fast: Sub-second analysis times
- Responsive: Real-time chart updates

## Next Steps

- Add multi-trade comparison view
- Implement portfolio-level risk analysis
- Export reports to PDF
- Integration with React frontend via API
