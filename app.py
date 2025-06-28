import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("🔋 Electric Vehicles Spec Explorer (2025)")

# Load data
df = pd.read_csv("electric_vehicles_spec_2025.csv.csv")

# Basic cleanup (replace with actual column names)
st.sidebar.header("Filter EVs")
brands = st.sidebar.multiselect("Select Brand", options=df['Brand'].unique(), default=df['Brand'].unique())
body_types = st.sidebar.multiselect("Select Body Type", options=df['Body Type'].unique(), default=df['Body Type'].unique())
range_min, range_max = st.sidebar.slider("Select Range (km)", int(df['Range (km)'].min()), int(df['Range (km)'].max()), (int(df['Range (km)'].min()), int(df['Range (km)'].max())))

# Filter data
filtered_df = df[
    (df['Brand'].isin(brands)) &
    (df['Body Type'].isin(body_types)) &
    (df['Range (km)'] >= range_min) & 
    (df['Range (km)'] <= range_max)
]

# KPI Cards
st.metric("Total Models", len(filtered_df))
st.metric("Average Range (km)", round(filtered_df['Range (km)'].mean(), 1))
st.metric("Average Price ($)", round(filtered_df['Price'].mean(), 2))

# Plot: Top 10 EVs by Range
top_range = filtered_df.sort_values(by="Range (km)", ascending=False).head(10)
fig1 = px.bar(top_range, x='Model', y='Range (km)', color='Brand', title='Top 10 EVs by Range')
st.plotly_chart(fig1)

# Plot: Price vs Range
fig2 = px.scatter(filtered_df, x="Price", y="Range (km)", color="Brand", hover_name="Model", title="Price vs Range")
st.plotly_chart(fig2)

# Plot: Market Share by Brand
brand_counts = filtered_df['Brand'].value_counts().reset_index()
fig3 = px.pie(brand_counts, names='index', values='Brand', title="Market Share by Brand")
st.plotly_chart(fig3)

# Data Table
st.subheader("Filtered EV Data")
st.dataframe(filtered_df)

# Download filtered data
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)
st.download_button("📥 Download CSV", data=csv, file_name='filtered_ev_data.csv', mime='text/csv')
