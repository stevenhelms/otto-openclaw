---
name: key-west-family-tracker
description: Monitor family locations via Life360 for Key West geofence alerts and safety.
---

# Key West Family Tracker

## Instructions
Use this skill when Steve asks "Where is the family?" or to monitor geofence crossings.

## Optimization
This skill should be run as a **Cron Job** when possible to save session context tokens.

## Usage
# Run the geofence monitor
export LIFE360_USERNAME="..." && export LIFE360_PASSWORD="..." && source .venv/bin/activate && python3 {baseDir}/scripts/monitor_location.py
