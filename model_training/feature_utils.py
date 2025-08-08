import pandas as pd
import sqlite3
import numpy as np
from pathlib import Path

def convert_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    return df

def sorted_df(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns:
        df = df.sort_values(by="timestamp").reset_index(drop=True)
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns:
        df = df.drop_duplicates(subset=["timestamp", "temperature", "humidity", "pressure"], keep='first')
    return df

def encode_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns:
        hour = df["timestamp"].dt.hour
        minute = df["timestamp"].dt.minute
        second = df["timestamp"].dt.second
        fraction_of_day = (hour * 3600 + minute * 60 + second) / 86400.0
        angle = fraction_of_day * 2 * np.pi
        sin_timestamp = np.sin(angle)
        cos_timestamp = np.cos(angle)
        df["sin_timestamp"] = sin_timestamp.astype(np.float32)
        df["cos_timestamp"] = cos_timestamp.astype(np.float32)
    return df

def rolling_means(df: pd.DataFrame, window_size: int = 5) -> pd.DataFrame:
    if "temperature" in df.columns:
        df["rolling_mean_temperature"] = df["temperature"].rolling(window=window_size, min_periods=1).mean()
    if "humidity" in df.columns:
        df["rolling_mean_humidity"] = df["humidity"].rolling(window=window_size, min_periods=1).mean()
    if "pressure" in df.columns:
        df["rolling_mean_pressure"] = df["pressure"].rolling(window=window_size, min_periods=1).mean()
    return df

def differences(df: pd.DataFrame) -> pd.DataFrame:
    if "temperature" in df.columns:
        df["temperature_diff"] = df["temperature"].diff().fillna(0)
    if "humidity" in df.columns:
        df["humidity_diff"] = df["humidity"].diff().fillna(0)
    if "pressure" in df.columns:
        df["pressure_diff"] = df["pressure"].diff().fillna(0)
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = encode_timestamp(df)
    df = rolling_means(df)
    df = differences(df)
    return df

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    df = convert_to_datetime(df)
    df = sorted_df(df)
    df = remove_duplicates(df)
    return df

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = validate_data(df)
    df = feature_engineering(df)
    return df

if __name__ == "__main__":
    # Testing
    path = Path("weather-dashboard/data/weather.db")
    uri = f"file:{path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    cursor = conn.execute("SELECT timestamp, temperature, humidity, pressure FROM weather_data")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["timestamp", "temperature", "humidity", "pressure"])
    df = validate_data(df)
    df = feature_engineering(df)
    print(df.iloc[:, 1:])  # Display first 5 rows for testing
    conn.close()