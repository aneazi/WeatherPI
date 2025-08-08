from feature_utils import prepare_data
import sqlite3
import pandas as pd
from pathlib import Path
import joblib
from sklearn.ensemble import IsolationForest
import time
import os
import yaml

def load_config(path: str) -> dict:
    # If path is not absolute, assume it's relative to the current working directory
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def load_data(db_path: Path) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT timestamp, temperature, pressure, humidity FROM weather_data", conn)
    conn.close()
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = prepare_data(df)
    df = df.dropna()
    return df

def split_data(df: pd.DataFrame, train_size: float = 0.8) -> (pd.DataFrame, pd.DataFrame):
    train_size = int(len(df) * train_size)
    train_df = df[:train_size]
    test_df = df[train_size:]
    return train_df, test_df

def train_model(train_df: pd.DataFrame) -> IsolationForest:
    model = IsolationForest(n_estimators=100, max_samples="auto",contamination=0.01, random_state=42, n_jobs=-1)
    X_df = train_df.drop(columns=["timestamp"])
    model.fit(X_df)
    return model

def evaluate_model(model: IsolationForest, test_df: pd.DataFrame) -> pd.Series:
    Y_df = test_df.drop(columns=["timestamp"])
    t0 = time.perf_counter()
    predictions = model.predict(Y_df)
    latency_ms = (time.perf_counter() - t0) * 1000
    print(f"Model inference latency: {latency_ms:.2f} ms")
    return pd.Series(predictions, index=test_df.index)

def save_model(model: IsolationForest, model_path: Path):
    joblib.dump(model, model_path)
    
def main():
    config = load_config("myconfig.yaml")
    db_path = os.path.join("weather_dashboard/data", config.get("db_name"))
    model_path = Path(config.get("model_path"))
    df = load_data(db_path)
    df = preprocess_data(df)
    train_df, _ = split_data(df, train_size=1.0)
    _, test_df = split_data(df, train_size=0.8)
    model = train_model(train_df)
    predictions = evaluate_model(model, test_df)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    save_model(model, model_path)
    print("Model training complete. Predictions on test set:")
    print(predictions.value_counts())

if __name__ == "__main__":
    main()