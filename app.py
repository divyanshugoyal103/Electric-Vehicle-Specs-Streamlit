import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(page_title="EV Explorer 2025", layout="wide")
st.title("🔋 Electric Vehicles Spec Explorer (2025)")

# Load and clean data
df = pd.read_csv("electric_vehicles_spec_2025.csv.csv")
df.columns = df.columns.str.strip()

# Sidebar Filters
st.sidebar.header("Filter EVs")
brands = st.sidebar.multiselect("Select Brand", options=df['brand'].unique(), default=df['brand'].unique())
body_types = st.sidebar.multiselect("Select Body Type", options=df['car_body_type'].dropna().unique(), default=df['car_body_type'].dropna().unique())
range_min, range_max = st.sidebar.slider("Select Range (km)", int(df['range_km'].min()), int(df['range_km'].max()), (int(df['range_km'].min()), int(df['range_km'].max())))

# Filtered DataFrame
filtered_df = df[
    (df['brand'].isin(brands)) &
    (df['car_body_type'].isin(body_types)) &
    (df['range_km'] >= range_min) &
    (df['range_km'] <= range_max)
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Models", len(filtered_df))
col2.metric("Average Range (km)", round(filtered_df['range_km'].mean(), 1))
col3.metric("Avg Battery Capacity (kWh)", round(filtered_df['battery_capacity_kWh'].mean(), 1))

st.markdown("---")

# Bar Chart - Top 10 by Range
top_range = filtered_df.sort_values(by="range_km", ascending=False).head(10)
fig1 = px.bar(top_range, x='model', y='range_km', color='brand', title='🔝 Top 10 EVs by Range')
st.plotly_chart(fig1, use_container_width=True)

# Scatter Plot - Efficiency vs Range
fig2 = px.scatter(filtered_df, x="efficiency_wh_per_km", y="range_km", color="brand",
                  hover_name="model", title="⚡ Efficiency vs Range (Wh/km vs km)")
st.plotly_chart(fig2, use_container_width=True)

# Pie Chart - Market Share by Brand
brand_counts = filtered_df['brand'].value_counts().reset_index()
brand_counts.columns = ['brand', 'count']
fig3 = px.pie(brand_counts, names='brand', values='count', title="📈 Market Share by Brand")
st.plotly_chart(fig3, use_container_width=True)

# Data Table
st.subheader("📋 Filtered EV Data")
st.dataframe(filtered_df)

# Download
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)
st.download_button("📥 Download Filtered Data", data=csv, file_name="filtered_ev_data.csv", mime='text/csv')
