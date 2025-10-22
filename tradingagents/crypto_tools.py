"""
Enhanced Crypto Tools for TradingAgents.
Provides comprehensive cryptocurrency analysis tools with real-time data.
"""

from typing import Annotated
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from io import StringIO
from .dataflows.crypto_enhanced import (
    get_crypto_data, 
    get_crypto_info, 
    get_crypto_news, 
    get_crypto_indicators,
    get_crypto_social_sentiment
)


def analyze_crypto_market(
    symbol: Annotated[str, "cryptocurrency symbol (e.g., BTC-USD, ETH-USD)"],
    period_days: Annotated[int, "Number of days to analyze"] = 30
):
    """Comprehensive cryptocurrency market analysis."""
    
    # Input validation
    if not symbol:
        return "Error: Symbol is required"
    if period_days <= 0:
        return "Error: Period days must be positive"
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
    
    try:
        # Get crypto data
        data_result = get_crypto_data(symbol, start_date, end_date)
        if "Error" in data_result or "No data found" in data_result:
            return f"Error analyzing crypto market for {symbol}: {data_result}"
        
        # Get crypto info
        info_result = get_crypto_info(symbol)
        
        # Get crypto news
        news_result = get_crypto_news(symbol)
        
        # Get social sentiment
        sentiment_result = get_crypto_social_sentiment(symbol)
        
        # Parse the data for analysis
        lines = data_result.split('\n')
        data_start = 0
        for i, line in enumerate(lines):
            if line.startswith('Date,') or line.startswith('Date	'):
                data_start = i
                break
        
        if data_start > 0:
            csv_data = '\n'.join(lines[data_start:])
            try:
                df = pd.read_csv(StringIO(csv_data))
            except Exception as e:
                return f"Error parsing crypto data for {symbol}: {str(e)}"
            
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                
                # Calculate metrics
                latest_price = df['Close'].iloc[-1]
                price_change = df['Close'].iloc[-1] - df['Close'].iloc[0]
                price_change_pct = (price_change / df['Close'].iloc[0]) * 100
                
                volatility = df['Close'].pct_change().std() * 100
                avg_volume = df['Volume'].mean()
                
                # Technical indicators
                df['SMA_20'] = df['Close'].rolling(window=20).mean()
                df['SMA_50'] = df['Close'].rolling(window=50).mean()
                
                # RSI calculation
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                df['RSI'] = 100 - (100 / (1 + rs))
                
                current_rsi = df['RSI'].iloc[-1]
                
                analysis = f"""# Comprehensive Crypto Analysis for {symbol.upper()}

## Price Analysis
- Current Price: ${latest_price:.2f}
- {period_days}-Day Change: ${price_change:.2f} ({price_change_pct:.2f}%)
- Volatility: {volatility:.2f}%
- Average Daily Volume: {avg_volume:,.0f}

## Technical Indicators
- RSI (14): {current_rsi:.2f} {'(Overbought)' if current_rsi > 70 else '(Oversold)' if current_rsi < 30 else '(Neutral)'}
- 20-Day SMA: ${df['SMA_20'].iloc[-1]:.2f}
- 50-Day SMA: ${df['SMA_50'].iloc[-1]:.2f}

## Market Position
- Price vs 20-SMA: {'Above' if latest_price > df['SMA_20'].iloc[-1] else 'Below'}
- Price vs 50-SMA: {'Above' if latest_price > df['SMA_50'].iloc[-1] else 'Below'}

## Additional Data
{info_result}

## Recent News
{news_result}

## Social Sentiment
{sentiment_result}
"""
                return analysis
        
        return f"Unable to analyze {symbol} data. Please check the symbol and try again."
        
    except Exception as e:
        return f"Error analyzing crypto market for {symbol}: {str(e)}"


def get_crypto_portfolio_analysis(
    symbols: Annotated[str, "Comma-separated cryptocurrency symbols (e.g., BTC-USD,ETH-USD,SOL-USD)"],
    period_days: Annotated[int, "Number of days to analyze"] = 30
):
    """Analyze multiple cryptocurrencies for portfolio construction."""
    
    # Input validation
    if not symbols:
        return "Error: Symbols are required"
    if period_days <= 0:
        return "Error: Period days must be positive"
    
    symbol_list = [s.strip() for s in symbols.split(',') if s.strip()]
    
    if not symbol_list:
        return "Error: No valid symbols provided"
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
    
    analysis_results = []
    
    for symbol in symbol_list:
        try:
            data_result = get_crypto_data(symbol, start_date, end_date)
            
            # Parse data
            lines = data_result.split('\n')
            data_start = 0
            for i, line in enumerate(lines):
                if line.startswith('Date,') or line.startswith('Date\t'):
                    data_start = i
                    break
            
            if data_start > 0:
                csv_data = '\n'.join(lines[data_start:])
                try:
                    df = pd.read_csv(StringIO(csv_data))
                except Exception as e:
                    analysis_results.append(f"Error parsing data for {symbol}: {str(e)}")
                    continue
                
                if not df.empty:
                    df['Date'] = pd.to_datetime(df['Date'])
                    df.set_index('Date', inplace=True)
                    
                    latest_price = df['Close'].iloc[-1]
                    price_change_pct = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
                    volatility = df['Close'].pct_change().std() * 100
                    
                    analysis_results.append({
                        'symbol': symbol,
                        'price': latest_price,
                        'change_pct': price_change_pct,
                        'volatility': volatility
                    })
        
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
    
    if not analysis_results:
        return "No valid data found for the provided symbols."
    
    # Create portfolio analysis
    analysis = f"# Crypto Portfolio Analysis\n\n"
    analysis += f"Period: {period_days} days\n\n"
    
    for result in analysis_results:
        analysis += f"## {result['symbol']}\n"
        analysis += f"- Current Price: ${result['price']:.2f}\n"
        analysis += f"- {period_days}-Day Return: {result['change_pct']:.2f}%\n"
        analysis += f"- Volatility: {result['volatility']:.2f}%\n\n"
    
    # Calculate portfolio metrics
    total_return = sum(r['change_pct'] for r in analysis_results) / len(analysis_results)
    avg_volatility = sum(r['volatility'] for r in analysis_results) / len(analysis_results)
    
    analysis += f"## Portfolio Summary\n"
    analysis += f"- Average Return: {total_return:.2f}%\n"
    analysis += f"- Average Volatility: {avg_volatility:.2f}%\n"
    analysis += f"- Sharpe Ratio (approx): {total_return / avg_volatility if avg_volatility > 0 else 'N/A'}\n"
    
    return analysis


def get_crypto_market_overview():
    """Get overview of major cryptocurrency markets."""
    
    major_cryptos = ["BTC-USD", "ETH-USD", "ADA-USD", "SOL-USD", "DOGE-USD"]
    
    overview = "# Crypto Market Overview\n\n"
    
    for symbol in major_cryptos:
        try:
            info_result = get_crypto_info(symbol)
            
            # Extract key info
            lines = info_result.split('\n')
            price_line = next((line for line in lines if 'Current Price' in line), None)
            change_line = next((line for line in lines if '24h Price Change' in line), None)
            
            if price_line and change_line:
                price = price_line.split(': $')[-1].strip()
                change = change_line.split(': ')[-1].replace('%', '').strip()
                
                overview += f"## {symbol}\n"
                overview += f"- Price: ${price}\n"
                overview += f"- 24h Change: {change}%\n\n"
        
        except Exception as e:
            overview += f"## {symbol}\n"
            overview += f"- Error retrieving data\n\n"
    
    overview += "## Market Summary\n"
    overview += "- Real-time market data from multiple sources\n"
    overview += "- Enhanced analytics with social sentiment\n"
    overview += "- Portfolio optimization tools available\n"
    
    return overview


def get_crypto_technical_analysis(
    symbol: Annotated[str, "cryptocurrency symbol (e.g., BTC-USD, ETH-USD)"],
    indicators: Annotated[str, "Comma-separated technical indicators"] = "rsi,macd,boll"
):
    """Get comprehensive technical analysis for cryptocurrency."""
    
    indicator_list = [ind.strip() for ind in indicators.split(',')]
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    analysis = f"# Technical Analysis for {symbol.upper()}\n\n"
    
    for indicator in indicator_list:
        try:
            indicator_result = get_crypto_indicators(symbol, indicator, curr_date, 30)
            analysis += indicator_result + "\n\n"
        except Exception as e:
            analysis += f"## {indicator.upper()}\n"
            analysis += f"Error retrieving {indicator}: {str(e)}\n\n"
    
    return analysis

def get_crypto_correlation_analysis(
    symbols: Annotated[str, "Comma-separated cryptocurrency symbols (e.g., BTC-USD,ETH-USD,SOL-USD)"],
    period_days: Annotated[int, "Number of days for correlation analysis"] = 90
):
    """
    Analyze correlation between multiple cryptocurrencies.
    
    Args:
        symbols: Comma-separated cryptocurrency symbols
        period_days: Number of days for analysis
        
    Returns:
        Correlation analysis report
    """
    # Input validation
    if not symbols:
        return "Error: Symbols are required"
    if period_days <= 0:
        return "Error: Period days must be positive"
    
    symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]
    
    if len(symbol_list) < 2:
        return "Error: At least 2 symbols are required for correlation analysis"
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
    
    try:
        # Collect price data for all symbols
        price_data = {}
        
        for symbol in symbol_list:
            data_result = get_crypto_data(symbol, start_date, end_date)
            
            if "Error" in data_result or "No data found" in data_result:
                return f"Error getting data for {symbol}: {data_result}"
            
            # Parse the data
            lines = data_result.split("\n")
            data_start = 0
            for i, line in enumerate(lines):
                if line.startswith("Date,") or line.startswith("Date\t"):
                    data_start = i
                    break
            
            if data_start > 0:
                csv_data = "\n".join(lines[data_start:])
                try:
                    df = pd.read_csv(StringIO(csv_data))
                    if not df.empty:
                        df["Date"] = pd.to_datetime(df["Date"])
                        df.set_index("Date", inplace=True)
                        price_data[symbol] = df["Close"]
                except Exception as e:
                    return f"Error parsing data for {symbol}: {str(e)}"
        
        # Create correlation matrix
        if len(price_data) >= 2:
            # Combine all price series
            combined_df = pd.DataFrame(price_data)
            
            # Calculate correlations
            correlation_matrix = combined_df.corr()
            
            # Generate analysis
            analysis = f"# Crypto Correlation Analysis\n\n"
            analysis += f"## Period: {start_date} to {end_date} ({period_days} days)\n\n"
            analysis += f"## Correlation Matrix\n\n"
            
            # Format correlation matrix
            for i, sym1 in enumerate(symbol_list):
                if sym1 in correlation_matrix.columns:
                    analysis += f"**{sym1}**:\n"
                    for j, sym2 in enumerate(symbol_list):
                        if i != j and sym2 in correlation_matrix.columns:
                            corr = correlation_matrix.loc[sym1, sym2]
                            analysis += f"  - {sym2}: {corr:.3f}\n"
                    analysis += "\n"
            
            # Overall correlation insights
            analysis += "## Correlation Insights\n\n"
            
            # Find highest and lowest correlations
            correlations = []
            for i in range(len(symbol_list)):
                for j in range(i+1, len(symbol_list)):
                    sym1, sym2 = symbol_list[i], symbol_list[j]
                    if sym1 in correlation_matrix.columns and sym2 in correlation_matrix.columns:
                        corr = correlation_matrix.loc[sym1, sym2]
                        correlations.append((sym1, sym2, corr))
            
            if correlations:
                highest_corr = max(correlations, key=lambda x: x[2])
                lowest_corr = min(correlations, key=lambda x: x[2])
                
                analysis += f"- **Highest Correlation**: {highest_corr[0]} & {highest_corr[1]} ({highest_corr[2]:.3f})\n"
                analysis += f"- **Lowest Correlation**: {lowest_corr[0]} & {lowest_corr[1]} ({lowest_corr[2]:.3f})\n\n"
                
                # Interpretation
                analysis += "## Interpretation\n\n"
                analysis += "- **Correlation > 0.7**: Strong positive correlation (move together)\n"
                analysis += "- **Correlation 0.3-0.7**: Moderate positive correlation\n"
                analysis += "- **Correlation -0.3 to 0.3**: Weak or no correlation\n"
                analysis += "- **Correlation < -0.3**: Negative correlation (move opposite)\n"
            
            return analysis
        else:
            return "Error: Insufficient data for correlation analysis"
            
    except Exception as e:
        return f"Error performing correlation analysis: {str(e)}"
