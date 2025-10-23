import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.data_loader import load_excel
from src.preprocessing import preprocess_data
from src.kpi_calculator import plant_level_kpis, customer_level_kpis, grade_level_kpis

# --- Config ---
st.set_page_config(
    page_title="RMC Plant Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
    }

    .kpi-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stMetric > div {
        color: white !important;
    }

    .stMetric label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Load Data ---
@st.cache_data
def load_dashboard_data():
    file_path = "data/raw/Test_File.xlsx"
    df = preprocess_data(load_excel(file_path))
    return df


df = load_dashboard_data()


# --- Compute KPIs ---
@st.cache_data
def compute_kpis(df):
    plant_kpi = plant_level_kpis(df)
    customer_kpi = customer_level_kpis(df)
    grade_kpi = grade_level_kpis(df)
    return plant_kpi, customer_kpi, grade_kpi


plant_kpi, customer_kpi, grade_kpi = compute_kpis(df)

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
st.sidebar.title("🏭 RMC Analytics")
st.sidebar.markdown("### Dashboard Controls")

# Add filters in sidebar
if not customer_kpi.empty:
    selected_customers = st.sidebar.multiselect(
        "Select Customers:",
        options=customer_kpi['customer_name'].unique(),
        default=customer_kpi['customer_name'].unique()[:5]  # Default to top 5
    )

if not grade_kpi.empty:
    selected_grades = st.sidebar.multiselect(
        "Select Grades:",
        options=grade_kpi['grade'].unique(),
        default=grade_kpi['grade'].unique()
    )

st.sidebar.markdown("### Quick Stats")
st.sidebar.info(f"📅 **Data Points:** {len(df):,}")
st.sidebar.info(f"👥 **Total Customers:** {len(customer_kpi):,}")
st.sidebar.info(f"🏷️ **Total Grades:** {len(grade_kpi):,}")

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# --- Main Dashboard ---
st.markdown('<h1 class="main-header">🏭 RMC Plant Dashboard</h1>', unsafe_allow_html=True)

# --- KPI Cards Section ---
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">📊 Key Performance Indicators</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"₹{plant_kpi['total_revenue']:,.0f}",
        delta=f"₹{plant_kpi['total_revenue'] * 0.05:.0f}",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="💎 Total Savings",
        value=f"₹{plant_kpi['total_savings']:,.0f}",
        delta=f"{plant_kpi['total_savings'] / plant_kpi['total_revenue'] * 100:.1f}%",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="📈 Avg Savings/cum",
        value=f"₹{plant_kpi['avg_savings_per_cum']:.2f}",
        delta="Optimized",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="🏗️ Total Quantity",
        value=f"{plant_kpi['total_qty']:,.0f}",
        delta="cum",
        delta_color="off"
    )

st.markdown('</div>', unsafe_allow_html=True)

# --- Charts Section ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">👥 Customer Performance</h3>', unsafe_allow_html=True)

    # Filter data based on selection
    filtered_customer_kpi = customer_kpi[
        customer_kpi['customer_name'].isin(selected_customers)] if 'selected_customers' in locals() else customer_kpi
    top_customers = filtered_customer_kpi.sort_values("total_savings", ascending=False).head(10)

    fig1 = px.bar(
        top_customers,
        x="total_savings",
        y="customer_name",
        orientation='h',
        title="Top Customers by Savings",
        color="total_savings",
        color_continuous_scale="viridis",
        text="total_savings"
    )
    fig1.update_traces(texttemplate='₹%{text:,.0f}', textposition='inside')
    fig1.update_layout(
        height=400,
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    fig1.update_xaxes(title="Savings (₹)", showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig1.update_yaxes(title="Customer", showgrid=False)

    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🎯 Grade Distribution</h3>', unsafe_allow_html=True)

    # Filter data based on selection
    filtered_grade_kpi = grade_kpi[
        grade_kpi['grade'].isin(selected_grades)] if 'selected_grades' in locals() else grade_kpi

    fig2 = px.pie(
        filtered_grade_kpi,
        names="grade",
        values="total_qty",
        title="Volume Distribution by Grade",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(
        height=400,
        font=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Combined Analytics ---
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
st.markdown('<h3 class="section-header">📈 Advanced Analytics</h3>', unsafe_allow_html=True)

# Create subplot with secondary y-axis
fig3 = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Savings vs Revenue by Customer", "Quantity vs Savings Efficiency"),
    specs=[[{"secondary_y": True}, {"secondary_y": True}]]
)

# Scatter plot: Savings vs Revenue
if not filtered_customer_kpi.empty and 'total_revenue' in filtered_customer_kpi.columns:
    fig3.add_trace(
        go.Scatter(
            x=filtered_customer_kpi['total_revenue'],
            y=filtered_customer_kpi['total_savings'],
            mode='markers+text',
            text=filtered_customer_kpi['customer_name'],
            textposition="top center",
            marker=dict(size=10, color=filtered_customer_kpi['total_savings'],
                        colorscale='viridis', showscale=True),
            name="Customer Performance"
        ),
        row=1, col=1
    )

# Bar chart: Quantity analysis
if not filtered_grade_kpi.empty:
    fig3.add_trace(
        go.Bar(
            x=filtered_grade_kpi['grade'],
            y=filtered_grade_kpi['total_qty'],
            name="Quantity",
            marker_color='lightblue',
            yaxis='y3'
        ),
        row=1, col=2
    )

    if 'avg_savings_per_cum' in filtered_grade_kpi.columns:
        fig3.add_trace(
            go.Scatter(
                x=filtered_grade_kpi['grade'],
                y=filtered_grade_kpi['avg_savings_per_cum'],
                mode='lines+markers',
                name="Savings/cum",
                line=dict(color='red', width=3),
                yaxis='y4'
            ),
            row=1, col=2
        )

fig3.update_layout(
    height=500,
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Data Tables ---
tab1, tab2 = st.tabs(["👥 Customer Analytics", "🏷️ Grade Analytics"])

with tab1:
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📋 Detailed Customer KPIs</h3>', unsafe_allow_html=True)

    # Enhanced dataframe with styling
    customer_display = filtered_customer_kpi.copy() if 'filtered_customer_kpi' in locals() else customer_kpi
    if not customer_display.empty:
        # Format currency columns
        for col in customer_display.columns:
            if 'total_' in col and col != 'total_qty':
                customer_display[col] = customer_display[col].apply(lambda x: f"₹{x:,.0f}")
            elif col == 'total_qty':
                customer_display[col] = customer_display[col].apply(lambda x: f"{x:,.0f} cum")
            elif 'avg_' in col:
                customer_display[col] = customer_display[col].apply(lambda x: f"₹{x:.2f}")

    st.dataframe(
        customer_display,
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📋 Detailed Grade KPIs</h3>', unsafe_allow_html=True)

    # Enhanced dataframe with styling
    grade_display = filtered_grade_kpi.copy() if 'filtered_grade_kpi' in locals() else grade_kpi
    if not grade_display.empty:
        # Format currency columns
        for col in grade_display.columns:
            if 'total_' in col and col != 'total_qty':
                grade_display[col] = grade_display[col].apply(lambda x: f"₹{x:,.0f}")
            elif col == 'total_qty':
                grade_display[col] = grade_display[col].apply(lambda x: f"{x:,.0f} cum")
            elif 'avg_' in col:
                grade_display[col] = grade_display[col].apply(lambda x: f"₹{x:.2f}")

    st.dataframe(
        grade_display,
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🏭 RMC Plant Dashboard | Built with Streamlit & Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)