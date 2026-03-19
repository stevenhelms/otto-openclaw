import json
import os
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

def main():
    data_file = os.path.join(os.path.dirname(__file__), "../data/history.json")
    
    if not os.path.exists(data_file):
        print("--- ✈️ FLIGHT PREDICTOR ---")
        print("No data yet. Run the tracker first.")
        return

    with open(data_file, 'r') as f:
        history = json.load(f)
    
    if len(history) < 10:
        print("--- ✈️ FLIGHT PREDICTOR ---")
        print(f"Need more data points to make a prediction (Current: {len(history)}).")
        return

    df = pd.DataFrame(history)
    df['check_date'] = pd.to_datetime(df['check_date'])
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    df['days_until_flight'] = (df['flight_date'] - df['check_date']).dt.days
    
    print("--- ✈️ FLIGHT PREDICTION ANALYSIS ---")
    
    for route in df['route'].unique():
        route_df = df[df['route'] == route]
        if len(route_df) < 5: continue
            
        # Simple linear regression: Price vs Days Until Flight
        X = route_df[['days_until_flight']]
        y = route_df['price']
        
        model = LinearRegression()
        model.fit(X, y)
        
        slope = model.coef_[0]
        
        if slope > 0:
            trend = "Rising (Book sooner!)"
        else:
            trend = "Falling (Wait a bit?)"
            
        avg_price = route_df['price'].mean()
        
        print(f"\n📍 Route: {route}")
        print(f"  - Average Price: ${avg_price:.2f}")
        print(f"  - Current Trend: {trend}")
        print(f"  - Correlation: {route_df['days_until_flight'].corr(route_df['price']):.2f}")

if __name__ == "__main__":
    main()
