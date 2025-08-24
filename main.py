from src.data_loader import load_excel
from src.preprocessing import preprocess_data
from src.kpi_calculator import plant_level_kpis, customer_level_kpis, grade_level_kpis
import pandas as pd


def main():
    file_path = "data/raw/Test_File.xlsx"

    # Load & preprocess
    df = load_excel(file_path)
    df = preprocess_data(df)
    print(df["saving_per_cum"])

    print("\n📊 Columns after preprocessing:")
    print(df.columns.tolist())

    # --- Plant Level KPIs ---
    plant_kpis = plant_level_kpis(df)
    print("\n✅ Plant Level KPIs")
    print(plant_kpis)

    # --- Customer Level KPIs ---
    customer_kpis = customer_level_kpis(df)
    print("\n✅ Customer Level KPIs (sample)")
    print(customer_kpis.head())

    # --- Grade Level KPIs ---
    grade_kpis = grade_level_kpis(df)
    print("\n✅ Grade Level KPIs (sample)")
    print(grade_kpis.head())

    # --- Export all results into Excel ---
    output_file = "data/processed/plant_kpi_report.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        # Plant KPIs (single row dict → DataFrame)
        pd.DataFrame([plant_kpis]).to_excel(writer, sheet_name="Plant_Summary", index=False)

        # Customer-wise KPIs
        customer_kpis.to_excel(writer, sheet_name="Customer_Summary", index=False)

        # Grade-wise KPIs
        grade_kpis.to_excel(writer, sheet_name="Grade_Summary", index=False)

        # Raw cleaned dataset
        df.to_excel(writer, sheet_name="Raw_Cleaned_Data", index=False)

    print(f"\n📂 KPI Report exported successfully → {output_file}")


if __name__ == "__main__":
    main()
