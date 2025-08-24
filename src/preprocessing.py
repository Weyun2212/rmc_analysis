import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess RMC plant data:
    - Handle missing values
    - Add derived columns for KPI calculations

    Args:
        df (pd.DataFrame): Cleaned dataframe from data_loader

    Returns:
        pd.DataFrame: Preprocessed dataframe
    """

    # ---------------------------
    # 1. Handle missing values
    # ---------------------------
    # Drop rows with no customer or qty (invalid records)
    df = df.dropna(subset=["customer_name", "qty"]).copy()

    # Fill missing numerical values with 0
    num_cols = df.select_dtypes(include=["float64", "int64"]).columns
    df.loc[:, num_cols] = df[num_cols].fillna(0)

    # Fill missing text fields with placeholder
    text_cols = df.select_dtypes(include=["object"]).columns
    df.loc[:, text_cols] = df[text_cols].fillna("Unknown")

    # ---------------------------
    # 2. Derived Columns
    # ---------------------------
    if "qty" in df.columns and "base_price" in df.columns:
        df["total_revenue"] = df["qty"] * df["base_price"]

    if "qty" in df.columns and "customer_mix_rm_cost" in df.columns:
        df["total_customer_mix_cost"] = df["qty"] * df["customer_mix_rm_cost"]

    if "qty" in df.columns and "optimized_mix_rm_cost" in df.columns:
        df["total_optimized_mix_cost"] = df["qty"] * df["optimized_mix_rm_cost"]

    if "qty" in df.columns and "savings_rs_per_cum" in df.columns:
        df["total_savings"] = df["qty"] * df["savings_rs_per_cum"]

    # Cement difference (customer mix - optimized mix)
    if "customer_mix_c1" in df.columns and "optimized_mix_c1" in df.columns:
        df["saving_per_cum"] = (
                df["optimized_mix_c1"] - df["customer_mix_c1"]
        )

    return df