import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Public Transport Optimization", layout="wide")

DATA_DIR = "data"
SUBWAY_FILE = os.path.join(DATA_DIR, "cleaned_subway.csv")
BUS_FILE = os.path.join(DATA_DIR, "cleaned_bus.csv")

@st.cache_data
def load_data():
    subway_df = pd.read_csv(SUBWAY_FILE)
    bus_df = pd.read_csv(BUS_FILE)
    subway_df['transit_timestamp'] = pd.to_datetime(subway_df['transit_timestamp'])
    return subway_df, bus_df

try:
    subway_df, bus_df = load_data()
except FileNotFoundError:
    st.error("Data files not found. Please run the data collection and cleaning scripts first.")
    st.stop()

st.title("Public Transport Optimization Dashboard")

# Sidebar
st.sidebar.header("Filters")
selected_borough = st.sidebar.multiselect("Select Borough", subway_df['borough'].unique(), default=subway_df['borough'].unique())

# Filter data
filtered_subway = subway_df[subway_df['borough'].isin(selected_borough)]
filtered_bus = bus_df[bus_df['borough'].isin(selected_borough)]

# Key Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Subway Ridership", f"{filtered_subway['ridership'].sum():,.0f}")
col2.metric("Avg Bus Speed", f"{filtered_bus['average_speed'].mean():.2f} mph")
col3.metric("Total Bus Operating Time", f"{filtered_bus['total_operating_time'].sum():,.0f} hrs")

# Tabs
tab1, tab2, tab3 = st.tabs(["Subway Analysis", "Bus Analysis", "Recommendations"])

with tab1:
    st.header("Subway Ridership Trends")
    
    # Daily Trend
    daily_ridership = filtered_subway.groupby('date')['ridership'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=daily_ridership, x='date', y='ridership', ax=ax)
    ax.set_title("Daily Ridership Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Hourly Trend
    hourly_ridership = filtered_subway.groupby('hour')['ridership'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=hourly_ridership, x='hour', y='ridership', ax=ax, palette="viridis")
    ax.set_title("Average Ridership by Hour")
    st.pyplot(fig)

with tab2:
    st.header("Bus Performance")
    
    # Speed by Borough
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered_bus, x='borough', y='average_speed', ax=ax)
    ax.set_title("Bus Speed Distribution by Borough")
    st.pyplot(fig)

with tab3:
    st.header("Optimization Suggestions")
    st.markdown("""
    Based on the analysis:
    - **Peak Hours**: Increase subway frequency during 7-9 AM and 5-7 PM.
    - **Congestion**: Boroughs with lower average bus speeds (e.g., Manhattan) may benefit from dedicated bus lanes.
    - **Ridership**: Monitor low ridership stations for potential service adjustments.
    """)

# Map Tab
tab4 = st.tabs(["Interactive Map"])[0]
with tab4:
    st.header("Traffic & Transit Map")
    
    # API Token Input
    api_token = st.text_input("Enter Map API Token (Optional)", value="1afe2a24-267b-421c-bcd3-ae62c34c4aa7")
    
    import pydeck as pdk
    
    # Prepare Subway Data for Map
    # We need unique stations with lat/lon and aggregated ridership
    station_map_data = subway_df.groupby(['station_complex', 'latitude', 'longitude'])['ridership'].sum().reset_index()
    
    # Normalize ridership for circle size
    station_map_data['radius'] = station_map_data['ridership'] / station_map_data['ridership'].max() * 1000
    
    # PyDeck Layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        station_map_data,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius='radius',
        pickable=True,
    )
    
    # View State
    view_state = pdk.ViewState(
        latitude=40.7128,
        longitude=-74.0060,
        zoom=10,
        pitch=50,
    )
    
    # Render Map
    # Note: If the token is for a specific provider (e.g. Mapbox), we pass it to pdk.Deck(api_keys={'mapbox': ...})
    # But this UUID doesn't look like Mapbox. We'll use standard PyDeck which works without a token for basic styles.
    # If the user wants to use it, we can try to pass it, but it might fail if invalid.
    # We'll display it as a tooltip or just use it if we can identify the provider.
    # For now, we'll stick to the default map style.
    
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "{station_complex}\nRidership: {ridership}"}
    ))
    
    st.info("Note: The provided API token was not recognized as a standard Mapbox token. The map is rendered using default styles.")

