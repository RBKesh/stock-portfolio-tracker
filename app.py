import streamlit as st
import pandas as pd
import yfinance as yf
from portfolio import Portfolio
import charts
from utils import format_currency, format_percent, get_color

st.set_page_config(page_title="Stock Portfolio Tracker", page_icon="📈", layout="wide")

# Initialize portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = Portfolio('data/sample_portfolio.json')

def load_data():
    return st.session_state.portfolio

portfolio = load_data()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Manage Portfolio", "Export"])

@st.cache_data(ttl=300)
def fetch_current_prices(tickers):
    prices = {}
    if not tickers:
        return prices
    try:
        data = yf.download(tickers, period="1d", group_by='ticker')
        if len(tickers) == 1:
            prices[tickers[0]] = float(data['Close'].iloc[-1])
        else:
            for ticker in tickers:
                prices[ticker] = float(data[ticker]['Close'].iloc[-1])
    except Exception as e:
        st.error(f"Error fetching prices: {e}")
    return prices

if page == "Dashboard":
    st.title("📈 Stock Portfolio Dashboard")
    
    holdings = portfolio.get_holdings()
    if not holdings:
        st.info("Your portfolio is empty. Go to 'Manage Portfolio' to add some stocks.")
    else:
        tickers = [h['ticker'] for h in holdings]
        current_prices = fetch_current_prices(tickers)
        
        total_value = 0
        total_cost = 0
        
        portfolio_data = []
        
        for h in holdings:
            ticker = h['ticker']
            shares = h['shares']
            cost_basis = h['buy_price']
            
            current_price = current_prices.get(ticker, cost_basis)
            current_value = current_price * shares
            total_cost_basis = cost_basis * shares
            
            unrealized_gl = current_value - total_cost_basis
            unrealized_gl_pct = (unrealized_gl / total_cost_basis) * 100 if total_cost_basis > 0 else 0
            
            total_value += current_value
            total_cost += total_cost_basis
            
            portfolio_data.append({
                "Ticker": ticker,
                "Shares": shares,
                "Avg Cost": cost_basis,
                "Current Price": current_price,
                "Total Value": current_value,
                "P&L ($)": unrealized_gl,
                "P&L (%)": unrealized_gl_pct
            })
            
        total_gl = total_value - total_cost
        total_gl_pct = (total_gl / total_cost) * 100 if total_cost > 0 else 0
        
        # Top metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Value", format_currency(total_value), f"{format_currency(total_gl)}")
        with col2:
            st.metric("Total P&L %", format_percent(total_gl_pct), f"{format_percent(total_gl_pct)}")
        with col3:
            st.metric("Total Cost", format_currency(total_cost))
            
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Asset Allocation")
            fig_pie = charts.plot_allocation([d["Ticker"] for d in portfolio_data], [d["Total Value"] for d in portfolio_data])
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.subheader("Gains & Losses by Stock")
            fig_bar = charts.plot_gains_losses([d["Ticker"] for d in portfolio_data], [d["P&L ($)"] for d in portfolio_data])
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.subheader("Portfolio Breakdown")
        
        # Format df for display
        df = pd.DataFrame(portfolio_data)
        df_display = df.copy()
        df_display["Avg Cost"] = df_display["Avg Cost"].apply(format_currency)
        df_display["Current Price"] = df_display["Current Price"].apply(format_currency)
        df_display["Total Value"] = df_display["Total Value"].apply(format_currency)
        df_display["P&L ($)"] = df_display["P&L ($)"].apply(format_currency)
        df_display["P&L (%)"] = df_display["P&L (%)"].apply(format_percent)
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)

elif page == "Manage Portfolio":
    st.title("⚙️ Manage Portfolio")
    
    st.subheader("Add / Buy Stock")
    with st.form("add_stock_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker_input = st.text_input("Ticker Symbol (e.g. AAPL)").upper()
        with col2:
            shares_input = st.number_input("Number of Shares", min_value=0.01, value=1.0)
        with col3:
            price_input = st.number_input("Buy Price ($)", min_value=0.01, value=100.0)
            
        submitted = st.form_submit_button("Add to Portfolio")
        if submitted:
            if ticker_input:
                try:
                    # Validate ticker
                    info = yf.Ticker(ticker_input).info
                    if 'regularMarketPrice' in info or 'currentPrice' in info or 'previousClose' in info:
                        portfolio.add_holding(ticker_input, shares_input, price_input)
                        st.success(f"Added {shares_input} shares of {ticker_input} at ${price_input}")
                        portfolio.save()
                    else:
                        st.error("Invalid ticker symbol.")
                except:
                    st.error("Invalid ticker symbol or API error.")
            else:
                st.error("Please enter a ticker symbol.")
                
    st.subheader("Current Holdings")
    holdings = portfolio.get_holdings()
    if holdings:
        for idx, h in enumerate(holdings):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"**{h['ticker']}**")
            with col2:
                st.write(f"{h['shares']} shares")
            with col3:
                st.write(f"${h['buy_price']} avg cost")
            with col4:
                if st.button("Remove", key=f"remove_{idx}"):
                    portfolio.remove_holding(h['ticker'])
                    portfolio.save()
                    st.rerun()
    else:
        st.write("No holdings yet.")

elif page == "Export":
    st.title("📥 Export Data")
    
    holdings = portfolio.get_holdings()
    if holdings:
        df = pd.DataFrame(holdings)
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Portfolio as CSV",
            data=csv,
            file_name='portfolio_export.csv',
            mime='text/csv',
        )
    else:
        st.info("No data to export.")
