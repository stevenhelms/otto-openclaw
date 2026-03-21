---
name: key-west-island-explorer
description: Monitors local Key West inventory for paddleboards, kayaks, and e-bikes.
---

# Key West Island Explorer

## Instructions
Use this skill when Steve wants to find gear for island life or check for local sales.

## Optimization
This skill should be run as a **Cron Job** when possible to save session context tokens.

## Usage
# Search for gear across local indexed sources
source .venv/bin/activate && python3 {baseDir}/scripts/search_gear.py "e-bike"
source .venv/bin/activate && python3 {baseDir}/scripts/search_gear.py "paddleboard"
