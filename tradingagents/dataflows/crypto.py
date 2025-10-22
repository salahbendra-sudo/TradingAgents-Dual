"""
Crypto data vendor module for TradingAgents.
Provides crypto-specific data fetching functions for cryptocurrencies.
"""

from typing import Annotated
from datetime import datetime
import yfinance as yf
import pandas as pd


def get_crypto_data(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
):
    """
    Retrieve cryptocurrency price data (OHLCV) for a given symbol.
    
    Args:
        symbol (str): Crypto symbol, e.g., BTC-USD, ETH-USD
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    
    Returns:
        str: A formatted dataframe containing the crypto price data
    """
    # Validate date format
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

    # Round numerical values to appropriate decimal places
    numeric_columns = ["Open", "High", "Low", "Close", "Adj Close"]
    for col in numeric_columns:
        if col in data.columns:
            # Use more decimal places for crypto (typically higher precision needed)
            data[col] = data[col].round(6)

    # Convert DataFrame to CSV string
    csv_string = data.to_csv()

    # Add header information
    header = f"# Crypto data for {symbol.upper()} from {start_date} to {end_date}\n"
    header += f"# Total records: {len(data)}\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += f"# Note: Crypto data is 24/7, includes weekends and holidays\n\n"

    return header + csv_string


def get_crypto_info(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"]
):
    """
    Get basic information about a cryptocurrency.
    
    Args:
        symbol (str): Crypto symbol, e.g., BTC-USD, ETH-USD
    
    Returns:
        str: Formatted information about the cryptocurrency
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        if not info:
            return f"No information found for crypto symbol '{symbol}'"
        
        # Extract relevant crypto information
        result = f"# Crypto Information for {symbol.upper()}\n\n"
        
        # Basic info
        result += f"Name: {info.get('shortName', 'N/A')}\n"
        result += f"Full Name: {info.get('longName', 'N/A')}\n"
        result += f"Currency: {info.get('currency', 'N/A')}\n"
        result += f"Market Cap: {info.get('marketCap', 'N/A')}\n"
        result += f"24h Volume: {info.get('volume24Hr', info.get('regularMarketVolume', 'N/A'))}\n"
        result += f"Price: {info.get('regularMarketPrice', info.get('currentPrice', 'N/A'))}\n"
        result += f"Previous Close: {info.get('previousClose', 'N/A')}\n"
        result += f"Open: {info.get('open', 'N/A')}\n"
        result += f"Day High: {info.get('dayHigh', 'N/A')}\n"
        result += f"Day Low: {info.get('dayLow', 'N/A')}\n"
        result += f"52 Week High: {info.get('fiftyTwoWeekHigh', 'N/A')}\n"
        result += f"52 Week Low: {info.get('fiftyTwoWeekLow', 'N/A')}\n"
        
        # Additional crypto-specific info
        result += f"\n# Additional Information\n"
        result += f"Algorithm: {info.get('algorithm', 'N/A')}\n"
        result += f"Proof Type: {info.get('proofType', 'N/A')}\n"
        result += f"Asset Class: {info.get('quoteType', 'N/A')}\n"
        result += f"Exchange: {info.get('exchange', 'N/A')}\n"
        result += f"Exchange Timezone: {info.get('exchangeTimezoneName', 'N/A')}\n"
        
        return result
        
    except Exception as e:
        return f"Error retrieving crypto info for {symbol}: {str(e)}"


def get_crypto_news(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"]
):
    """
    Get news related to a cryptocurrency.
    Note: This is a placeholder - yfinance doesn't provide crypto-specific news.
    In a real implementation, you might use a crypto-specific news API.
    
    Args:
        symbol (str): Crypto symbol
    
    Returns:
        str: News information (placeholder)
    """
    return f"# Crypto News for {symbol.upper()}\n\nNote: Crypto news functionality requires integration with crypto-specific news APIs.\nCurrently using general market news for crypto analysis.\n"


def get_crypto_indicators(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"],
    indicator: Annotated[str, "technical indicator to calculate"],
    curr_date: Annotated[str, "current date for reference"],
    look_back_days: Annotated[int, "how many days to look back"]
):
    """
    Get technical indicators for cryptocurrency.
    Uses the same implementation as stocks since the calculation is the same.
    
    Args:
        symbol (str): Crypto symbol
        indicator (str): Technical indicator name
        curr_date (str): Current date
        look_back_days (int): Number of days to look back
    
    Returns:
        str: Technical indicator values
    """
    # For now, use the same implementation as stocks
    # In the future, we might want crypto-specific indicators
    from .y_finance import get_stock_stats_indicators_window
    
    try:
        return get_stock_stats_indicators_window(symbol, indicator, curr_date, look_back_days)
    except Exception as e:
        return f"Error getting crypto indicators for {symbol}: {str(e)}"