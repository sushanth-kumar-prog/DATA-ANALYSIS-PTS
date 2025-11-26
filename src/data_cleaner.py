import pandas as pd
import os

DATA_DIR = "data"
SUBWAY_FILE = os.path.join(DATA_DIR, "subway_ridership.csv")
BUS_FILE = os.path.join(DATA_DIR, "bus_speeds.csv")

CLEANED_SUBWAY_FILE = os.path.join(DATA_DIR, "cleaned_subway.csv")
CLEANED_BUS_FILE = os.path.join(DATA_DIR, "cleaned_bus.csv")

def clean_subway_data():
    print("Cleaning subway data...")
    if not os.path.exists(SUBWAY_FILE):
        print("Subway file not found.")
        return

    df = pd.read_csv(SUBWAY_FILE)
    
    # Convert timestamp
    df['transit_timestamp'] = pd.to_datetime(df['transit_timestamp'])
    
    # Fill missing values if any (ridership should be 0 if missing, but let's check)
    df['ridership'] = df['ridership'].fillna(0)
    df['transfers'] = df['transfers'].fillna(0)
    
    # Extract date and hour features
    df['date'] = df['transit_timestamp'].dt.date
    df['hour'] = df['transit_timestamp'].dt.hour
    df['day_of_week'] = df['transit_timestamp'].dt.day_name()
    
    # Save cleaned data
    df.to_csv(CLEANED_SUBWAY_FILE, index=False)
    print(f"Saved cleaned subway data to {CLEANED_SUBWAY_FILE}")
    print(df.head())

def clean_bus_data():
    print("Cleaning bus data...")
    if not os.path.exists(BUS_FILE):
        print("Bus file not found.")
        return

    df = pd.read_csv(BUS_FILE)
    
    # Convert month to datetime
    df['month'] = pd.to_datetime(df['month'])
    
    # Save cleaned data
    df.to_csv(CLEANED_BUS_FILE, index=False)
    print(f"Saved cleaned bus data to {CLEANED_BUS_FILE}")
    print(df.head())

if __name__ == "__main__":
    clean_subway_data()
    clean_bus_data()
