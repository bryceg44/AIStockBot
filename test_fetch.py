from utils.data_fetcher import fetch_stock_data

if __name__ == "__main__":
    symbol = "AAPL"
    start_date = "2024-06-01"
    end_date = "2024-12-3"
    data = fetch_stock_data(symbol, start_date, end_date)
    if data is not None:
        print(data.head())
