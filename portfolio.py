import json
import os

class Portfolio:
    def __init__(self, filename="portfolio.json"):
        self.filename = filename
        self.holdings = []
        self.load()
        
    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.holdings = json.load(f)
            except:
                self.holdings = []
        else:
            self.holdings = []
            
    def save(self):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w') as f:
            json.dump(self.holdings, f, indent=4)
            
    def add_holding(self, ticker, shares, buy_price):
        ticker = ticker.upper()
        # Check if already exists, if so average cost
        for h in self.holdings:
            if h['ticker'] == ticker:
                total_cost = (h['shares'] * h['buy_price']) + (shares * buy_price)
                h['shares'] += shares
                h['buy_price'] = total_cost / h['shares']
                return
        
        self.holdings.append({
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price
        })
        
    def remove_holding(self, ticker):
        ticker = ticker.upper()
        self.holdings = [h for h in self.holdings if h['ticker'] != ticker]
        
    def get_holdings(self):
        return self.holdings
