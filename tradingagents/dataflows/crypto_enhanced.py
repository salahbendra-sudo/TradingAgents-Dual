"""
Enhanced Crypto data vendor for TradingAgents.
Provides comprehensive cryptocurrency data with multiple API support.
Supports: CoinGecko, CoinMarketCap, CryptoCompare, and social media APIs.
"""

from typing import Annotated, Dict, Any, List
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os
import requests
import json
import time
from .config import get_config

# Crypto API configurations
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINMARKETCAP_API_BASE = "https://pro-api.coinmarketcap.com/v1"
CRYPTOCOMPARE_API_BASE = "https://min-api.cryptocompare.com/data"

# Rate limiting
RATE_LIMITS = {
    "coingecko": 50,  # requests per minute
    "coinmarketcap": 333,  # requests per day for free tier
    "cryptocompare": 1000,  # requests per hour
}

# Last request timestamps for rate limiting
_last_request = {}


def get_crypto_api_key(api_name: str) -> str:
    """Retrieve API key for crypto data providers from environment variables."""
    api_keys = {
        "coinmarketcap": os.getenv("COINMARKETCAP_API_KEY"),
        "cryptocompare": os.getenv("CRYPTOCOMPARE_API_KEY"),
        "coingecko": os.getenv("COINGECKO_API_KEY"),  # Optional for higher limits
    }
    
    api_key = api_keys.get(api_name.lower())
    if not api_key and api_name.lower() == "coinmarketcap":
        raise ValueError(f"{api_name.upper()}_API_KEY environment variable is not set.")
    return api_key


def _rate_limit(api_name: str):
    """Implement rate limiting for API calls."""
    current_time = time.time()
    last_time = _last_request.get(api_name, 0)
    
    if current_time - last_time < 60 / RATE_LIMITS.get(api_name, 10):
        time.sleep(60 / RATE_LIMITS.get(api_name, 10))
    
    _last_request[api_name] = time.time()


def _symbol_to_coin_id(symbol: str) -> str:
    """Map common symbols to API-specific coin IDs."""
    symbol_mappings = {
        # CoinGecko IDs
        "BTC-USD": "bitcoin",
        "ETH-USD": "ethereum", 
        "ADA-USD": "cardano",
        "SOL-USD": "solana",
        "DOGE-USD": "dogecoin",
        "XRP-USD": "ripple",
        "LTC-USD": "litecoin",
        "DOT-USD": "polkadot",
        "LINK-USD": "chainlink",
        "MATIC-USD": "matic-network",
        "AVAX-USD": "avalanche-2",
        "ATOM-USD": "cosmos",
        "ALGO-USD": "algorand",
        "FIL-USD": "filecoin",
        "BNB-USD": "binancecoin",
        "XLM-USD": "stellar",
        "EOS-USD": "eos",
        "TRX-USD": "tron",
        "XMR-USD": "monero",
        "DASH-USD": "dash",
        "ZEC-USD": "zcash",
    }
    
    return symbol_mappings.get(symbol.upper(), symbol.lower().replace("-usd", ""))


def get_crypto_data(
    symbol: Annotated[str, "cryptocurrency symbol (e.g., BTC-USD, ETH-USD)"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
):
    """Get cryptocurrency OHLCV data with enhanced API support."""
    
    # Input validation
    if not symbol or not start_date or not end_date:
        return "Error: Symbol, start_date, and end_date are required"
    
    try:
        config = get_config()
        vendor = config["data_vendors"].get("core_stock_apis", "yfinance")
        
        if vendor == "crypto":
            # Try enhanced APIs in order of preference
            for api_name in ["coingecko", "cryptocompare"]:
                try:
                    if api_name == "coingecko":
                        result = _get_crypto_data_coingecko(symbol, start_date, end_date)
                        if result and "No data found" not in result and "Error" not in result:
                            return result
                    elif api_name == "cryptocompare":
                        result = _get_crypto_data_cryptocompare(symbol, start_date, end_date)
                        if result and "No data found" not in result and "Error" not in result:
                            return result
                except Exception as e:
                    print(f"{api_name} API failed for {symbol}: {e}")
                    continue
        
        # Fallback to yfinance
        return _get_crypto_data_yfinance(symbol, start_date, end_date)
    
    except Exception as e:
        return f"Error fetching crypto data for {symbol}: {str(e)}"


def _get_crypto_data_yfinance(
    symbol: str,
    start_date: str,
    end_date: str
):
    """Get cryptocurrency data using yfinance (fallback)."""
    
    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")

    # Create ticker object
    ticker = yf.Ticker(symbol.upper())

    # Fetch historical data for the specified date range
    data = ticker.history(start=start_date, end=end_date)

    # Check if data is empty
    if data.empty:
        return (
            f"No data found for crypto symbol '{symbol}' between {start_date} and {end_date}"
        )

    # Remove timezone info from index for cleaner output
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    # Round numerical values to appropriate decimal places for crypto
    numeric_columns = ["Open", "High", "Low", "Close", "Adj Close"]
    for col in numeric_columns:
        if col in data.columns:
            data[col] = data[col].round(6)  # More decimal places for crypto

    # Convert DataFrame to CSV string
    csv_string = data.to_csv()

    # Add header information
    header = f"# Crypto data for {symbol.upper()} from {start_date} to {end_date}\n"
    header += f"# Total records: {len(data)}\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += "# Note: Crypto data is 24/7, includes weekends and holidays\n"
    header += "# Source: Yahoo Finance\n\n"

    return header + csv_string


def _get_crypto_data_coingecko(
    symbol: str,
    start_date: str,
    end_date: str
):
    """Get enhanced cryptocurrency data using CoinGecko API."""
    
    coin_id = _symbol_to_coin_id(symbol)
    
    try:
        _rate_limit("coingecko")
        
        # Convert dates to timestamps
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # CoinGecko API call for historical data
        url = f"{COINGECKO_API_BASE}/coins/{coin_id}/market_chart/range"
        params = {
            "vs_currency": "usd",
            "from": int(start_dt.timestamp()),
            "to": int(end_dt.timestamp())
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Process the data
        if "prices" not in data:
            return f"No price data available for {symbol}"
        
        # Create DataFrame from CoinGecko data
        prices = data.get("prices", [])
        volumes = data.get("total_volumes", [])
        
        if not prices:
            return f"No price data found for {symbol}"
        
        # Create DataFrame
        df_data = []
        for i, (timestamp, price) in enumerate(prices):
            date = datetime.fromtimestamp(timestamp / 1000)
            volume = volumes[i][1] if i < len(volumes) else 0
            
            # For simplicity, use same price for OHLC (real APIs provide separate OHLC)
            df_data.append({
                'Date': date,
                'Open': price,
                'High': price,
                'Low': price,
                'Close': price,
                'Volume': volume
            })
        
        df = pd.DataFrame(df_data)
        df.set_index('Date', inplace=True)
        
        # Convert to CSV string
        csv_string = df.to_csv()
        
        # Add header information
        header = f"# Enhanced Crypto data for {symbol.upper()} from {start_date} to {end_date}\n"
        header += f"# Total records: {len(df)}\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "# Note: Crypto data is 24/7, includes weekends and holidays\n"
        header += "# Source: CoinGecko API\n\n"
        
        return header + csv_string
        
    except Exception as e:
        raise Exception(f"CoinGecko API failed: {str(e)}")


def _get_crypto_data_cryptocompare(
    symbol: str,
    start_date: str,
    end_date: str
):
    """Get cryptocurrency data using CryptoCompare API."""
    
    try:
        _rate_limit("cryptocompare")
        
        # Map symbol to CryptoCompare format
        symbol_map = {
            "BTC-USD": "BTC",
            "ETH-USD": "ETH",
            "ADA-USD": "ADA",
            "SOL-USD": "SOL",
            "DOGE-USD": "DOGE",
            "XRP-USD": "XRP",
            "LTC-USD": "LTC",
            "DOT-USD": "DOT",
            "LINK-USD": "LINK",
            "MATIC-USD": "MATIC",
            "AVAX-USD": "AVAX",
            "ATOM-USD": "ATOM",
            "ALGO-USD": "ALGO",
            "FIL-USD": "FIL",
        }
        
        crypto_symbol = symbol_map.get(symbol.upper(), symbol.upper().replace("-USD", ""))
        
        # CryptoCompare API call for historical daily data
        url = f"{CRYPTOCOMPARE_API_BASE}/v2/histoday"
        params = {
            "fsym": crypto_symbol,
            "tsym": "USD",
            "limit": 2000,  # Maximum limit
            "toTs": int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()),
            "api_key": get_crypto_api_key("cryptocompare") or ""
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "Error":
            raise Exception(f"CryptoCompare API error: {data.get('Message', 'Unknown error')}")
        
        # Process the data
        if "Data" not in data or not data["Data"]["Data"]:
            return f"No price data available for {symbol}"
        
        # Create DataFrame
        df_data = []
        for entry in data["Data"]["Data"]:
            date = datetime.fromtimestamp(entry["time"])
            df_data.append({
                'Date': date,
                'Open': entry["open"],
                'High': entry["high"],
                'Low': entry["low"],
                'Close': entry["close"],
                'Volume': entry["volumeto"]  # Volume in USD
            })
        
        df = pd.DataFrame(df_data)
        df.set_index('Date', inplace=True)
        
        # Filter by date range
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        df = df[(df.index >= start_dt) & (df.index <= end_dt)]
        
        if df.empty:
            return f"No data found for {symbol} in the specified date range"
        
        # Convert to CSV string
        csv_string = df.to_csv()
        
        # Add header information
        header = f"# Enhanced Crypto data for {symbol.upper()} from {start_date} to {end_date}\n"
        header += f"# Total records: {len(df)}\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "# Note: Crypto data is 24/7, includes weekends and holidays\n"
        header += "# Source: CryptoCompare API\n\n"
        
        return header + csv_string
        
    except Exception as e:
        raise Exception(f"CryptoCompare API failed: {str(e)}")


def get_crypto_info(
    symbol: Annotated[str, "cryptocurrency symbol (e.g., BTC-USD, ETH-USD)"]
):
    """Get comprehensive cryptocurrency information with enhanced data."""
    
    config = get_config()
    vendor = config["data_vendors"].get("core_stock_apis", "yfinance")
    
    if vendor == "crypto":
        # Try enhanced APIs
        for api_name in ["coingecko", "coinmarketcap"]:
            try:
                if api_name == "coingecko":
                    return _get_crypto_info_coingecko(symbol)
                elif api_name == "coinmarketcap":
                    return _get_crypto_info_coinmarketcap(symbol)
            except Exception as e:
                print(f"{api_name} info API failed for {symbol}: {e}")
                continue
    
    # Fallback to yfinance
    return _get_crypto_info_yfinance(symbol)


def _get_crypto_info_yfinance(symbol: str):
    """Get crypto info using yfinance."""
    
    ticker = yf.Ticker(symbol.upper())
    
    try:
        info = ticker.info
        
        # Extract relevant information
        name = info.get('longName', info.get('shortName', 'N/A'))
        currency = info.get('currency', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        volume_24h = info.get('volume24Hr', info.get('regularMarketVolume', 'N/A'))
        price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        prev_close = info.get('previousClose', 'N/A')
        open_price = info.get('open', 'N/A')
        day_high = info.get('dayHigh', 'N/A')
        day_low = info.get('dayLow', 'N/A')
        week_52_high = info.get('fiftyTwoWeekHigh', 'N/A')
        week_52_low = info.get('fiftyTwoWeekLow', 'N/A')
        
        info_str = f"# Crypto Information for {symbol.upper()}\n\n"
        info_str += f"Name: {name}\n"
        info_str += f"Full Name: {name}\n"
        info_str += f"Currency: {currency}\n"
        info_str += f"Market Cap: {market_cap}\n"
        info_str += f"24h Volume: {volume_24h}\n"
        info_str += f"Price: {price}\n"
        info_str += f"Previous Close: {prev_close}\n"
        info_str += f"Open: {open_price}\n"
        info_str += f"Day High: {day_high}\n"
        info_str += f"Day Low: {day_low}\n"
        info_str += f"52 Week High: {week_52_high}\n"
        info_str += f"52 Week Low: {week_52_low}\n"
        
        # Add additional crypto-specific info
        info_str += "\n# Additional Information\n"
        info_str += f"Circulating Supply: {info.get('circulatingSupply', 'N/A')}\n"
        info_str += f"Total Supply: {info.get('totalSupply', 'N/A')}\n"
        info_str += f"Max Supply: {info.get('maxSupply', 'N/A')}\n"
        
        return info_str
        
    except Exception as e:
        return f"Error retrieving crypto info for {symbol}: {str(e)}"


def _get_crypto_info_coingecko(symbol: str):
    """Get comprehensive crypto info using CoinGecko API."""
    
    coin_id = _symbol_to_coin_id(symbol)
    
    try:
        _rate_limit("coingecko")
        
        # CoinGecko API call for coin data
        url = f"{COINGECKO_API_BASE}/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "true",
            "developer_data": "true",
            "sparkline": "false"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract comprehensive information
        market_data = data.get("market_data", {})
        community_data = data.get("community_data", {})
        developer_data = data.get("developer_data", {})
        
        info_str = f"# Enhanced Crypto Information for {symbol.upper()}\n\n"
        info_str += f"Name: {data.get('name', 'N/A')}\n"
        info_str += f"Symbol: {data.get('symbol', 'N/A').upper()}\n"
        info_str += f"Rank: #{data.get('market_cap_rank', 'N/A')}\n"
        
        # Market Data
        info_str += "\n# Market Data\n"
        info_str += f"Current Price: ${market_data.get('current_price', {}).get('usd', 'N/A')}\n"
        info_str += f"Market Cap: ${market_data.get('market_cap', {}).get('usd', 'N/A')}\n"
        info_str += f"24h Volume: ${market_data.get('total_volume', {}).get('usd', 'N/A')}\n"
        info_str += f"24h Price Change: {market_data.get('price_change_percentage_24h', 'N/A')}%\n"
        info_str += f"24h High: ${market_data.get('high_24h', {}).get('usd', 'N/A')}\n"
        info_str += f"24h Low: ${market_data.get('low_24h', {}).get('usd', 'N/A')}\n"
        info_str += f"ATH: ${market_data.get('ath', {}).get('usd', 'N/A')}\n"
        info_str += f"ATL: ${market_data.get('atl', {}).get('usd', 'N/A')}\n"
        
        # Supply Data
        info_str += "\n# Supply Data\n"
        info_str += f"Circulating Supply: {market_data.get('circulating_supply', 'N/A')}\n"
        info_str += f"Total Supply: {market_data.get('total_supply', 'N/A')}\n"
        info_str += f"Max Supply: {market_data.get('max_supply', 'N/A')}\n"
        
        # Community Data
        info_str += "\n# Community Data\n"
        info_str += f"Twitter Followers: {community_data.get('twitter_followers', 'N/A')}\n"
        info_str += f"Reddit Subscribers: {community_data.get('reddit_subscribers', 'N/A')}\n"
        
        # Developer Data
        info_str += "\n# Developer Data\n"
        info_str += f"GitHub Stars: {developer_data.get('stars', 'N/A')}\n"
        info_str += f"GitHub Forks: {developer_data.get('forks', 'N/A')}\n"
        
        info_str += "\n# Source: CoinGecko API\n"
        
        return info_str
        
    except Exception as e:
        raise Exception(f"CoinGecko info API failed: {str(e)}")


def _get_crypto_info_coinmarketcap(symbol: str):
    """Get crypto info using CoinMarketCap API."""
    
    try:
        _rate_limit("coinmarketcap")
        
        # Map symbol to CoinMarketCap format
        symbol_map = {
            "BTC-USD": "BTC",
            "ETH-USD": "ETH",
            "ADA-USD": "ADA",
            "SOL-USD": "SOL",
            "DOGE-USD": "DOGE",
            "XRP-USD": "XRP",
            "LTC-USD": "LTC",
            "DOT-USD": "DOT",
            "LINK-USD": "LINK",
            "MATIC-USD": "MATIC",
            "AVAX-USD": "AVAX",
            "ATOM-USD": "ATOM",
            "ALGO-USD": "ALGO",
            "FIL-USD": "FIL",
        }
        
        crypto_symbol = symbol_map.get(symbol.upper(), symbol.upper().replace("-USD", ""))
        
        # CoinMarketCap API call
        url = f"{COINMARKETCAP_API_BASE}/cryptocurrency/quotes/latest"
        headers = {
            "X-CMC_PRO_API_KEY": get_crypto_api_key("coinmarketcap")
        }
        params = {
            "symbol": crypto_symbol,
            "convert": "USD"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "data" not in data or crypto_symbol not in data["data"]:
            return f"No data found for {symbol}"
        
        coin_data = data["data"][crypto_symbol][0]
        quote_data = coin_data["quote"]["USD"]
        
        info_str = f"# Enhanced Crypto Information for {symbol.upper()}\n\n"
        info_str += f"Name: {coin_data.get('name', 'N/A')}\n"
        info_str += f"Symbol: {coin_data.get('symbol', 'N/A')}\n"
        info_str += f"Rank: #{coin_data.get('cmc_rank', 'N/A')}\n"
        
        # Market Data
        info_str += "\n# Market Data\n"
        info_str += f"Current Price: ${quote_data.get('price', 'N/A')}\n"
        info_str += f"Market Cap: ${quote_data.get('market_cap', 'N/A')}\n"
        info_str += f"24h Volume: ${quote_data.get('volume_24h', 'N/A')}\n"
        info_str += f"24h Price Change: {quote_data.get('percent_change_24h', 'N/A')}%\n"
        info_str += f"24h High: ${quote_data.get('high_24h', 'N/A')}\n"
        info_str += f"24h Low: ${quote_data.get('low_24h', 'N/A')}\n"
        
        # Supply Data
        info_str += "\n# Supply Data\n"
        info_str += f"Circulating Supply: {coin_data.get('circulating_supply', 'N/A')}\n"
        info_str += f"Total Supply: {coin_data.get('total_supply', 'N/A')}\n"
        info_str += f"Max Supply: {coin_data.get('max_supply', 'N/A')}\n"
        
        info_str += "\n# Source: CoinMarketCap API\n"
        
        return info_str
        
    except Exception as e:
        raise Exception(f"CoinMarketCap API failed: {str(e)}")


def get_crypto_news(
    symbol: Annotated[str, "cryptocurrency symbol (e.g., BTC-USD, ETH-USD)"]
):
    """Get cryptocurrency news from multiple sources."""
    
    config = get_config()
    vendor = config["data_vendors"].get("news_data", "alpha_vantage")
    
    if vendor == "crypto":
        try:
            return _get_crypto_news_enhanced(symbol)
        except Exception as e:
            print(f"Enhanced crypto news failed: {e}")
    
    # Fallback to placeholder
    return f"# Crypto News for {symbol.upper()}\n\nCrypto-specific news integration coming soon. Currently using general market news."


def _get_crypto_news_enhanced(symbol: str):
    """Get enhanced crypto news using multiple sources."""
    
    coin_id = _symbol_to_coin_id(symbol)
    
    try:
        _rate_limit("coingecko")
        
        # CoinGecko API for news
        url = f"{COINGECKO_API_BASE}/coins/{coin_id}/status_updates"
        params = {
            "per_page": 10
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        news_str = f"# Crypto News for {symbol.upper()}\n\n"
        
        if "status_updates" in data and data["status_updates"]:
            for i, update in enumerate(data["status_updates"][:5]):
                news_str += f"## News {i+1}\n"
                news_str += f"Title: {update.get('description', 'N/A')}\n"
                news_str += f"Date: {update.get('created_at', 'N/A')}\n"
                news_str += f"User: {update.get('user', 'N/A')}\n\n"
        else:
            news_str += "No recent news updates available.\n\n"
        
        news_str += "# Additional News Sources\n"
        news_str += "- Crypto-specific news aggregation coming soon\n"
        news_str += "- Social media sentiment analysis in development\n"
        news_str += "- On-chain metrics integration planned\n"
        
        return news_str
        
    except Exception as e:
        raise Exception(f"Crypto news API failed: {str(e)}")


def get_crypto_indicators(
    symbol: Annotated[str, "cryptocurrency symbol (e.g., BTC-USD, ETH-USD)"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[str, "The current trading date you are trading on, YYYY-mm-dd"],
    look_back_days: Annotated[int, "how many days to look back"],
):
    """Get technical indicators for cryptocurrency with enhanced crypto-specific indicators."""
    
    config = get_config()
    vendor = config["data_vendors"].get("technical_indicators", "yfinance")
    
    if vendor == "crypto":
        try:
            return _get_crypto_indicators_enhanced(symbol, indicator, curr_date, look_back_days)
        except Exception as e:
            print(f"Enhanced crypto indicators failed: {e}")
    
    # Fallback to stock indicators
    from .y_finance import get_stock_stats_indicators_window
    
    try:
        return get_stock_stats_indicators_window(symbol, indicator, curr_date, look_back_days)
    except Exception as e:
        return f"Error getting crypto indicators for {symbol}: {str(e)}"


def _get_crypto_indicators_enhanced(
    symbol: str,
    indicator: str,
    curr_date: str,
    look_back_days: int
):
    """Get enhanced crypto-specific technical indicators."""
    
    # Crypto-specific indicators
    crypto_indicators = {
        "nvt_ratio": (
            "NVT Ratio: Network Value to Transactions ratio. "
            "Usage: Measures if a cryptocurrency is overvalued relative to its transaction volume. "
            "Tips: High NVT suggests overvaluation, low NVT suggests undervaluation."
        ),
        "mayer_multiple": (
            "Mayer Multiple: Current price divided by 200-day moving average. "
            "Usage: Identifies overbought/oversold conditions in Bitcoin. "
            "Tips: Values below 1 suggest undervaluation, above 2.4 suggest overvaluation."
        ),
        "puell_multiple": (
            "Puell Multiple: Daily issuance value divided by 365-day moving average. "
            "Usage: Measures miner profitability and selling pressure. "
            "Tips: High values suggest miner selling pressure, low values suggest accumulation."
        ),
        "rhodl_ratio": (
            "RHODL Ratio: Ratio of 1-week to 1-2 year UTXO age bands. "
            "Usage: Identifies market cycle extremes. "
            "Tips: High values suggest market tops, low values suggest market bottoms."
        ),
    }
    
    if indicator in crypto_indicators:
        # For now, return placeholder for crypto-specific indicators
        result_str = (
            f"## {indicator} values from {curr_date} (looking back {look_back_days} days):\n\n"
            f"Crypto-specific indicator '{indicator}' analysis coming soon.\n"
            f"Currently using standard technical indicators.\n\n"
            + crypto_indicators[indicator]
        )
        return result_str
    else:
        # Use standard indicators
        from .y_finance import get_stock_stats_indicators_window
        return get_stock_stats_indicators_window(symbol, indicator, curr_date, look_back_days)


def get_crypto_social_sentiment(
    symbol: Annotated[str, "cryptocurrency symbol (e.g., BTC-USD, ETH-USD)"]
):
    """Get social media sentiment for cryptocurrency."""
    
    coin_id = _symbol_to_coin_id(symbol)
    
    try:
        _rate_limit("coingecko")
        
        # CoinGecko API for community data
        url = f"{COINGECKO_API_BASE}/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "false",
            "community_data": "true",
            "developer_data": "false",
            "sparkline": "false"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        community_data = data.get("community_data", {})
        
        sentiment_str = f"# Social Media Sentiment for {symbol.upper()}\n\n"
        
        sentiment_str += "## Community Metrics\n"
        sentiment_str += f"Twitter Followers: {community_data.get('twitter_followers', 'N/A')}\n"
        sentiment_str += f"Reddit Subscribers: {community_data.get('reddit_subscribers', 'N/A')}\n"
        sentiment_str += f"Reddit Active Users: {community_data.get('reddit_accounts_active_48h', 'N/A')}\n"
        
        sentiment_str += "\n## Sentiment Analysis\n"
        sentiment_str += "- Real-time social sentiment analysis coming soon\n"
        sentiment_str += "- Reddit and Twitter sentiment integration planned\n"
        sentiment_str += "- Telegram and Discord community metrics in development\n"
        
        return sentiment_str
        
    except Exception as e:
        return f"Error retrieving social sentiment for {symbol}: {str(e)}"