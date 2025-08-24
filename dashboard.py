import streamlit as st
import plotly.express as px
from src.data_loader import load_excel
from src.preprocessing import preprocess_data
from src.kpi_calculator import plant_level_kpis, customer_level_kpis, grade_level_kpis

# --- Config ---
st.set_page_config(page_title="RMC Plant Dashboard", layout="wide")

# --- Load Data ---
file_path = "data/raw/Test_File.xlsx"
df = preprocess_data(load_excel(file_path))

# --- Compute KPIs ---
plant_kpi = plant_level_kpis(df)
customer_kpi = customer_level_kpis(df)
grade_kpi = grade_level_kpis(df)

# --- Dashboard ---
st.title("🏭 RMC Plant Dashboard")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{plant_kpi['total_revenue']:,}")
col2.metric("Total Savings", f"₹{plant_kpi['total_savings']:,}")
col3.metric("Avg Savings / cum", f"₹{plant_kpi['avg_savings_per_cum']:.2f}")
col4.metric("Total Qty", f"{plant_kpi['total_qty']:,} cum")

# Customer-wise Savings
st.subheader("📊 Customer-wise Savings")
fig1 = px.bar(customer_kpi.sort_values("total_savings", ascending=False),
              x="customer_name", y="total_savings",
              title="Top Customers by Savings")
st.plotly_chart(fig1, use_container_width=True)

# Grade-wise Performance
st.subheader("🎯 Grade-wise Performance")
fig2 = px.pie(grade_kpi, names="grade", values="total_qty", title="Volume by Grade")
st.plotly_chart(fig2, use_container_width=True)

# Tables
st.subheader("📋 Customer Level KPIs")
st.dataframe(customer_kpi)

st.subheader("📋 Grade Level KPIs")
st.dataframe(grade_kpi)
