import sys
from pathlib import Path

# ------------------------------
# Ensure project root is in sys.path
# ------------------------------
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import streamlit as st
import plotly.express as px
import pandas as pd

from src.data_loader import load_excel
from src.preprocessing import preprocess_data
from src.kpi_calculator import plant_level_kpis, customer_level_kpis, grade_level_kpis

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="RMC Plant Dashboard v2", layout="wide")

# ------------------------------
# LOAD DATA
# ------------------------------
file_path = "data/raw/Test_File.xlsx"
df = preprocess_data(load_excel(file_path))

# ------------------------------
# SIDEBAR FILTERS
# ------------------------------
st.sidebar.header("🔍 Filters")
unique_months = df["date"].dt.to_period("M").astype(str).unique() if "date" in df.columns else []
selected_month = st.sidebar.selectbox("Select Month", ["All"] + list(unique_months))
if selected_month != "All":
    df = df[df["date"].dt.to_period("M").astype(str) == selected_month]

customers = st.sidebar.multiselect("Select Customers", options=sorted(df["customer_name"].unique()))
if customers:
    df = df[df["customer_name"].isin(customers)]

# ------------------------------
# KPI CALCULATIONS
# ------------------------------
plant_kpi = plant_level_kpis(df)
customer_kpi = customer_level_kpis(df)
grade_kpi = grade_level_kpis(df)

# ------------------------------
# KPI CARDS
# ------------------------------
st.title("🏭 RMC Plant Monthly Dashboard")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Qty Produced", f"{plant_kpi['total_qty']:.0f} cum")
kpi2.metric("Avg Selling Price", f"₹{plant_kpi['avg_selling_price']:.2f}")
kpi3.metric("Total Revenue", f"₹{plant_kpi['total_revenue'] / 1e5:.2f} L")
kpi4.metric("Avg Saving per m³", f"₹{plant_kpi['avg_saving_per_cum']:.2f}")
kpi5.metric("Avg C1", f"{plant_kpi['avg_c1']:.2f}")

st.markdown("---")

# ------------------------------
# CUSTOMER LEVEL INSIGHTS
# ------------------------------
st.subheader("👥 Customer Level Insights")

sort_by = st.selectbox(
    "Sort Customers By",
    ["total_qty", "avg_c1", "avg_asp", "total_revenue"],
    index=0
)
ascending = st.checkbox("Sort Ascending", value=False)

# Sort dynamically based on selection
sorted_customer_kpi = customer_kpi.sort_values(sort_by, ascending=ascending)

# Display full customer table
st.dataframe(sorted_customer_kpi, use_container_width=True)

# Bar chart for selected metric
fig = px.bar(
    sorted_customer_kpi,
    x="customer_name",
    y=sort_by,
    title=f"Customer-wise {sort_by.replace('_', ' ').title()}",
    text_auto=True,
    color=sort_by
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ------------------------------
# GRADE LEVEL INSIGHTS
# ------------------------------
st.subheader("🧱 Grade Level Insights")

# Sort grades numerically based on extracted numeric part (if available)
grade_kpi["grade_num"] = grade_kpi["grade"].str.extract(r'(\d+)').astype(float)
grade_kpi = grade_kpi.sort_values("grade_num")

grade_kpi_col1, grade_kpi_col2 = st.columns(2)
grade_kpi_col1.metric(
    "Avg Grade Supplied",
    f"{grade_kpi['avg_grade'].mean() if 'avg_grade' in grade_kpi else 0:.2f}"
)
grade_kpi_col2.metric(
    "Avg RM Cost per m³",
    f"₹{grade_kpi['avg_rm_cost_per_m3'].mean():.2f}"
)

fig3 = px.bar(
    grade_kpi,
    x="grade",
    y="total_qty",
    title="Grade-wise Quantity Supplied",
    text_auto=True
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.line(
    grade_kpi,
    x="grade",
    y="avg_mix_cost",
    markers=True,
    title="Grade-wise Average Mix Cost"
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ------------------------------
# EXPORT SECTION
# ------------------------------
st.subheader("📦 Export Data")

@st.cache_data
def convert_to_excel(plant_kpi, customer_kpi, grade_kpi, df):
    output_path = project_root / "data/processed/dashboard_export.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame([plant_kpi]).to_excel(writer, sheet_name="Plant_Summary", index=False)
        customer_kpi.to_excel(writer, sheet_name="Customer_Summary", index=False)
        grade_kpi.to_excel(writer, sheet_name="Grade_Summary", index=False)
        df.to_excel(writer, sheet_name="Raw_Data", index=False)
    return output_path

if st.button("📤 Export Dashboard Report"):
    path = convert_to_excel(plant_kpi, customer_kpi, grade_kpi, df)
    st.success(f"Report exported successfully → {path}")
