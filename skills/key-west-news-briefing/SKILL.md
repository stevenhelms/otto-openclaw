---
name: key-west-news-briefing
description: Aggregates international, national, and Trump-specific news via RSS feeds for a daily morning briefing.
---

# Key West News Briefing

## Instructions
Use this skill when Steve asks for "The news," "Morning briefing," or "What's happening in the world?"

## Usage
source .venv/bin/activate && python3 {baseDir}/scripts/fetch_news.py

## Source Priority
1. **International:** BBC World/Reuters feeds.
2. **National:** AP News and trending Google News.
3. **Eagle Eye:** Specific tracking for President Trump's statements via indexed X/Twitter bridges.

## Logic
- The script cleans up CDATA and HTML noise from RSS feeds.
- Snippets are truncated to keep the briefing concise for mobile viewing.
