# Project Structure - Trading Coach

## Overview
```
trading-coach-poc/
├── backend/                 # Python backend application
├── frontend/               # Frontend application (to be built)
├── .venv/                  # Shared Python virtual environment
├── README.md              # Project overview
└── .gitignore             # Git ignore rules
```

## Backend Structure

```
backend/
├── src/                   # Core application modules
│   ├── __init__.py       
│   ├── tiger_client.py   # Tiger Brokers API client
│   ├── coach_logic.py    # Trade analysis algorithms
│   ├── database.py       # SQLite database management
│   └── mock_data.py      # Mock data generator for testing
│
├── main.py               # CLI interface
├── generate_test_data.py # Test dataset generator
├── test_behavioral_profiles.py  # Behavioral testing script
│
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
├── tiger_openapi_config.properties  # Tiger API config (not in git)
├── trading_coach.db      # SQLite database (not in git)
│
├── README.md            # Backend documentation
├── TEST_SUMMARY.md      # Test results
├── TEST_DATASETS.md     # Test data documentation
└── TIGER_API_TEST_RESULTS.md  # API integration tests
```

## Frontend Structure (Planned)

```
frontend/
├── src/                  # Source code
│   ├── components/      # React/Vue components
│   ├── pages/           # Page components
│   ├── api/             # API client
│   ├── utils/           # Utility functions
│   └── styles/          # CSS/styling
│
├── public/              # Static assets
├── package.json         # Node dependencies
└── README.md           # Frontend documentation
```

## Core Modules

### Backend: `src/tiger_client.py`
**Purpose:** Tiger Brokers API integration
- `TigerClientManager` class - Manages API connection
- `get_historical_data()` - Fetches daily bars

**Key Features:**
- Environment variable configuration
- Market data retrieval
- Error handling and fallback

### Backend: `src/coach_logic.py`
**Purpose:** Trade analysis and behavioral detection
- `analyze_trade_timing()` - Calculate MFE/MAE
- `detect_behavioral_anomaly()` - Pattern recognition
- `format_trade_analysis()` - Report generation

**Key Features:**
- Statistical analysis (mean, std dev, z-scores)
- 2 sigma threshold for anomalies
- Multi-factor detection (position size, beta, sector)

### Backend: `src/database.py`
**Purpose:** SQLite database management
- `init_database()` - Create tables and indexes
- `save_trade()` - Store trade records
- `save_analysis_result()` - Store analysis outputs
- `get_last_n_trades()` - Retrieve trade history

**Tables:**
- `trades` - Trade records with position size, beta, sector
- `analysis_results` - JSON-stored analysis outputs

### Backend: `src/mock_data.py`
**Purpose:** Generate realistic test data
- `generate_mock_historical_data()` - OHLCV bars
- Consistent seed for reproducibility
- Configurable volatility and volume

## Shared Resources

### Python Virtual Environment
Located at project root: `.venv/`
- Shared between backend and any Python-based tools
- Install: `python -m venv .venv`
- Activate: `source .venv/bin/activate`

### Database
Located at: `backend/trading_coach.db`
- SQLite3 database
- 300+ test trades across 3 profiles
- Analysis history

### Configuration Files

**`.env`** (backend/)
```env
tiger_id=your_id
private_key_pk1=your_key
account=your_account
```

**`tiger_openapi_config.properties`** (backend/)
```properties
tiger_id=20154444
private_key_pk1=...
account=
license=TBSG
env=PROD
```

## Running the Application

### Backend CLI
```bash
cd backend
source ../.venv/bin/activate
python main.py AAPL 275.00 2025-12-15 -p 10000 -b 1.2 -s Technology
```

### Generate Test Data
```bash
cd backend
source ../.venv/bin/activate
python generate_test_data.py
```

### Test Behavioral Profiles
```bash
cd backend
source ../.venv/bin/activate
python test_behavioral_profiles.py
```

## Development Workflow

### Backend Development
1. Navigate to `backend/`
2. Activate venv: `source ../.venv/bin/activate`
3. Make changes to Python files
4. Test with `python main.py ...`
5. Run tests with test scripts

### Frontend Development (Coming Soon)
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`
4. Build for production: `npm run build`

## API Design (Planned)

### REST Endpoints
```
POST   /api/trades              # Create new trade
GET    /api/trades              # Get trade history
GET    /api/trades/:id          # Get trade details
POST   /api/trades/:id/analyze  # Run analysis
GET    /api/profiles            # Get investor profiles
GET    /api/stats               # Get statistics
```

### WebSocket (Optional)
```
ws://localhost:8000/ws/trades   # Real-time updates
```

## Testing Strategy

### Unit Tests
- `tests/` directory (to be created)
- Test each module independently
- Mock external dependencies

### Integration Tests
- Test end-to-end workflows
- Use test database
- Verify API endpoints

### Test Data
- 3 investor profiles (100 trades each)
- Institutional, speculative, conservative
- Covers edge cases and anomalies

## Deployment Considerations

### Backend
- Python 3.8+ required
- PostgreSQL for production (replace SQLite)
- Environment variables for secrets
- Containerization with Docker

### Frontend
- Static hosting (Vercel, Netlify)
- API proxy configuration
- Environment-specific builds
- CDN for assets

## Security Considerations

- ✅ API keys in `.env` (not in git)
- ✅ Database credentials secured
- 🔄 Add API authentication (JWT)
- 🔄 Input validation and sanitization
- 🔄 Rate limiting
- 🔄 CORS configuration

## Performance Optimization

### Backend
- Database indexing (already implemented)
- Query optimization
- Caching for repeated analyses
- Async processing for heavy computations

### Frontend
- Code splitting
- Lazy loading components
- Optimized bundle size
- Service worker for offline support

## Monitoring & Logging

- Application logs
- Error tracking (Sentry)
- Performance monitoring
- User analytics
- Database query profiling

---

**Status:** Backend complete ✅ | Frontend ready for development 🚧
