# Trading Coach React Frontend

Modern React + TypeScript frontend for the Trading Coach application.

## Status

🚧 **In Development** - UI components ready, backend API integration pending

## Features

### ✅ Completed
- **Trade Input Form**: Complete form with validation
- **Analysis Display Components**: 
  - Timing analysis card with verdict system
  - Behavioral analysis with anomaly detection
  - Responsive metric displays
- **Modern UI**: Clean, professional design with Vite + React + TypeScript
- **Type Safety**: Full TypeScript definitions for all data structures

### 🚧 Pending
- **Backend REST API**: Need FastAPI/Flask endpoints
- **Data Visualization**: Candlestick chart component
- **Trade History**: List and detail views

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Create a `.env` file:
```bash
VITE_API_URL=http://localhost:5000/api
```

### 3. Run Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## Project Structure

```
src/
├── components/          # React components
│   ├── TradeForm.tsx
│   ├── TimingAnalysisCard.tsx
│   ├── BehavioralAnalysisCard.tsx
│   └── *.css
├── types.ts            # TypeScript definitions
├── api.ts              # API client
├── App.tsx             # Main app
└── main.tsx            # Entry point
```

## Current Status: Use Streamlit

Until the REST API backend is ready, use the Streamlit dashboard for full functionality:

```bash
cd ../streamlit
streamlit run app.py
```

## Technology Stack

- React 18 + TypeScript
- Vite (Fast build tool)
- Axios (HTTP client)

## Next Steps

1. Create FastAPI backend with REST endpoints
2. Add candlestick chart visualization
3. Implement trade history view
4. Connect frontend to API
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
