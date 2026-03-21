---
name: key-west-cruise-ships
description: Checks the live cruise ship schedule for Key West to monitor island crowd levels.
---

# Key West Cruise Ship Status

## Instructions
Use this skill when Steve asks "Are there ships in port?" or "How busy is downtown today?"

## Optimization
This skill should be run as a **Cron Job** when possible to save session context tokens.

## Usage
source .venv/bin/activate && python3 {baseDir}/scripts/fetch_ships.py
