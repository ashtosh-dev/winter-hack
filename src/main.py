from src.data_cleaning import load_and_prepare_data
from src.feature_engineering import build_features
from src.ml_model import detect_ghost_demand
from src.optimization import optimize_production
from src.evaluation import evaluate_impact
from src.explainability import generate_explanations

def main():
    
    df = load_and_prepare_data("data/Amazon Sale Report.csv")
    df = build_features(df)
    df = detect_ghost_demand(df)
    df = generate_explanations(df)      # ← explain the detection
    df = optimize_production(df)
    df = evaluate_impact(df)

    df.to_csv("outputs/final_results.csv", index=False)

if __name__ == "__main__":
    main()
