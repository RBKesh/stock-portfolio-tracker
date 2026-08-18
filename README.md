# 📈 Stock Portfolio Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2.36-green?style=for-the-badge)

A clean, modern stock portfolio tracker built with Python and Streamlit. This app lets you manage your stock holdings, calculates your profit and loss (P&L), and visualizes your asset allocation and gains/losses using Plotly charts. Real-time stock data is fetched via Yahoo Finance (`yfinance`).

## ✨ Features
- **Real-time Price Fetching:** Uses yfinance to get the latest stock prices.
- **Portfolio Management:** Add, edit, or remove holdings.
- **Cost Basis Calculation:** Automatically calculates average cost when buying more shares.
- **Interactive Charts:** 
  - Pie chart for portfolio allocation.
  - Bar chart showing absolute gains and losses per stock.
- **P&L Tracking:** See total unrealized profit/loss both in absolute dollars and percentages.
- **Export Data:** Export your portfolio data to a CSV file.

## 📸 Screenshots
*(Add screenshots here)*
- Dashboard View
- Add Stock View

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RBKesh/stock-portfolio-tracker.git
   cd stock-portfolio-tracker
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```
This will open the app in your default web browser (usually at `http://localhost:8501`).

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Financial Data:** yfinance
- **Visualization:** Plotly
- **Storage:** Local JSON file

## 📜 License
MIT License. Copyright (c) 2024 Rishi B.
