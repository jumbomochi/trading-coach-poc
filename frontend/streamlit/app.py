"""Trading Coach Streamlit Dashboard"""

import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Add backend to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.join(backend_path, 'src'))

from src.tiger_client import TigerClientManager
from src.coach_logic import analyze_trade_timing, detect_behavioral_anomaly
from src.database import init_database, save_trade, save_analysis_result, get_last_n_trades, get_trades_for_behavioral_analysis

# Initialize database
init_database()

# Page configuration
st.set_page_config(
    page_title="Trading Coach Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .trade-info {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">📈 Trading Coach Dashboard</p>', unsafe_allow_html=True)
st.markdown("Analyze your trades with AI-powered insights and behavioral pattern detection")

# Sidebar - Trade Input Form
st.sidebar.header("🔧 Log New Trade")

with st.sidebar.form("trade_form"):
    st.subheader("Trade Details")
    
    # Input fields
    ticker = st.text_input("Ticker Symbol", value="AAPL", help="Stock ticker symbol (e.g., AAPL, TSLA)")
    entry_price = st.number_input("Entry Price ($)", min_value=0.01, value=150.00, step=0.01)
    entry_date = st.date_input(
        "Entry Date",
        value=datetime.now() - timedelta(days=7),
        max_value=datetime.now()
    )
    
    horizon = st.selectbox(
        "Horizon (days)",
        options=[7, 30, 90],
        index=0,
        help="Analysis period from entry date"
    )
    
    st.divider()
    
    st.subheader("Position Details")
    position_size = st.number_input(
        "Position Size ($)",
        min_value=0.0,
        value=10000.00,
        step=100.00,
        help="Total dollar value of the position"
    )
    
    stock_beta = st.number_input(
        "Stock Beta",
        min_value=0.0,
        max_value=5.0,
        value=1.2,
        step=0.1,
        help="Stock's beta (market sensitivity)"
    )
    
    sector = st.text_input(
        "Sector",
        value="Technology",
        help="Industry sector of the stock"
    )
    
    st.divider()
    
    use_mock = st.checkbox(
        "Use Mock Data",
        value=False,
        help="Use simulated data instead of Tiger API"
    )
    
    # Submit button
    analyze_button = st.form_submit_button("🚀 Analyze Trade", use_container_width=True)

# Main content area
if analyze_button:
    with st.spinner("🔍 Analyzing trade..."):
        try:
            # Fetch historical data
            if use_mock:
                # Use mock data
                from src.mock_data import generate_mock_historical_data
                df_historical = generate_mock_historical_data(
                    base_price=entry_price,
                    num_days=horizon + 10,
                    volatility=0.02
                )
                st.info("ℹ️ Using mock data for analysis")
            else:
                # Use Tiger API
                tiger_client = TigerClientManager()
                df_historical = tiger_client.get_historical_data(
                    symbol=ticker,
                    horizon_days=horizon + 10
                )
                st.success(f"✅ Fetched {len(df_historical)} days of market data from Tiger API")
            
            # Validate data
            if df_historical.empty:
                st.error("❌ No historical data available. Try using mock data instead.")
                st.stop()
            
            # Run trade timing analysis
            # Convert date to pandas datetime for compatibility
            entry_datetime = pd.to_datetime(entry_date)
            timing_analysis = analyze_trade_timing(
                entry_price=entry_price,
                entry_date=entry_datetime,
                df_historical=df_historical
            )
            
            # Get trade history for behavioral analysis
            trade_history = get_trades_for_behavioral_analysis()
            
            # Run behavioral analysis
            current_trade = {
                'position_size': position_size,
                'stock_beta': stock_beta,
                'sector': sector
            }
            behavioral_analysis = detect_behavioral_anomaly(current_trade, trade_history)
            
            # Save trade to database
            trade_id = save_trade(
                symbol=ticker,
                entry_price=entry_price,
                entry_date=entry_date,
                horizon=horizon,
                position_size=position_size,
                stock_beta=stock_beta,
                sector=sector
            )
            
            # Save analysis results
            save_analysis_result(trade_id, 'timing', timing_analysis)
            save_analysis_result(trade_id, 'behavioral', behavioral_analysis)
            
            st.success(f"✅ Trade #{trade_id} saved to database")
            
            # === VISUALIZATIONS ===
            
            # Create three columns for key metrics
            st.markdown("---")
            st.subheader("📊 Key Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                timing_score = timing_analysis['entry_timing_score']
                delta_color = "normal" if timing_score >= -5 else "off"
                st.metric(
                    "Timing Score",
                    f"{timing_score:.2f}%",
                    delta=f"{timing_score:.2f}%",
                    delta_color=delta_color,
                    help="How much worse (negative) or better (positive) your entry was vs ideal"
                )
            
            with col2:
                st.metric(
                    "Ideal Entry",
                    f"${timing_analysis['ideal_entry']:.2f}",
                    delta=f"${timing_analysis['ideal_entry'] - entry_price:.2f}",
                    delta_color="inverse",
                    help="The best possible entry price during the period"
                )
            
            with col3:
                mfe_percent = timing_analysis['mfe_percent']
                st.metric(
                    "MFE %",
                    f"{mfe_percent:.2f}%",
                    delta=f"{mfe_percent:.2f}%",
                    delta_color="normal" if mfe_percent > 0 else "off",
                    help="Maximum Favorable Excursion - peak profit potential"
                )
            
            with col4:
                mae_percent = timing_analysis['mae_percent']
                st.metric(
                    "MAE %",
                    f"{mae_percent:.2f}%",
                    delta=f"{mae_percent:.2f}%",
                    delta_color="inverse",
                    help="Maximum Adverse Excursion - maximum drawdown"
                )
            
            # Candlestick Chart
            st.markdown("---")
            st.subheader("📈 Price Action Chart")
            
            # Filter data from entry date
            df_chart = df_historical[df_historical['date'] >= pd.to_datetime(entry_date)].copy()
            
            # Create candlestick chart
            fig = go.Figure()
            
            # Add candlestick
            fig.add_trace(go.Candlestick(
                x=df_chart['date'],
                open=df_chart['open'],
                high=df_chart['high'],
                low=df_chart['low'],
                close=df_chart['close'],
                name='Price',
                increasing_line_color='#26a69a',
                decreasing_line_color='#ef5350'
            ))
            
            # Add entry point marker
            entry_datetime = pd.to_datetime(entry_date)
            fig.add_trace(go.Scatter(
                x=[entry_datetime],
                y=[entry_price],
                mode='markers',
                marker=dict(
                    symbol='diamond',
                    size=20,
                    color='gold',
                    line=dict(color='darkgoldenrod', width=2)
                ),
                name=f'Entry: ${entry_price:.2f}',
                hovertemplate=f'<b>Your Entry</b><br>Price: ${entry_price:.2f}<br>Date: {entry_date}<extra></extra>'
            ))
            
            # Add ideal entry marker (MAE)
            ideal_entry_price = timing_analysis['ideal_entry']
            mae_date = df_chart[df_chart['low'] == df_chart['low'].min()]['date'].iloc[0]
            fig.add_trace(go.Scatter(
                x=[mae_date],
                y=[ideal_entry_price],
                mode='markers',
                marker=dict(
                    symbol='star',
                    size=18,
                    color='lime',
                    line=dict(color='darkgreen', width=2)
                ),
                name=f'Ideal Entry: ${ideal_entry_price:.2f}',
                hovertemplate=f'<b>Ideal Entry</b><br>Price: ${ideal_entry_price:.2f}<br>Date: {mae_date.strftime("%Y-%m-%d")}<extra></extra>'
            ))
            
            # Add MFE line
            mfe_price = timing_analysis['mfe']
            fig.add_hline(
                y=mfe_price,
                line_dash="dash",
                line_color="green",
                annotation_text=f"MFE: ${mfe_price:.2f}",
                annotation_position="right"
            )
            
            # Update layout
            fig.update_layout(
                title=f"{ticker} - {horizon} Day Analysis Period",
                yaxis_title="Price ($)",
                xaxis_title="Date",
                height=600,
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                ),
                xaxis_rangeslider_visible=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Analysis Details
            st.markdown("---")
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("⏱️ Timing Analysis")
                
                # Timing verdict
                if timing_score >= 0:
                    st.success(f"✅ **EXCELLENT** - You entered at or below the ideal price!")
                elif timing_score >= -5:
                    st.info(f"ℹ️ **GOOD** - Your entry was close to optimal")
                elif timing_score >= -10:
                    st.warning(f"⚠️ **FAIR** - Entry timing could be improved")
                else:
                    st.error(f"❌ **POOR** - Entry was significantly above ideal price")
                
                st.write("**Details:**")
                st.write(f"- Actual Entry: **${entry_price:.2f}**")
                st.write(f"- Ideal Entry: **${timing_analysis['ideal_entry']:.2f}**")
                st.write(f"- Difference: **${entry_price - timing_analysis['ideal_entry']:.2f}**")
                st.write(f"- Maximum Favorable Excursion: **${mfe_price:.2f}** (+{mfe_percent:.2f}%)")
                st.write(f"- Maximum Adverse Excursion: **${timing_analysis['mae']:.2f}** ({mae_percent:.2f}%)")
                st.write(f"- Missed Profit Potential: **{timing_analysis['missed_profit_potential']:.2f}%**")
            
            with col_right:
                st.subheader("🧠 Behavioral Analysis")
                
                # Behavioral verdict
                if behavioral_analysis['is_anomaly']:
                    st.warning(f"⚠️ **ANOMALIES DETECTED** - {len(behavioral_analysis['anomalies'])} issue(s) found")
                    
                    for i, anomaly in enumerate(behavioral_analysis['anomalies'], 1):
                        with st.expander(f"🔴 Anomaly {i}: {anomaly['type'].replace('_', ' ').title()}"):
                            st.write(f"**{anomaly['message']}**")
                            st.write(f"- Current Value: **{anomaly['current_value']:,.2f}**")
                            st.write(f"- Historical Mean: **{anomaly['historical_mean']:,.2f}**")
                            st.write(f"- Z-Score: **{anomaly['z_score']:.2f}σ**")
                            
                            if anomaly['type'] == 'position_size':
                                if anomaly['z_score'] > 0:
                                    st.info("💡 **Tip**: This position is unusually large. Ensure you have adequate risk management in place.")
                                else:
                                    st.info("💡 **Tip**: This position is unusually small compared to your typical trades. Consider if this aligns with your strategy.")
                            elif anomaly['type'] == 'stock_beta':
                                if anomaly['z_score'] > 0:
                                    st.info("💡 **Tip**: This stock is significantly more volatile than your usual picks. Be prepared for larger price swings.")
                                else:
                                    st.info("💡 **Tip**: This stock is less volatile than your usual picks. Returns may be more modest.")
                else:
                    st.success("✅ **WITHIN NORMAL PARAMETERS**")
                    st.write("This trade aligns with your typical trading behavior:")
                    
                    if behavioral_analysis['metrics']:
                        if 'position_size_mean' in behavioral_analysis['metrics']:
                            st.write(f"- Position Size: ${position_size:,.2f} (avg: ${behavioral_analysis['metrics']['position_size_mean']:,.2f})")
                        if 'stock_beta_mean' in behavioral_analysis['metrics']:
                            st.write(f"- Stock Beta: {stock_beta:.2f} (avg: {behavioral_analysis['metrics']['stock_beta_mean']:.2f})")
                
                # Warnings
                if behavioral_analysis['warnings']:
                    st.markdown("---")
                    st.write("**⚡ Warnings:**")
                    for warning in behavioral_analysis['warnings']:
                        if isinstance(warning, dict):
                            st.warning(f"🆕 {warning['message']}")
                            if 'known_sectors' in warning:
                                st.caption(f"Your typical sectors: {', '.join(warning['known_sectors'])}")
                        else:
                            st.info(warning)
        
        except Exception as e:
            st.error(f"❌ Error analyzing trade: {str(e)}")
            st.exception(e)

# History View
st.markdown("---")
st.subheader("📜 Recent Trade History")

try:
    recent_trades = get_last_n_trades(n=5)
    
    if recent_trades:
        # Convert to DataFrame for display
        history_df = pd.DataFrame(recent_trades)
        
        # Format columns
        history_df['entry_date'] = pd.to_datetime(history_df['entry_date']).dt.strftime('%Y-%m-%d')
        history_df['entry_price'] = history_df['entry_price'].apply(lambda x: f"${x:.2f}")
        history_df['position_size'] = history_df['position_size'].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
        history_df['stock_beta'] = history_df['stock_beta'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        
        # Rename columns
        history_df = history_df.rename(columns={
            'id': 'ID',
            'symbol': 'Symbol',
            'entry_price': 'Entry Price',
            'entry_date': 'Entry Date',
            'horizon': 'Horizon',
            'position_size': 'Position Size',
            'stock_beta': 'Beta',
            'sector': 'Sector'
        })
        
        # Display table
        st.dataframe(
            history_df[['ID', 'Symbol', 'Entry Price', 'Entry Date', 'Horizon', 'Position Size', 'Beta', 'Sector']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No trade history yet. Analyze your first trade to get started!")
        
except Exception as e:
    st.error(f"Error loading trade history: {str(e)}")

# Footer
st.markdown("---")
st.caption("🤖 Trading Coach powered by Tiger Brokers API | Data analysis using statistical behavioral detection")
