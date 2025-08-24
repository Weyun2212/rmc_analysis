import pandas as pd


def load_excel(file_path: str) -> pd.DataFrame:
    """
    Load and clean RMC plant Excel report.

    Args:
        file_path (str): Path to Excel file

    Returns:
        pd.DataFrame: Cleaned dataframe
    """

    # Load sheet (assuming 1st sheet, adjust if needed)
    df = pd.read_excel(file_path, sheet_name=0)

    # Standardize column names → lowercase, replace spaces with underscores
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
    )

    # Convert date column (if exists)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Ensure numeric fields are properly typed
    numeric_cols = [
        "qty", "vac_qty", "base_price",
        "customer_mix_rm_cost", "optimized_mix_rm_cost",
        "customer_mix_c1", "optimized_mix_c1",
        "savings_rs_per_cum"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
