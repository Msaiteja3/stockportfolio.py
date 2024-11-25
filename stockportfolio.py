import requests

class StockPortfolio:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}  # Stores stocks with ticker as key and details as value

    def add_stock(self, ticker, quantity, buy_price):
        """Add a stock to the portfolio."""
        self.portfolio[ticker] = {
            'quantity': quantity,
            'buy_price': buy_price,
        }
        print(f"Added {ticker} to portfolio.")

    def remove_stock(self, ticker):
        """Remove a stock from the portfolio."""
        if ticker in self.portfolio:
            del self.portfolio[ticker]
            print(f"Removed {ticker} from portfolio.")
        else:
            print(f"{ticker} is not in the portfolio.")

    def fetch_stock_price(self, ticker):
        """Fetch the real-time price of a stock using Alpha Vantage."""
        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.api_key,
        }
        response = requests.get(url, params=params)
        data = response.json()

        try:
            price = float(data['Global Quote']['05. price'])
            return price
        except KeyError:
            print(f"Could not fetch data for {ticker}.")
            return None

    def view_portfolio(self):
        """Display portfolio with current values and performance."""
        if not self.portfolio:
            print("Your portfolio is empty.")
            return

        print(f"{'Ticker':<10} {'Quantity':<10} {'Buy Price':<10} {'Current Price':<15} {'Value':<10} {'P/L'}")
        total_value = 0
        total_cost = 0
        for ticker, details in self.portfolio.items():
            current_price = self.fetch_stock_price(ticker)
            if current_price is None:
                continue

            quantity = details['quantity']
            buy_price = details['buy_price']
            value = quantity * current_price
            cost = quantity * buy_price
            pl = value - cost

            total_value += value
            total_cost += cost

            print(f"{ticker:<10} {quantity:<10} {buy_price:<10.2f} {current_price:<15.2f} {value:<10.2f} {pl:.2f}")

        print(f"\nTotal Portfolio Value: {total_value:.2f}")
        print(f"Total Cost: {total_cost:.2f}")
        print(f"Overall P/L: {total_value - total_cost:.2f}")

# Initialize the portfolio tool
api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
portfolio = StockPortfolio(api_key)

# Menu for user interaction
while True:
    print("\nStock Portfolio Tracker")
    print("1. Add Stock")
    print("2. Remove Stock")
    print("3. View Portfolio")
    print("4. Exit")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        ticker = input("Enter stock ticker: ").upper()
        quantity = int(input("Enter quantity: "))
        buy_price = float(input("Enter buy price: "))
        portfolio.add_stock(ticker, quantity, buy_price)
    elif choice == "2":
        ticker = input("Enter stock ticker to remove: ").upper()
        portfolio.remove_stock(ticker)
    elif choice == "3":
        portfolio.view_portfolio()
    elif choice == "4":
        print("Exiting the portfolio tracker.")
        break
    else:
        print("Invalid choice. Please try again.")
