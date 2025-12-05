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
    
    import streamlit.components.v1 as components
    import json

    # Prepare Subway Data for Map
    # We need unique stations with lat/lon and aggregated ridership
    station_map_data = subway_df.groupby(['station_complex', 'latitude', 'longitude'])['ridership'].sum().reset_index()
    
    # Convert data to JSON for injection into JS
    stations_json = station_map_data.to_json(orient='records')

    # Leaflet HTML
    leaflet_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NYC Transit Map</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
        <style>
            #map {{ height: 600px; width: 100%; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([40.7128, -74.0060], 11);

            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }}).addTo(map);

            var stations = {stations_json};

            stations.forEach(function(station) {{
                var radius = Math.sqrt(station.ridership) / 50; // Simple scaling
                if (radius < 5) radius = 5; // Min size
                
                L.circleMarker([station.latitude, station.longitude], {{
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.5,
                    radius: radius
                }}).addTo(map)
                .bindPopup("<b>" + station.station_complex + "</b><br>Ridership: " + station.ridership.toLocaleString());
            }});
        </script>
    </body>
    </html>
    """

    components.html(leaflet_html, height=600)

