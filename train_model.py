from utils.data_fetcher import fetch_stock_data
from utils.data_processor import add_technical_indicators
from utils.model_trainer import train_model

if __name__ == "__main__":
    symbol = "AAPL"
    start_date = "2024-01-01"
    end_date = "2024-12-04"
    data = fetch_stock_data(symbol, start_date, end_date)
    if data is not None:
        data = add_technical_indicators(data)
        model = train_model(data)
