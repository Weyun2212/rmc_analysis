import pandas as pd


def plant_level_kpis(df: pd.DataFrame) -> dict:
    """
    Compute overall KPIs for a single RMC plant.

    Args:
        df (pd.DataFrame): Preprocessed dataframe

    Returns:
        dict: Plant-level KPIs
    """
    return {
        "total_revenue": df["total_revenue"].sum(),
        "total_customer_mix_cost": df["total_customer_mix_cost"].sum(),
        "total_optimized_mix_cost": df["total_optimized_mix_cost"].sum(),
        "total_savings": df["total_savings"].sum(),
        "avg_savings_per_cum": df["savings_rs_per_cum"].mean(),
        "savings_per_cum": (df["saving_per_cum"] * df["qty"]).sum(),
        "total_qty": df["qty"].sum()
    }


def customer_level_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute KPIs per customer.

    Args:
        df (pd.DataFrame): Preprocessed dataframe

    Returns:
        pd.DataFrame: KPIs grouped by customer_name
    """
    agg_df = df.groupby("customer_name").agg(
        total_qty=("qty", "sum"),
        total_revenue=("total_revenue", "sum"),
        total_customer_mix_cost=("total_customer_mix_cost", "sum"),
        total_optimized_mix_cost=("total_optimized_mix_cost", "sum"),
        total_savings=("total_savings", "sum"),
        avg_savings_per_cum=("savings_rs_per_cum", "mean"),
        savings_per_cum=("saving_per_cum", lambda x: (x * df.loc[x.index, "qty"]).sum())
    ).reset_index()

    return agg_df


def grade_level_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute KPIs per grade.

    Args:
        df (pd.DataFrame): Preprocessed dataframe

    Returns:
        pd.DataFrame: KPIs grouped by grade
    """
    agg_df = df.groupby("grade").agg(
        total_qty=("qty", "sum"),
        total_revenue=("total_revenue", "sum"),
        total_customer_mix_cost=("total_customer_mix_cost", "sum"),
        total_optimized_mix_cost=("total_optimized_mix_cost", "sum"),
        total_savings=("total_savings", "sum"),
        avg_savings_per_cum=("savings_rs_per_cum", "mean"),
        savings_per_cum=("saving_per_cum", lambda x: (x * df.loc[x.index, "qty"]).sum())
    ).reset_index()

    return agg_df
