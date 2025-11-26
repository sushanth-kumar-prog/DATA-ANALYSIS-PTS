import requests
import os
import pandas as pd

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Dataset IDs
SUBWAY_ID = "wujg-7c2s"
BUS_ID = "6ksi-7cxr"

BASE_URL = "https://data.ny.gov/resource/"

def download_data(dataset_id, filename, limit=50000):
    url = f"{BASE_URL}{dataset_id}.csv?$limit={limit}"
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Saved to {filepath}")
        
        # Verify it's a valid CSV
        df = pd.read_csv(filepath)
        print(f"Downloaded {len(df)} rows.")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

if __name__ == "__main__":
    print("Starting data download...")
    download_data(SUBWAY_ID, "subway_ridership.csv")
    download_data(BUS_ID, "bus_speeds.csv")
    print("Download complete.")
