from src.data_cleaning import load_data
from src.feature_engineering import add_time_series_features
from src.ml_model import train_ghost_model

df = load_data()
df = add_time_series_features(df)

train_ghost_model(df)

print("Ghost demand model trained and saved.")
