---
name: key-west-surf-report
description: Resilient coastal monitoring for Key West using NOAA Harbor/Sand Key sensors and NWS Marine forecasts.
---

# Key West Surf Report

## Instructions
Use this skill when Steven asks for the "Surf Report," "Beach Conditions," or "How's the water in Key West?" 

This skill implements a failover logic: if the primary Key West Harbor station is reporting suspect data, it automatically pivots to secondary offshore sensors (Sand Key/Peterson Key).

## Usage
uv run {baseDir}/scripts/fetch_surf_report.py

## Logic & Tone
- **Strategic Advice:** If the Flag Status is 🔴 RED, advise Steven to avoid the Atlantic side (Smathers Beach) and perhaps stick to the Gulf side or a pool.
- **Snorkel Alert:** If the Flag is 🟢 GREEN and Water Temp is >78°F, encourage a trip to the reef.
- **Small Craft Awareness:** If the report mentions a "Small Craft Advisory," explicitly mention that it's a "No-Go" for light boat activity.

## Contextual Note
Key West conditions are governed by the reef. Even if the 'Flag' is Green, always check the 'Wind' speed in the output to determine if the harbor will be choppy for paddleboarding.
