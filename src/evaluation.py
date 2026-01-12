import numpy as np

def evaluate_impact(df):
    df = df.copy()

    df['blind_production'] = df['rolling_mean_7']
    df['optimized_production'] = (
        df['blind_production'] - df['recommended_cut']
    ).clip(lower=df['daily_sales'])

    df['blind_waste'] = np.maximum(
        df['blind_production'] - df['daily_sales'], 0
    )

    df['optimized_waste'] = np.maximum(
        df['optimized_production'] - df['daily_sales'], 0
    )

    df['waste_saved'] = df['blind_waste'] - df['optimized_waste']

    return df
