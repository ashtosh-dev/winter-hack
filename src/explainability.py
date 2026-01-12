import pandas as pd


def generate_explanations(ghost_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a human-readable explanation column explaining
    why a SKU-day was flagged as ghost demand.
    """

    df = ghost_df.copy()

    explanations = []

    for _, row in df.iterrows():
        reasons = []

        # 1. Large deviation from expected demand
        if row["forecast_error"] > row["rolling_mean_7"]:
            reasons.append(
                "Sales significantly exceeded recent average demand"
            )

        # 2. High volatility
        if row.get("volatility_ratio", 0) > 1.5:
            reasons.append(
                "Demand showed unusually high short-term volatility"
            )

        # 3. Sudden demand spike
        if row.get("demand_change", 0) > 1.0:
            reasons.append(
                "Abrupt demand spike compared to previous period"
            )

        # Fallback
        if not reasons:
            reasons.append(
                "Anomalous demand pattern compared to historical behavior"
            )

        explanations.append("; ".join(reasons))

    df["explanation"] = explanations
    return df
