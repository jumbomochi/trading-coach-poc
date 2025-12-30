# Trading Coach

A full-stack trading analysis and coaching application with behavioral pattern detection.

## Project Structure

```
trading-coach-poc/
├── backend/                 # Python backend
│   ├── src/                # Core application code
│   │   ├── tiger_client.py # Tiger Brokers API integration
│   │   ├── coach_logic.py  # Trade analysis algorithms
│   │   ├── database.py     # SQLite database management
│   │   └── mock_data.py    # Mock data generator
│   ├── main.py             # CLI interface
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
│
├── frontend/               # Frontend applications
│   ├── streamlit/         # Streamlit dashboard (✅ Ready)
│   │   ├── app.py         # Interactive web dashboard
│   │   ├── requirements.txt
│   │   └── README.md
│   └── react/             # React frontend (🚧 In Development)
│       ├── src/           # React components
│       ├── package.json
│       └── README.md
│
└── README.md              # This file
```

## Features

### Backend ✅
- **Tiger Brokers API Integration** - Real-time and historical market data
- **Trade Timing Analysis** - MFE/MAE calculation and entry optimization
- **Behavioral Anomaly Detection** - Pattern recognition using statistical analysis
- **SQLite Database** - Persistent storage for trades and analysis results
- **CLI Interface** - Command-line tool for trade analysis

### Streamlit Dashboard ✅
- **Interactive Web UI** - User-friendly trade analysis interface
- **Real-time Candlestick Charts** - Visualize price action with Plotly
- **Entry Point Markers** - Visual indicators for your entry vs ideal entry
- **Behavioral Insights** - Anomaly detection with clear warnings
- **Trade History** - View recent trading activity

### React Frontend 🚧
- **Modern UI Components** - Professional React + TypeScript interface
- **Responsive Design** - Mobile-friendly layout
- **Type Safety** - Full TypeScript support
- **API Ready** - Awaiting backend REST API implementation

## Quick Start

### 1. Backend CLI

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Tiger API credentials
# Edit .env file with your Tiger Brokers credentials

# Run a trade analysis
python main.py AAPL 275.00 2025-12-15 -p 10000 -b 1.2 -s Technology
```

### 2. Streamlit Dashboard (Recommended)

```bash
# Install Streamlit (if not already installed)
pip install streamlit plotly

# Run the dashboard
cd frontend/streamlit
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

#### Streamlit Features
- 📊 Candlestick charts with entry markers
- 📈 Real-time timing analysis
- 🧠 Behavioral anomaly detection
- 📜 Trade history table
- 🎨 Clean, professional UI

### 3. React Frontend (Development)

```bash
cd frontend/react

# Install dependencies
npm install

# Start development server
npm run dev
```

Open `http://localhost:3000` to view the React app.

**Note**: React frontend requires a REST API backend (coming soon). Use Streamlit for full functionality.

### Test with Mock Data

```bash
cd backend
python main.py AAPL 275.00 2025-12-15 -p 10000 -b 1.2 -s Technology --mock
```

## Backend API

### CLI Usage
```bash
python main.py <SYMBOL> <PRICE> <DATE> [OPTIONS]

Options:
  -p, --position-size   Position size in dollars
  -b, --beta           Stock beta value
  -s, --sector         Stock sector
  -H, --horizon        Days of historical data (default: 30)
  --mock              Use mock data instead of Tiger API
  --no-save           Don't save to database
  --init-db           Initialize database
```

### Example Output

```
🎯 TRADING COACH REPORT
═══════════════════════════════════════════════════════════════════

📊 TRADE SUMMARY
Symbol:           AAPL
Entry Price:      $275.00
Entry Date:       2025-12-15

⏱️ TIMING EFFICIENCY ANALYSIS
Timing Score:     -2.93%
Verdict:          ✓ GOOD - Acceptable entry timing
Peak Potential:   +1.87%

🧠 BEHAVIORAL PATTERN ANALYSIS
Status:           ✅ NORMAL - Trade is within your typical patterns
Avg Position:     $518,221 (±$199,979)
Avg Beta:         1.15 (±0.28)

💼 COACHING ADVICE
✓ Entry Timing: Your timing is acceptable but can be improved
```

## Test Datasets

The backend includes 300 pre-generated trades across 3 investor profiles:

1. **Institutional Investor** (IDs 14-113) - $500K avg, low risk, tech-focused
2. **Retail Speculative** (IDs 114-213) - $5.6K avg, high risk, concept stocks
3. **Retail Conservative** (IDs 214-313) - $2.2K avg, low risk, ETFs

See [backend/TEST_DATASETS.md](backend/TEST_DATASETS.md) for details.

## Tech Stack

### Backend
- **Language:** Python 3.8+
- **API:** Tiger Brokers OpenAPI
- **Database:** SQLite3
- **Analysis:** Pandas, NumPy
- **CLI:** argparse

### Frontend (Planned)
- To be determined based on requirements
- Options: React, Vue, Next.js, Streamlit, or similar

## Documentation

- [Backend README](backend/README.md) - Detailed backend documentation
- [Test Summary](backend/TEST_SUMMARY.md) - Test results and validation
- [Test Datasets](backend/TEST_DATASETS.md) - Pre-generated test data
- [Tiger API Results](backend/TIGER_API_TEST_RESULTS.md) - API integration tests

## Development Status

### ✅ Backend Complete
- Tiger API integration
- Trade analysis algorithms
- Behavioral detection
- Database management
- CLI interface
- Test data generation

### 🚧 Frontend Next Steps
- Architecture planning
- Technology selection
- UI/UX design
- API endpoint design (REST or GraphQL)

## Project Roadmap

**Phase 1: Backend** ✅
- [x] Tiger API integration
- [x] Trade timing analysis (MFE/MAE)
- [x] Behavioral anomaly detection
- [x] Database and persistence
- [x] CLI interface
- [x] Test data generation

**Phase 2: Backend API** 🔄
- [ ] REST API with Flask/FastAPI
- [ ] Authentication and user management
- [ ] API documentation
- [ ] Rate limiting and caching

**Phase 3: Frontend** 📋
- [ ] Technology selection
- [ ] UI/UX design
- [ ] Dashboard implementation
- [ ] Real-time updates
- [ ] Mobile responsiveness

**Phase 4: Production** 📋
- [ ] Deployment strategy
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Performance optimization

## Contributing

This is a proof-of-concept project. For questions or suggestions, please open an issue.

## License

Private POC - All rights reserved
