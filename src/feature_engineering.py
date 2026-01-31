import pandas as pd

def add_time_series_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["SKU", "Date"]).copy()

    df["rolling_mean_7"] = (
        df.groupby("SKU")["daily_sales"]
        .transform(lambda x: x.rolling(7).mean())
    )

    df["rolling_std_7"] = (
        df.groupby("SKU")["daily_sales"]
        .transform(lambda x: x.rolling(7).std())
    )

    df["demand_change"] = (
        df.groupby("SKU")["daily_sales"]
        .pct_change()
    )

    df["volatility_ratio"] = (
        df["rolling_std_7"] / (df["rolling_mean_7"] + 1e-6)
    )

    # Simple proxy for forecast error (naive forecast)
    df["forecast_error"] = (
        df["daily_sales"] -
        df.groupby("SKU")["daily_sales"].shift(1)
    )

    return df
