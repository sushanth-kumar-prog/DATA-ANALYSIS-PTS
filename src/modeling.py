import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os

DATA_DIR = "data"
PLOTS_DIR = "plots"
SUBWAY_FILE = os.path.join(DATA_DIR, "cleaned_subway.csv")

def train_ridership_model():
    print("Training ridership model...")
    if not os.path.exists(SUBWAY_FILE):
        return

    df = pd.read_csv(SUBWAY_FILE)
    
    # Feature Engineering
    # Convert categorical variables to dummy/indicator variables
    df = pd.get_dummies(df, columns=['borough', 'day_of_week'], drop_first=True)
    
    # Select features and target
    features = ['hour'] + [col for col in df.columns if 'borough_' in col or 'day_of_week_' in col]
    target = 'ridership'
    
    X = df[features]
    y = df[target]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Evaluate
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    
    # Plot Actual vs Predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.3)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    plt.xlabel('Actual Ridership')
    plt.ylabel('Predicted Ridership')
    plt.title('Actual vs Predicted Ridership')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'ridership_prediction_actual_vs_pred.png'))
    plt.close()
    
    print("Model training and evaluation complete.")

if __name__ == "__main__":
    train_ridership_model()
