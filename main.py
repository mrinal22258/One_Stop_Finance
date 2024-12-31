import requests
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
from datetime import datetime

# Class for currency conversion
class CurrencyConverter:
    API_KEY = "5015383d81-c795049103-soeb2d"
    
    @staticmethod
    def convert(from_currency, to_currency, amount):
        url = f"https://api.fastforex.io/convert?from={from_currency}&to={to_currency}&amount={amount}&api_key={CurrencyConverter.API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["result"].get(to_currency, "N/A")

# Class for crypto price retrieval
class CryptoPrice:
    API_KEY = "6122917b181462d0baf5008fddd84379"
    
    @staticmethod
    def get_price(crypto_code):
        url = f"http://api.coinlayer.com/live?access_key={CryptoPrice.API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["rates"].get(crypto_code, "N/A")

# Class for stock price retrieval
class StockPrice:
    API_KEY = "ctdk6u9r01qng9geqcggctdk6u9r01qng9geqch0"
    
    @staticmethod
    def get_prices(symbol):
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={StockPrice.API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "timestamp": int(datetime.now().timestamp() * 1000),
                "open": data["o"],
                "high": data["h"],
                "low": data["l"],
                "close": data["c"]
            }
        ]

# Class for news retrieval
class NewsFetcher:
    API_KEY = "pub_6219700cf21ae4a53bc16981ce4cddc2b7f4d"
    
    @staticmethod
    def get_news(topic):
        url = f"https://newsdata.io/api/1/news?apikey={NewsFetcher.API_KEY}&q={topic}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])

# Main Application Class
class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("One Stop Finance")
        self.root.geometry("700x550")
        self.root.configure(bg="lightgray")
        self.root.resizable(False, False)

        # Title label
        tk.Label(root, text="** ONE STOP FINANCE **", font=("Arial", 18, "bold"), fg="blue", bg="lightgray").pack(pady=15)

        # Frame for buttons
        button_frame = tk.Frame(root, bg="lightgray")
        button_frame.pack(pady=20)

        # Buttons for different functionalities
        ttk.Button(button_frame, text="Convert Currency", command=self.currency, width=30).grid(row=0, column=0, pady=10, padx=10)
        ttk.Button(button_frame, text="Get Crypto Price", command=self.crypto, width=30).grid(row=1, column=0, pady=10, padx=10)
        ttk.Button(button_frame, text="Get Stock Price", command=self.stock, width=30).grid(row=2, column=0, pady=10, padx=10)
        ttk.Button(button_frame, text="Get Latest News", command=self.news, width=30).grid(row=3, column=0, pady=10, padx=10)
        ttk.Button(button_frame, text="Exit", command=root.quit, width=30).grid(row=4, column=0, pady=10, padx=10)

    def show_input_window(self, title, prompt, default_value=""):
        input_window = Toplevel(self.root)
        input_window.title(title)
        input_window.geometry("300x150")
        input_window.resizable(False, False)
        input_window.grab_set()

        tk.Label(input_window, text=prompt, font=("Arial", 12)).pack(pady=10)
        entry = ttk.Entry(input_window, font=("Arial", 12))
        entry.insert(0, default_value)
        entry.pack(pady=5)

        result = {}

        def submit():
            result['value'] = entry.get()
            input_window.destroy()

        ttk.Button(input_window, text="Submit", command=submit).pack(pady=10)
        input_window.wait_window()
        return result.get('value')

    def currency(self):
        try:
            from_currency = self.show_input_window("Currency", "From (Currency code):")
            to_currency = self.show_input_window("Currency", "To (Currency code):")
            amount = self.show_input_window("Currency", "Amount (default 1):", "1")

            if not from_currency or not to_currency:
                raise ValueError("Currency codes cannot be empty.")

            converted_amount = CurrencyConverter.convert(from_currency, to_currency, float(amount))
            messagebox.showinfo("Currency Conversion", f"Converted Amount: {converted_amount}")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except requests.RequestException as re:
            messagebox.showerror("Network Error", f"Unable to fetch data: {str(re)})")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)})")

    def crypto(self):
        try:
            crypto_code = self.show_input_window("Crypto", "Crypto code (e.g., BTC, ETH):")
            if not crypto_code:
                raise ValueError("Crypto code cannot be empty.")

            price = CryptoPrice.get_price(crypto_code)
            if price == "N/A":
                raise ValueError("Invalid or unavailable crypto code.")

            messagebox.showinfo("Crypto Price", f"Price of {crypto_code}: {price}")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except requests.RequestException as re:
            messagebox.showerror("Network Error", f"Unable to fetch data: {str(re)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)})")

    def stock(self):
        try:
            symbol = self.show_input_window("Stock", "Symbol of the stock:")
            if not symbol:
                raise ValueError("Stock symbol cannot be empty.")

            stock_data = StockPrice.get_prices(symbol)
            if not stock_data:
                raise ValueError("Stock data not found.")

            stock_info = "\n\n".join(
                [
                    (f"Timestamp: {datetime.fromtimestamp(entry['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')}\n"
                     f"Open: {entry['open']}\n"
                     f"High: {entry['high']}\n"
                     f"Low: {entry['low']}\n"
                     f"Close: {entry['close']}")
                    for entry in stock_data
                ]
            )
            messagebox.showinfo("Stock Price", stock_info)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except requests.RequestException as re:
            messagebox.showerror("Network Error", f"Unable to fetch data: {str(re)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)})")

    def news(self):
        try:
            topic = self.show_input_window("News", "Enter topic for news:")
            if not topic:
                raise ValueError("Topic cannot be empty.")

            articles = NewsFetcher.get_news(topic)
            
            if not articles:
                raise ValueError("No articles found.")

            news_summary = "\n\n".join([f"{i+1}. {article['title']}\n{article['description']}"
                                           for i, article in enumerate(articles[:5])])
            messagebox.showinfo("News Articles", news_summary)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except requests.RequestException as re:
            messagebox.showerror("Network Error", f"Unable to fetch data: {str(re)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)})")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
