import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Nigeria Household Spending Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ENHANCED COLOUR PALETTE & CONTRAST INJECTION
# ============================================================

# Brand Colors
NAVY = "#17233C"
BLUE = "#2563EB"      # Slightly deeper blue for higher contrast
TEAL = "#0D9488"      # Deeper teal for enhanced legibility
PINK = "#DB2777"      # High-contrast vibrant pink
PURPLE = "#7C3AED"    # Deep vibrant purple
SKY = "#0284C7"

# Text & Interface Colors (High Contrast)
DARK_TEXT = "#0F172A"  # Deep slate for primary chart text & titles
AXIS_TEXT = "#334155"  # Medium-dark slate for tick marks & axis labels
MUTED_TEXT = "#64748B" # Muted slate for captions
WHITE = "#FFFFFF"
GRID = "#E2E8F0"       # Slightly stronger grid line contrast

# Custom CSS for Streamlit Native Components (Metrics & Headers)
st.markdown(
    f"""
    <style>
    /* High contrast for Streamlit Metrics */
    [data-testid="stMetricValue"] {{
        color: {DARK_TEXT} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {AXIS_TEXT} !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# OPTIMIZED PLOTLY SETTINGS
# ============================================================

plotly_font = dict(
    family="Inter, -apple-system, BlinkMacSystemFont, Arial, sans-serif",
    color=DARK_TEXT,
    size=13
)

plotly_layout = dict(
    paper_bgcolor=WHITE,
    plot_bgcolor=WHITE,
    font=plotly_font,
    margin=dict(l=20, r=20, t=40, b=20)
)

# Shared axis styling for visual consistency
axis_style = dict(
    title_font=dict(size=13, color=DARK_TEXT, family="Arial, sans-serif"),
    tickfont=dict(size=11, color=AXIS_TEXT),
    gridcolor=GRID
)


# ============================================================
# DATA GENERATION
# ============================================================

@st.cache_data
def create_data():

    np.random.seed(42)
    n = 1000

    regions = [
        "North Central",
        "North East",
        "North West",
        "South East",
        "South South",
        "South West"
    ]

    region_values = np.random.choice(
        regions,
        size=n,
        p=[0.16, 0.12, 0.17, 0.14, 0.16, 0.25]
    )

    household_size = np.random.randint(1, 9, size=n)
    monthly_income = np.random.randint(80000, 1200001, size=n)

    months = np.random.choice(
        [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        size=n
    )

    food = (
        monthly_income * np.random.uniform(0.12, 0.25, n)
        + household_size * np.random.randint(3000, 9000, n)
    )
    housing = monthly_income * np.random.uniform(0.10, 0.24, n)
    transportation = monthly_income * np.random.uniform(0.04, 0.12, n)
    electricity = monthly_income * np.random.uniform(0.025, 0.08, n)
    healthcare = monthly_income * np.random.uniform(0.025, 0.09, n)
    education = (
        monthly_income * np.random.uniform(0.02, 0.08, n)
        + household_size * np.random.randint(1000, 5000, n)
    )
    communication = monthly_income * np.random.uniform(0.015, 0.05, n)

    total_spending = (
        food + housing + transportation + electricity +
        healthcare + education + communication
    )

    savings = np.maximum(monthly_income - total_spending, 0)
    savings_rate = (savings / monthly_income) * 100

    income_group = pd.cut(
        monthly_income,
        bins=[0, 250000, 600000, np.inf],
        labels=["Lower Income", "Middle Income", "Higher Income"]
    )

    df = pd.DataFrame({
        "Region": region_values,
        "Household Size": household_size,
        "Monthly Income": monthly_income,
        "Month": months,
        "Food": food,
        "Housing": housing,
        "Transportation": transportation,
        "Electricity": electricity,
        "Healthcare": healthcare,
        "Education": education,
        "Communication": communication,
        "Total Spending": total_spending,
        "Savings": savings,
        "Savings Rate": savings_rate,
        "Income Group": income_group
    })

    return df


df = create_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Dashboard controls")
st.sidebar.caption("Explore household spending patterns across Nigeria.")

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_income_groups = st.sidebar.multiselect(
    "Income group",
    options=["Lower Income", "Middle Income", "Higher Income"],
    default=["Lower Income", "Middle Income", "Higher Income"]
)

minimum_household_size = st.sidebar.slider(
    "Minimum household size",
    min_value=1,
    max_value=8,
    value=1
)

st.sidebar.divider()
st.sidebar.info(
    "This dashboard uses a synthetic household dataset "
    "created for portfolio and analytical demonstration."
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Income Group"].astype(str).isin(selected_income_groups)) &
    (df["Household Size"] >= minimum_household_size)
].copy()


# ============================================================
# EMPTY FILTER STATE
# ============================================================

if filtered_df.empty:
    st.warning("No households match the selected filters. Try widening your selection.")
    st.stop()


# ============================================================
# HERO SECTION
# ============================================================

st.caption("NIGERIA  •  HOUSEHOLD ECONOMICS  •  2025")
st.title("How Nigerian households spend what they earn.")
st.write(
    "An exploratory view of household income, spending, "
    "savings and financial pressure across six regions."
)
st.caption("Synthetic sample household dataset • 1,000 observations")
st.divider()


# ============================================================
# TOP METRICS
# ============================================================

average_income = filtered_df["Monthly Income"].mean()
average_spending = filtered_df["Total Spending"].mean()
average_savings = filtered_df["Savings"].mean()
average_savings_rate = filtered_df["Savings Rate"].mean()

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric("Average income", f"₦{average_income:,.0f}")
with metric2:
    st.metric("Average spending", f"₦{average_spending:,.0f}")
with metric3:
    st.metric("Average savings", f"₦{average_savings:,.0f}")
with metric4:
    st.metric("Average savings rate", f"{average_savings_rate:.1f}%")

st.write("")


# ============================================================
# SPENDING DISTRIBUTION
# ============================================================

st.subheader("Where household money goes")

category_columns = [
    "Food", "Housing", "Transportation", "Electricity",
    "Healthcare", "Education", "Communication"
]

category_totals = (
    filtered_df[category_columns]
    .sum()
    .sort_values(ascending=False)
)

category_df = category_totals.reset_index()
category_df.columns = ["Category", "Spending"]

category_chart = px.bar(
    category_df,
    x="Category",
    y="Spending",
    text_auto=".2s",
    color="Category",
    color_discrete_sequence=[PINK, TEAL, BLUE, PURPLE, SKY, "#0D9488", "#DB2777"]
)

category_chart.update_layout(
    **plotly_layout,
    height=420,
    showlegend=False,
    xaxis=dict(title=None, showgrid=False, **axis_style),
    yaxis=dict(title="Total spending", tickprefix="₦", tickformat=",", showgrid=True, **axis_style)
)

category_chart.update_traces(
    textposition="outside",
    cliponaxis=False,
    textfont=dict(color=DARK_TEXT, size=12, family="Arial, sans-serif")
)

st.plotly_chart(category_chart, use_container_width=True)


# ============================================================
# INCOME VS SPENDING
# ============================================================

st.subheader("Income and spending move together")
st.write(
    "Higher-income households generally spend more in absolute "
    "terms, but spending does not increase at exactly the same rate as income."
)

scatter_chart = px.scatter(
    filtered_df,
    x="Monthly Income",
    y="Total Spending",
    size="Household Size",
    color="Income Group",
    hover_data=["Region", "Household Size", "Savings", "Savings Rate"],
    color_discrete_map={
        "Lower Income": PINK,
        "Middle Income": TEAL,
        "Higher Income": BLUE
    }
)

scatter_chart.update_layout(
    **plotly_layout,
    height=450,
    legend=dict(font=dict(color=DARK_TEXT, size=12)),
    xaxis=dict(title="Monthly income", tickprefix="₦", tickformat=",", showgrid=True, **axis_style),
    yaxis=dict(title="Monthly spending", tickprefix="₦", tickformat=",", showgrid=True, **axis_style)
)

st.plotly_chart(scatter_chart, use_container_width=True)


# ============================================================
# INSIGHT BOXES
# ============================================================

insight1, insight2 = st.columns(2)

with insight1:
    st.info(
        "The largest spending categories are generally housing and food, "
        "highlighting the importance of essential household costs."
    )

with insight2:
    st.success(
        "Savings increase with income in absolute terms, although household size "
        "and spending patterns still create substantial differences."
    )

st.write("")


# ============================================================
# MONTHLY TREND
# ============================================================

st.subheader("Monthly household spending")

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

monthly_df = (
    filtered_df
    .groupby("Month", observed=False)
    .agg(
        Average_Income=("Monthly Income", "mean"),
        Average_Spending=("Total Spending", "mean"),
        Average_Savings=("Savings", "mean")
    )
    .reindex(month_order)
    .reset_index()
)

trend_chart = go.Figure()

trend_chart.add_trace(
    go.Scatter(
        x=monthly_df["Month"],
        y=monthly_df["Average_Income"],
        mode="lines+markers",
        name="Income",
        line=dict(width=3.5, color=BLUE),
        marker=dict(size=8)
    )
)

trend_chart.add_trace(
    go.Scatter(
        x=monthly_df["Month"],
        y=monthly_df["Average_Spending"],
        mode="lines+markers",
        name="Spending",
        line=dict(width=3.5, color=PINK),
        marker=dict(size=8)
    )
)

trend_chart.add_trace(
    go.Scatter(
        x=monthly_df["Month"],
        y=monthly_df["Average_Savings"],
        mode="lines+markers",
        name="Savings",
        line=dict(width=3.5, color=TEAL),
        marker=dict(size=8)
    )
)

trend_chart.update_layout(
    **plotly_layout,
    height=430,
    hovermode="x unified",
    xaxis=dict(title=None, showgrid=False, **axis_style),
    yaxis=dict(title="Average monthly amount", tickprefix="₦", tickformat=",", showgrid=True, **axis_style),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        font=dict(color=DARK_TEXT, size=12)
    )
)

st.plotly_chart(trend_chart, use_container_width=True)


# ============================================================
# REGIONAL ANALYSIS
# ============================================================

st.subheader("The regional picture")

regional_df = (
    filtered_df
    .groupby("Region")
    .agg(
        Average_Income=("Monthly Income", "mean"),
        Average_Spending=("Total Spending", "mean"),
        Average_Savings=("Savings", "mean")
    )
    .reset_index()
)

regional_spending = px.bar(
    regional_df.sort_values("Average_Spending", ascending=False),
    x="Region",
    y="Average_Spending",
    color="Region",
    text_auto=".2s",
    color_discrete_sequence=[BLUE, TEAL, PINK, PURPLE, SKY, "#0D9488"]
)

regional_spending.update_layout(
    paper_bgcolor=WHITE,
    plot_bgcolor=WHITE,
    font=plotly_font,
    height=390,
    margin=dict(l=10, r=10, t=20, b=80),
    showlegend=False,
    xaxis=dict(title=None, showgrid=False, tickangle=-25, **axis_style),
    yaxis=dict(title="Average spending", tickprefix="₦", tickformat=",", showgrid=True, **axis_style)
)

regional_spending.update_traces(
    textposition="outside",
    cliponaxis=False,
    textfont=dict(color=DARK_TEXT, size=11)
)

regional_savings = px.bar(
    regional_df.sort_values("Average_Savings", ascending=False),
    x="Region",
    y="Average_Savings",
    color="Region",
    text_auto=".2s",
    color_discrete_sequence=[TEAL, BLUE, PINK, PURPLE, SKY, "#0D9488"]
)

regional_savings.update_layout(
    paper_bgcolor=WHITE,
    plot_bgcolor=WHITE,
    font=plotly_font,
    height=390,
    margin=dict(l=10, r=10, t=20, b=80),
    showlegend=False,
    xaxis=dict(title=None, showgrid=False, tickangle=-25, **axis_style),
    yaxis=dict(title="Average savings", tickprefix="₦", tickformat=",", showgrid=True, **axis_style)
)

regional_savings.update_traces(
    textposition="outside",
    cliponaxis=False,
    textfont=dict(color=DARK_TEXT, size=11)
)

regional_col1, regional_col2 = st.columns(2)

with regional_col1:
    st.plotly_chart(regional_spending, use_container_width=True)

with regional_col2:
    st.plotly_chart(regional_savings, use_container_width=True)


# ============================================================
# INCOME GROUP COMPARISON
# ============================================================

st.subheader("How spending changes across income groups")

income_group_df = (
    filtered_df
    .groupby("Income Group", observed=False)
    .agg(
        Average_Income=("Monthly Income", "mean"),
        Average_Spending=("Total Spending", "mean"),
        Average_Savings=("Savings", "mean"),
        Average_Savings_Rate=("Savings Rate", "mean")
    )
    .reset_index()
)

income_long = income_group_df.melt(
    id_vars="Income Group",
    value_vars=["Average_Spending", "Average_Savings"],
    var_name="Measure",
    value_name="Amount"
)

income_long["Measure"] = income_long["Measure"].replace({
    "Average_Spending": "Spending",
    "Average_Savings": "Savings"
})

income_chart = px.bar(
    income_long,
    x="Income Group",
    y="Amount",
    color="Measure",
    barmode="group",
    text_auto=".2s",
    color_discrete_map={"Spending": PINK, "Savings": TEAL}
)

income_chart.update_layout(
    **plotly_layout,
    height=420,
    legend=dict(font=dict(color=DARK_TEXT, size=12)),
    xaxis=dict(title=None, showgrid=False, **axis_style),
    yaxis=dict(title="Average monthly amount", tickprefix="₦", tickformat=",", showgrid=True, **axis_style)
)

income_chart.update_traces(
    textposition="outside",
    cliponaxis=False,
    textfont=dict(color=DARK_TEXT, size=11)
)

st.plotly_chart(income_chart, use_container_width=True)


# ============================================================
# SPENDING COMPOSITION
# ============================================================

st.subheader("What makes up household spending?")

composition = (
    filtered_df[category_columns]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

composition.columns = ["Category", "Average Spending"]

donut_chart = go.Figure(
    data=[
        go.Pie(
            labels=composition["Category"],
            values=composition["Average Spending"],
            hole=0.62,
            textinfo="percent",
            textposition="outside",
            textfont=dict(color=DARK_TEXT, size=13),
            marker=dict(colors=[PINK, TEAL, BLUE, PURPLE, SKY, "#0D9488", "#DB2777"])
        )
    ]
)

donut_chart.update_layout(
    **plotly_layout,
    height=500,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(color=DARK_TEXT, size=12)
    )
)

st.plotly_chart(donut_chart, use_container_width=True)


# ============================================================
# FINANCIAL PRESSURE
# ============================================================

st.subheader("Financial pressure")

pressure_col1, pressure_col2, pressure_col3 = st.columns(3)

food_share = (filtered_df["Food"].sum() / filtered_df["Total Spending"].sum()) * 100
housing_share = (filtered_df["Housing"].sum() / filtered_df["Total Spending"].sum()) * 100
zero_savings_share = ((filtered_df["Savings"] <= 1).mean()) * 100

with pressure_col1:
    st.metric("Food share of spending", f"{food_share:.1f}%")
    st.caption("Share of total household expenditure allocated to food.")

with pressure_col2:
    st.metric("Housing share of spending", f"{housing_share:.1f}%")
    st.caption("Share of total household expenditure allocated to housing.")

with pressure_col3:
    st.metric("Households with no savings", f"{zero_savings_share:.1f}%")
    st.caption("Households where simulated spending reaches income.")


# ============================================================
# KEY TAKEAWAYS
# ============================================================

st.subheader("Key takeaways")

highest_spending_category = category_totals.idxmax()

highest_spending_region = (
    regional_df
    .sort_values("Average_Spending", ascending=False)
    .iloc[0]["Region"]
)

highest_saving_region = (
    regional_df
    .sort_values("Average_Savings", ascending=False)
    .iloc[0]["Region"]
)

takeaway1, takeaway2 = st.columns(2)

with takeaway1:
    st.info(
        f"Food is the largest spending category in this synthetic sample, "
        f"accounting for {food_share:.1f}% of total expenditure."
    )
    st.info(
        f"{highest_spending_region} has the highest average household spending "
        f"among the selected regions."
    )

with takeaway2:
    st.success(
        f"{highest_saving_region} records the highest average savings in the selected sample."
    )
    st.success(
        f"The average household saves approximately {average_savings_rate:.1f}% "
        f"of monthly income after simulated spending."
    )


# ============================================================
# DATA EXPLORER
# ============================================================

st.divider()
st.subheader("Data explorer")
st.caption("The table below shows the households included in the current analysis.")

display_columns = [
    "Region", "Income Group", "Household Size",
    "Monthly Income", "Total Spending", "Savings", "Savings Rate"
]

st.dataframe(
    filtered_df[display_columns].round(2),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered dataset",
    data=csv_data,
    file_name="nigeria_household_spending_filtered.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("Nigeria Household Spending Analytics • 2025")