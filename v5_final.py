import streamlit as st
import plotly.express as px
import pandas as pd
from src.data_loader import load_excel
from src.preprocessing import preprocess_data
from src.kpi_calculator import plant_level_kpis, customer_level_kpis, grade_level_kpis

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="RMC Plant Dashboard v3", layout="wide")

# ------------------------------
# LOAD DATA
# ------------------------------
file_path = "data/raw/Test_File.xlsx"
df = preprocess_data(load_excel(file_path))

# ------------------------------
# TITLE
# ------------------------------
st.title("🧱 RMC Plant Analytics Dashboard")

# ------------------------------
# PLANT LEVEL INSIGHTS
# ------------------------------
with st.container():
    st.header("🏭 Plant Level Insights")

    plant_df = plant_level_kpis(df)
    plant_df = pd.DataFrame(plant_df)  # ✅ Convert dict -> DataFrame
    plant_df = plant_df.reset_index(drop=True)
    plant_df.insert(0, "S.No", range(1, len(plant_df) + 1))

    st.subheader("Sort Plants By")
    sort_col = st.selectbox(
        "Select column to sort by",
        options=[col for col in plant_df.columns if col not in ["S.No", "plant_name"]],
        index=0,
        key="plant_sort",
        label_visibility="collapsed"
    )

    sort_direction = st.radio(
        "Sort Order",
        options=["Ascending", "Descending"],
        horizontal=True,
        index=0,
        key="plant_sort_dir",
    )
    ascending = sort_direction == "Ascending"

    sorted_plant_df = plant_df.sort_values(by=sort_col, ascending=ascending, ignore_index=True)
    sorted_plant_df["S.No"] = range(1, len(sorted_plant_df) + 1)

    st.dataframe(sorted_plant_df, use_container_width=True, hide_index=True)

    st.subheader("📊 Top Plants by Selected Metric")
    max_plants = len(plant_df)
    top_n_plants = st.slider("Select Top N Plants", 5, max_plants, min(10, max_plants), key="plant_topn")

    top_plants = (
        plant_df.sort_values(by=sort_col, ascending=False)
        .head(top_n_plants)
        .sort_values(by=sort_col, ascending=True)
    )

    fig_plant = px.bar(
        top_plants,
        x=sort_col,
        y="plant_name",
        orientation="h",
        color=sort_col,
        color_continuous_scale=px.colors.sequential.Blues,
        title=f"Top {top_n_plants} Plants by {sort_col}",
    )

    fig_plant.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18, color="white"),
    )

    st.plotly_chart(fig_plant, use_container_width=True)


# ------------------------------
# CUSTOMER LEVEL INSIGHTS
# ------------------------------
with st.container():
    st.header("👥 Customer Level Insights")

    customer_df = customer_level_kpis(df)
    customer_df = pd.DataFrame(customer_df)  # ✅ Convert dict -> DataFrame
    customer_df = customer_df.reset_index(drop=True)
    customer_df.insert(0, "S.No", range(1, len(customer_df) + 1))

    st.subheader("Sort Customers By")
    sort_col = st.selectbox(
        "Select column to sort by",
        options=[col for col in customer_df.columns if col not in ["S.No", "customer_name"]],
        index=0,
        key="customer_sort",
        label_visibility="collapsed"
    )

    sort_direction = st.radio(
        "Sort Order",
        options=["Ascending", "Descending"],
        horizontal=True,
        index=0,
        key="customer_sort_dir",
    )
    ascending = sort_direction == "Ascending"

    sorted_df = customer_df.sort_values(by=sort_col, ascending=ascending, ignore_index=True)
    sorted_df["S.No"] = range(1, len(sorted_df) + 1)

    st.dataframe(sorted_df, use_container_width=True, hide_index=True)

    st.subheader("📊 Top Customers by Selected Metric")
    max_customers = len(customer_df)
    top_n = st.slider("Select Top N Customers", 5, max_customers, min(10, max_customers), key="customer_topn")

    top_customers = (
        customer_df.sort_values(by=sort_col, ascending=False)
        .head(top_n)
        .sort_values(by=sort_col, ascending=True)
    )

    fig = px.bar(
        top_customers,
        x=sort_col,
        y="customer_name",
        orientation="h",
        color=sort_col,
        color_continuous_scale=px.colors.sequential.Blues,
        title=f"Top {top_n} Customers by {sort_col}",
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18, color="white"),
    )

    st.plotly_chart(fig, use_container_width=True)


# ------------------------------
# GRADE LEVEL INSIGHTS
# ------------------------------
with st.container():
    st.header("🧪 Grade Level Insights")

    grade_df = grade_level_kpis(df)
    grade_df = pd.DataFrame(grade_df)  # ✅ Convert dict -> DataFrame
    grade_df = grade_df.reset_index(drop=True)
    grade_df.insert(0, "S.No", range(1, len(grade_df) + 1))

    st.subheader("Sort Grades By")
    sort_col = st.selectbox(
        "Select column to sort by",
        options=[col for col in grade_df.columns if col not in ["S.No", "grade"]],
        index=0,
        key="grade_sort",
        label_visibility="collapsed"
    )

    sort_direction = st.radio(
        "Sort Order",
        options=["Ascending", "Descending"],
        horizontal=True,
        index=0,
        key="grade_sort_dir",
    )
    ascending = sort_direction == "Ascending"

    sorted_grade_df = grade_df.sort_values(by=sort_col, ascending=ascending, ignore_index=True)
    sorted_grade_df["S.No"] = range(1, len(sorted_grade_df) + 1)

    st.dataframe(sorted_grade_df, use_container_width=True, hide_index=True)

    st.subheader("📊 Top Grades by Selected Metric")
    max_grades = len(grade_df)
    top_n_grades = st.slider("Select Top N Grades", 5, max_grades, min(10, max_grades), key="grade_topn")

    top_grades = (
        grade_df.sort_values(by=sort_col, ascending=False)
        .head(top_n_grades)
        .sort_values(by=sort_col, ascending=True)
    )

    fig_grade = px.bar(
        top_grades,
        x=sort_col,
        y="grade",
        orientation="h",
        color=sort_col,
        color_continuous_scale=px.colors.sequential.Blues,
        title=f"Top {top_n_grades} Grades by {sort_col}",
    )

    fig_grade.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18, color="white"),
    )

    st.plotly_chart(fig_grade, use_container_width=True)
