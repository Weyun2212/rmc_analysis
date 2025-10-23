import streamlit as st
import plotly.express as px
import pandas as pd
from src.data_loader import load_excel
from src.preprocessing import preprocess_data
from src.kpi_calculator import customer_level_kpis

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Customer Level Insights", layout="wide")
st.title("👥 Customer Level Insights")

# ------------------------------
# LOAD DATA
# ------------------------------
file_path = "data/raw/Test_File.xlsx"
if not file_path:
    st.warning("⚠️ Please upload a data file from the Home page.")
    st.stop()

df = load_excel(file_path)
df = preprocess_data(df)
customer_df = customer_level_kpis(df)

# Reset index to keep fixed serial numbering
customer_df = customer_df.reset_index(drop=True)
customer_df.insert(0, "S.No", range(1, len(customer_df) + 1))

# ------------------------------
# SORTING OPTIONS
# ------------------------------
st.subheader("Sort Customers By")
sort_col = st.selectbox(
    "Select a column to sort by:",
    options=[col for col in customer_df.columns if col not in ["S.No", "customer_name"]],
    index=0,
    label_visibility="collapsed"
)

# Dual sort direction options
sort_direction = st.radio(
    "Sort Order",
    options=["Ascending", "Descending"],
    horizontal=True,
    index=0,
)

ascending = sort_direction == "Ascending"

# Sort but keep serial numbers fixed
sorted_df = customer_df.copy()
sorted_df = sorted_df.sort_values(by=sort_col, ascending=ascending, ignore_index=True)
sorted_df["S.No"] = range(1, len(sorted_df) + 1)

# ------------------------------
# DISPLAY TABLE
# ------------------------------
st.dataframe(
    sorted_df,
    use_container_width=True,
    hide_index=True,
)

# ------------------------------
# VISUALIZATION
# ------------------------------
st.subheader("📊 Top Customers by Selected Metric")

top_n = st.slider("Select Top N Customers", 5, 20, 10)

top_customers = (
    customer_df.sort_values(by=sort_col, ascending=False)
    .head(top_n)
    .sort_values(by=sort_col, ascending=True)
)

# Updated bar color – gradient from darker to lighter (avoid white)
fig = px.bar(
    top_customers,
    x=sort_col,
    y="customer_name",
    orientation="h",
    color=sort_col,
    color_continuous_scale=px.colors.sequential.Tealgrn,  # Dark → Light green-blue
    title=f"Top {top_n} Customers by {sort_col}",
)

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    title_font=dict(size=18, color="white"),
)

st.plotly_chart(fig, use_container_width=True)
