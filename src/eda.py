import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_DIR = "data"
PLOTS_DIR = "plots"
SUBWAY_FILE = os.path.join(DATA_DIR, "cleaned_subway.csv")
BUS_FILE = os.path.join(DATA_DIR, "cleaned_bus.csv")

os.makedirs(PLOTS_DIR, exist_ok=True)

def plot_subway_eda():
    print("Plotting subway EDA...")
    if not os.path.exists(SUBWAY_FILE):
        return

    df = pd.read_csv(SUBWAY_FILE)
    df['transit_timestamp'] = pd.to_datetime(df['transit_timestamp'])
    
    # Ridership over time (daily aggregation)
    daily_ridership = df.groupby('date')['ridership'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_ridership, x='date', y='ridership')
    plt.title('Daily Subway Ridership')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'subway_ridership_over_time.png'))
    plt.close()
    
    # Ridership by Borough
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='borough', y='ridership', estimator=sum, ci=None)
    plt.title('Total Ridership by Borough')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'subway_ridership_by_borough.png'))
    plt.close()

def plot_bus_eda():
    print("Plotting bus EDA...")
    if not os.path.exists(BUS_FILE):
        return

    df = pd.read_csv(BUS_FILE)
    
    # Average Speed by Borough
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='borough', y='average_speed')
    plt.title('Bus Average Speed by Borough')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'bus_speed_by_borough.png'))
    plt.close()

if __name__ == "__main__":
    plot_subway_eda()
    plot_bus_eda()
