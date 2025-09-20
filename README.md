# StonkBot007 - Business News Aggregator

A simple Python application that fetches and displays recent business news from India (with US fallback).

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   - Copy `config.example.py` to `config.py`
   - Get a free API key from [NewsAPI](https://newsapi.org/)
   - Add your API key to `config.py`

3. **Run the application:**
   ```bash
   python agent.py
   ```

## Features

- Fetches business news from India (with fallback to US business news)
- Clean, formatted output with emojis
- Robust error handling
- Smart fallback system for different news sources

## Files

- `agent.py` - Main application entry point
- `news_fetcher.py` - News fetching logic with API integration
- `config.py` - API configuration (not tracked in git)
- `config.example.py` - Example configuration file
- `requirements.txt` - Python dependencies
