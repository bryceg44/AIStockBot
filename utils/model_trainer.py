import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

MODEL_PATH = os.path.join('models', 'stock_model.pkl')

def train_model(df):
    # Define target variable (next day's close price)
    df['target'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    # Features
    features = ['ema_20', 'ema_50', 'rsi', 'macd', 'macdsignal', 'volume']

    X = df[features]
    y = df['target']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    score = model.score(X_test, y_test)
    print(f"Model R^2 Score: {score:.2f}")

    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    return model
