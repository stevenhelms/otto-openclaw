import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from otto_utils import load_json_file

DATA_FILE = Path(__file__).parent / "../data/history.json"


def main():
    history = load_json_file(str(DATA_FILE))

    print("--- ✈️ FLIGHT PREDICTION ANALYSIS ---")

    if len(history) < 10:
        print(f"Need more data points to make a prediction (current: {len(history)}).")
        return

    df = pd.DataFrame(history)
    df["check_date"] = pd.to_datetime(df["check_date"])
    df["flight_date"] = pd.to_datetime(df["flight_date"])
    df["days_until_flight"] = (df["flight_date"] - df["check_date"]).dt.days

    for route in df["route"].unique():
        route_df = df[df["route"] == route]
        if len(route_df) < 5:
            continue

        X = route_df[["days_until_flight"]]
        y = route_df["price"]

        model = LinearRegression()
        model.fit(X, y)

        trend = "Rising (Book sooner!)" if model.coef_[0] > 0 else "Falling (Wait a bit?)"
        avg_price = route_df["price"].mean()
        correlation = route_df["days_until_flight"].corr(route_df["price"])

        print(f"\n📍 Route: {route}")
        print(f"  - Average Price: ${avg_price:.2f}")
        print(f"  - Current Trend: {trend}")
        print(f"  - Correlation: {correlation:.2f}")


if __name__ == "__main__":
    main()
