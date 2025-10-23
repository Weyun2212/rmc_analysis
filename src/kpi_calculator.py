import pandas as pd
import numpy as np
import re


def weighted_average(series, weights):
    """Helper to compute weighted average safely"""
    try:
        return np.average(series, weights=weights)
    except ZeroDivisionError:
        return 0


def extract_grade_number(grade):
    """Extract numeric part from grade string like 'M30SCC' -> 30"""
    if pd.isna(grade):
        return np.nan
    match = re.search(r'\d+', str(grade))
    return float(match.group()) if match else np.nan


def plant_level_kpis(df: pd.DataFrame) -> dict:
    """Compute overall KPIs for the RMC plant."""
    total_qty = df["qty"].sum()
    total_revenue = df["total_revenue"].sum()

    weighted_asp = weighted_average(df["base_price"], df["qty"])
    weighted_c1 = weighted_average(df["customer_mix_c1"], df["qty"])
    avg_saving_per_cum = weighted_average(df["savings_rs_per_cum"], df["qty"])

    return {
        "total_qty": total_qty,
        "total_revenue": total_revenue,
        "avg_selling_price": weighted_asp,
        "avg_c1": weighted_c1,
        "avg_saving_per_cum": avg_saving_per_cum
    }


def customer_level_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute KPIs per customer."""
    agg_df = df.groupby("customer_name").apply(
        lambda g: pd.Series({
            "total_qty": g["qty"].sum(),
            "total_revenue": g["total_revenue"].sum(),
            "avg_asp": weighted_average(g["base_price"], g["qty"]),
            "avg_c1": weighted_average(g["customer_mix_c1"], g["qty"]),
            "avg_saving_per_cum": weighted_average(g["savings_rs_per_cum"], g["qty"])
        })
    ).reset_index()
    return agg_df


def grade_level_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute KPIs per grade (numeric part used for calculations)."""

    # Extract numeric grade values
    df["grade_num"] = df["grade"].apply(extract_grade_number)

    agg_df = df.groupby("grade").apply(
        lambda g: pd.Series({
            "total_qty": g["qty"].sum(),
            "avg_grade": weighted_average(g["grade_num"], g["qty"]),
            "avg_rm_cost_per_m3": weighted_average(g["optimized_mix_rm_cost"], g["qty"]),
            "avg_mix_cost": weighted_average(g["optimized_mix_rm_cost"], g["qty"])
        })
    ).reset_index()

    return agg_df
