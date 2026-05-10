import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Sneaker Market Analytics",
    page_icon="👟",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/StockX-Data-Contest-2019-3.csv")

# -----------------------------
# TITLE
# -----------------------------
st.title("👟 Sneaker Market Analytics Dashboard")
st.markdown("Interactive analytics dashboard for sneaker resale and market trends.")


# -----------------------------
# DATA CLEANING
# -----------------------------

# Convert order date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Convert Sale Price to numeric
df["Sale Price"] = (
    df["Sale Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Sale Price"] = pd.to_numeric(df["Sale Price"])

# Convert Retail Price to numeric
df["Retail Price"] = (
    df["Retail Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["Retail Price"] = pd.to_numeric(df["Retail Price"])

# Calculate resale profit
df["Resale Profit"] = df["Sale Price"] - df["Retail Price"]
df["ROI %"] = (
    (df["Resale Profit"] / df["Retail Price"]) * 100
)
# -----------------------------
# -----------------------------
# TOP FILTERS
# -----------------------------

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_brand = st.selectbox(
        "Select Brand",
        options=["All"] + list(df["Brand"].unique())
    )

with filter_col2:
    sneaker_search = st.text_input(
        "Search Sneaker Model"
    )

# Apply filters
filtered_df = df.copy()

if selected_brand != "All":
    filtered_df = filtered_df[
        filtered_df["Brand"] == selected_brand
    ]

if sneaker_search:
    filtered_df = filtered_df[
        filtered_df["Sneaker Name"]
        .str.contains(sneaker_search, case=False)
    ]


# -----------------------------
# KPI METRICS
# -----------------------------
total_sales = filtered_df["Sale Price"].sum()
average_price = filtered_df["Sale Price"].mean()
total_pairs = filtered_df.shape[0]

col1, col2, col3, col4 = st.columns(4)
average_roi = filtered_df["ROI %"].mean()

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Average Sale Price", f"${average_price:,.0f}")
col3.metric("👟 Total Pairs Sold", f"{total_pairs:,}")
col4.metric("🚀 Average ROI", f"{average_roi:.1f}%")
# -----------------------------
# SALES BY BRAND
# -----------------------------
st.subheader("Sales by Brand")

brand_sales = (
    filtered_df.groupby("Brand")["Sale Price"]
    .sum()
    .reset_index()
)

fig_brand = px.bar(
    brand_sales,
    x="Brand",
    y="Sale Price",
    text_auto=True,
    title="Brand Sales Performance"
)

st.plotly_chart(fig_brand, use_container_width=True)

# -----------------------------
# TOP SNEAKERS
# -----------------------------
st.subheader("Top Sneaker Models")

top_sneakers = (
    filtered_df.groupby("Sneaker Name")["Sale Price"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_sneakers = px.bar(
    top_sneakers,
    x="Sneaker Name",
    y="Sale Price",
    text_auto=True,
    title="Top 10 Sneaker Models by Average Price"
)

st.plotly_chart(fig_sneakers, use_container_width=True)

# -----------------------------
# MONTHLY SALES TREND
# -----------------------------
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.to_period("M"))["Sale Price"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig_monthly = px.line(
    monthly_sales,
    x="Order Date",
    y="Sale Price",
    markers=True,
    title="Monthly Sneaker Sales Trend"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# -----------------------------
# RETAIL PRICE VS SALE PRICE
# -----------------------------
st.subheader("Retail Price vs Sale Price")

fig_scatter = px.scatter(
    filtered_df,
    x="Retail Price",
    y="Sale Price",
    color="Brand",
    hover_data=["Sneaker Name"],
    title="Retail Price vs Resale Price"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# MOST EXPENSIVE SNEAKERS
# -----------------------------
st.subheader("Most Expensive Sneakers")

expensive_sneakers = (
    filtered_df[["Sneaker Name", "Sale Price"]]
    .sort_values(by="Sale Price", ascending=False)
    .head(10)
)

st.dataframe(expensive_sneakers)
# -----------------------------
# TOP RESALE PROFIT SNEAKERS
# -----------------------------
st.subheader("Top Sneaker Resale Profits")

profit_by_shoe = (
    filtered_df.groupby("Sneaker Name")["Resale Profit"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_profit = px.bar(
    profit_by_shoe,
    x="Sneaker Name",
    y="Resale Profit",
    text_auto=True,
    title="Top 10 Sneakers by Average Resale Profit"
)

st.plotly_chart(fig_profit, use_container_width=True)
# -----------------------------
# TOP ROI SNEAKERS
# -----------------------------
st.subheader("Top ROI Sneakers")

roi_chart = (
    filtered_df.groupby("Sneaker Name")["ROI %"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_roi = px.bar(
    roi_chart,
    x="Sneaker Name",
    y="ROI %",
    text_auto=True,
    title="Top 10 Sneakers by ROI %"
)

st.plotly_chart(fig_roi, use_container_width=True)

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------
st.subheader("Market Insights")

st.markdown("""
- Certain sneaker models dominate the resale market significantly.
- Premium sneakers achieved substantially higher resale values.
- Brand popularity strongly influenced resale pricing.
- Monthly sales trends indicate periods of heightened sneaker demand.
- Several sneakers showed large gaps between retail and resale pricing.
""")