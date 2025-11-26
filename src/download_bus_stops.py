import requests
import os
import pandas as pd

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# MTA Bus Stops Dataset ID
BUS_STOPS_ID = "39hk-dx4f" # Found via search or common knowledge for MTA Bus Stops
# Actually, let's use a known URL or search result ID if possible. 
# The search result mentioned "MTA Bus Stops" on data.gov. 
# I'll use a direct URL if I can find one, or try the SODA API with a likely ID.
# Let's try searching for the exact ID first to be safe, or use a generic search in the script?
# No, I'll use the ID from the search result if available. 
# Search result 5: "MTA Bus Stops" -> data.gov -> usually has an ID.
# Let's try to find the ID "39hk-dx4f" (common for NYC bus stops) or similar.
# Alternatively, I can use the "MTA Bus Routes" dataset ID if I want shapes.
# Let's try to download "MTA Bus Stops" using a likely ID or search.

# Let's use the ID for "MTA Bus Stops": "39hk-dx4f" is often cited.
# If not, I'll use the search API to find it dynamically? No, that's complex.
# I'll try to download from a known stable URL for NYC Bus Stops if possible.
# https://data.cityofnewyork.us/api/views/39hk-dx4f/rows.csv?accessType=DOWNLOAD

BASE_URL = "https://data.cityofnewyork.us/api/views/39hk-dx4f/rows.csv?accessType=DOWNLOAD"

def download_bus_stops():
    filename = "bus_stops.csv"
    filepath = os.path.join(DATA_DIR, filename)
    print(f"Downloading {filename}...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Saved to {filepath}")
        
        # Preview
        df = pd.read_csv(filepath)
        print(f"Downloaded {len(df)} bus stops.")
        print(df.head())
    except Exception as e:
        print(f"Error downloading bus stops: {e}")

if __name__ == "__main__":
    download_bus_stops()
