from ortools.linear_solver import pywraplp
import numpy as np
import pandas as pd


# -------------------------------
# Configuration (business knobs)
# -------------------------------
MAX_REDUCTION_RATIO = 0.8        # Max % of excess demand we are willing to cut
UNIT_PRODUCTION_COST = 50.0      # Cost per unit produced (₹ or $)
UNIT_WASTE_PENALTY = 20.0        # Waste / disposal / discount cost per unit


def optimize_production(ghost_df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize production cuts for ghost demand cases using OR-Tools.

    Returns ghost_df with:
    - recommended_cut
    - cost_saving
    - waste_reduction_value
    """

    # Defensive copy
    df = ghost_df.copy()

    # -------------------------------
    # 1. Filter actionable cases ONLY
    # -------------------------------
    df = df[
        (df["forecast_error"] > 0) &
        (df["rolling_mean_7"] > 0)
    ].copy()

    if df.empty:
        # Nothing actionable
        ghost_df["recommended_cut"] = 0.0
        ghost_df["cost_saving"] = 0.0
        ghost_df["waste_reduction_value"] = 0.0
        return ghost_df

    # -------------------------------
    # 2. Initialize solver
    # -------------------------------
    solver = pywraplp.Solver.CreateSolver("GLOP")

    if solver is None:
        raise RuntimeError("OR-Tools solver could not be created")

    reduction_vars = {}

    # -------------------------------
    # 3. Decision variables
    # -------------------------------
    for idx, row in df.iterrows():
        max_cut = max(
            0.0,
            row["forecast_error"] * MAX_REDUCTION_RATIO
        )

        reduction_vars[idx] = solver.NumVar(
            0.0,
            max_cut,
            f"cut_{idx}"
        )

    # -------------------------------
    # 4. Objective function
    # Minimize cost of overproduction
    # -------------------------------
    objective = solver.Objective()

    unit_penalty = UNIT_PRODUCTION_COST + UNIT_WASTE_PENALTY

    for idx, var in reduction_vars.items():
        objective.SetCoefficient(var, unit_penalty)

    objective.SetMinimization()

    # -------------------------------
    # 5. Solve
    # -------------------------------
    status = solver.Solve()

    # -------------------------------
    # 6. Handle solver result safely
    # -------------------------------
    df["recommended_cut"] = 0.0

    if status == pywraplp.Solver.OPTIMAL:
        for idx, var in reduction_vars.items():
            df.loc[idx, "recommended_cut"] = var.solution_value()
    else:
        # Infeasible or abnormal → no action
        df["recommended_cut"] = 0.0

    # -------------------------------
    # 7. Business impact metrics
    # -------------------------------
    df["cost_saving"] = df["recommended_cut"] * UNIT_PRODUCTION_COST
    df["waste_reduction_value"] = df["recommended_cut"] * UNIT_WASTE_PENALTY

    # -------------------------------
    # 8. Merge back into original DF
    # -------------------------------
    ghost_df["recommended_cut"] = 0.0
    ghost_df["cost_saving"] = 0.0
    ghost_df["waste_reduction_value"] = 0.0

    ghost_df.update(
        df[["recommended_cut", "cost_saving", "waste_reduction_value"]]
    )

    return ghost_df
