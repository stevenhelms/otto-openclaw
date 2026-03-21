---
name: key-west-traffic-report
description: Monitors US-1 traffic and FL511 incidents for the Key West commute.
---

# Instructions
Run this skill when Steven asks "What's the drive look like?" or "Any traffic today?"

## Optimization
This skill should be run as a **Cron Job** when possible to save session context tokens.

# Usage
uv run {baseDir}/scripts/fetch_traffic_report.py

# Intelligence Logic
- If commute > 20 mins: Warn him that US-1 is backing up.
- If FL511 reports a "Crash" or "Bridge Closure": Flag this as a CRITICAL ALERT.
- Remind him that parking downtown can be a secondary bottleneck if he's running late.
