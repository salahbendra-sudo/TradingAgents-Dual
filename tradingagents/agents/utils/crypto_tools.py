"""
Crypto-specific tools for TradingAgents.
Provides tools for cryptocurrency analysis.
"""

from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor


@tool
def get_crypto_data(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve cryptocurrency price data (OHLCV) for a given symbol.
    
    Args:
        symbol (str): Crypto symbol, e.g., BTC-USD, ETH-USD
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    
    Returns:
        str: A formatted dataframe containing the crypto price data
    """
    return route_to_vendor("get_stock_data", symbol, start_date, end_date)


@tool
def get_crypto_indicators(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[
        str, "The current trading date you are trading on, YYYY-mm-dd"
    ],
    look_back_days: Annotated[int, "how many days to look back"],
) -> str:
    """
    Get technical indicators for cryptocurrency.
    
    Args:
        symbol (str): Crypto symbol
        indicator (str): Technical indicator name
        curr_date (str): Current date
        look_back_days (int): Number of days to look back
    
    Returns:
        str: Technical indicator values
    """
    return route_to_vendor("get_indicators", symbol, indicator, curr_date, look_back_days)


@tool
def get_crypto_news(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"]
) -> str:
    """
    Get news related to a cryptocurrency.
    
    Args:
        symbol (str): Crypto symbol
    
    Returns:
        str: News information
    """
    return route_to_vendor("get_news", symbol)


@tool
def get_crypto_info(
    symbol: Annotated[str, "crypto symbol (e.g., BTC-USD, ETH-USD)"]
) -> str:
    """
    Get basic information about a cryptocurrency.
    
    Args:
        symbol (str): Crypto symbol, e.g., BTC-USD, ETH-USD
    
    Returns:
        str: Formatted information about the cryptocurrency
    """
    from tradingagents.dataflows.crypto import get_crypto_info as crypto_info_func
    return crypto_info_func(symbol)