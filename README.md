# Public Transport Optimization

## Objective
Optimize public transport by analyzing ridership, delays, and congestion. This project aims to provide actionable insights for transit authorities and commuters.

## Features
- **Data Collection**: Fetching data from public transport APIs/datasets.
- **Data Cleaning**: Preprocessing and normalizing data.
- **EDA**: Exploratory Data Analysis to find trends and patterns.
- **Modeling**: Time series forecasting and clustering.
- **Dashboard**: Interactive visualization of insights.

## Structure
- `data/`: Raw and processed datasets.
- `notebooks/`: Jupyter notebooks for EDA and experiments.
- `src/`: Source code for data loading, cleaning, modeling, and dashboard.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the dashboard:
   ```bash
   streamlit run src/dashboard.py
   ```
