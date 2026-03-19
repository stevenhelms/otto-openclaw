---
name: key-west-flight-forecaster
description: Tracks flight prices between EYW (Key West) and XNA (Northwest Arkansas) to build a predictive model for the best booking times.
---

# Key West Flight Forecaster

## Instructions
Use this skill to track current flight prices or run the predictive model.

## Usage
# To track current prices and save to data/history.json
source .venv/bin/activate && python3 {baseDir}/scripts/track_prices.py

# To run the prediction model (needs at least 4 weeks of data)
source .venv/bin/activate && python3 {baseDir}/scripts/predict_prices.py
