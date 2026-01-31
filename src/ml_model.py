from sklearn.ensemble import IsolationForest
import joblib
import os

FEATURES = [
    "daily_sales",
    "rolling_mean_7",
    "rolling_std_7",
    "forecast_error",
    "demand_change",
    "volatility_ratio"
]

MODEL_PATH = "ghost_demand_model.pkl"


def train_ghost_model(df):
    df = df.dropna(subset=FEATURES).copy()
    X = df[FEATURES]

    model = IsolationForest(
        n_estimators=300,
        max_samples=256,
        max_features=0.8,
        contamination=0.02,
        random_state=42
    )

    model.fit(X)
    joblib.dump(model, MODEL_PATH)

    return model


def load_ghost_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Train it first.")
    return joblib.load(MODEL_PATH)


def detect_ghost_demand(df, model):
    df = df.dropna(subset=FEATURES).copy()
    X = df[FEATURES]

    df["ghost_flag"] = model.predict(X)
    df["ghost_demand"] = (df["ghost_flag"] == -1).astype(int)

    ghost_df = df[df["ghost_demand"] == 1].copy()
    return ghost_df
