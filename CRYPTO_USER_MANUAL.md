# Crypto Integration User Manual

## Overview

TradingAgents now includes comprehensive cryptocurrency analysis capabilities with multi-API support, real-time data, and crypto-specific analytics. This manual covers all aspects of using the crypto integration features.

## Quick Start

### Basic Crypto Analysis

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Initialize the trading graph
ta = TradingAgentsGraph(debug=True)

# Analyze Bitcoin
_, btc_decision = ta.propagate("BTC-USD", "2024-05-10")
print(f"Bitcoin Decision: {btc_decision}")

# Analyze Ethereum
_, eth_decision = ta.propagate("ETH-USD", "2024-05-10")
print(f"Ethereum Decision: {eth_decision}")
```

### Enhanced Crypto Tools

```python
from tradingagents.crypto_tools import (
    analyze_crypto_market,
    get_crypto_portfolio_analysis,
    get_crypto_correlation_analysis,
    get_crypto_market_overview,
    get_crypto_technical_analysis
)

# Comprehensive market analysis
analysis = analyze_crypto_market("BTC-USD", 30)

# Portfolio analysis for multiple cryptocurrencies
portfolio = get_crypto_portfolio_analysis("BTC-USD,ETH-USD,SOL-USD", 90)

# Correlation analysis between cryptocurrencies
correlation = get_crypto_correlation_analysis("BTC-USD,ETH-USD,SOL-USD", 30)

# Market overview
overview = get_crypto_market_overview()

# Technical analysis
technical = get_crypto_technical_analysis("BTC-USD", "rsi,macd,sma")
```

## Installation & Setup

### Required Dependencies

The crypto integration requires the standard TradingAgents dependencies plus additional crypto-specific packages:

```bash
# Install from requirements (already included)
pip install -r requirements.txt
```

### API Configuration

#### Required APIs
- **OpenAI API**: For all LLM agents
- **Alpha Vantage API**: For fundamental and news data (stocks)

#### Optional Crypto APIs (Enhanced Features)
- **CoinMarketCap API**: Premium crypto data
- **CryptoCompare API**: Historical data and social metrics
- **CoinGecko API**: Higher rate limits and enhanced data

#### Environment Setup

```bash
# Required APIs
export OPENAI_API_KEY="your_openai_api_key"
export ALPHA_VANTAGE_API_KEY="your_alpha_vantage_api_key"

# Optional crypto APIs (recommended for production)
export COINMARKETCAP_API_KEY="your_coinmarketcap_api_key"
export CRYPTOCOMPARE_API_KEY="your_cryptocompare_api_key"
export COINGECKO_API_KEY="your_coingecko_api_key"
```

#### .env File Setup

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
COINMARKETCAP_API_KEY=your_coinmarketcap_api_key
CRYPTOCOMPARE_API_KEY=your_cryptocompare_api_key
COINGECKO_API_KEY=your_coingecko_api_key
```

### API Key Sources

- **CoinMarketCap**: [Free API Key](https://coinmarketcap.com/api/)
- **CryptoCompare**: [Free API Key](https://min-api.cryptocompare.com/)
- **CoinGecko**: [Free API Key](https://www.coingecko.com/en/api)

## Supported Cryptocurrencies

### Major Cryptocurrencies
- `BTC-USD` - Bitcoin
- `ETH-USD` - Ethereum
- `ADA-USD` - Cardano
- `SOL-USD` - Solana
- `DOGE-USD` - Dogecoin
- `XRP-USD` - Ripple

### Altcoins
- `LTC-USD` - Litecoin
- `DOT-USD` - Polkadot
- `LINK-USD` - Chainlink
- `MATIC-USD` - Polygon
- `AVAX-USD` - Avalanche
- `ATOM-USD` - Cosmos
- `ALGO-USD` - Algorand
- `FIL-USD` - Filecoin

### Additional Cryptocurrencies
- `BNB-USD` - Binance Coin
- `XLM-USD` - Stellar
- `EOS-USD` - EOS
- `TRX-USD` - TRON
- `XMR-USD` - Monero
- `DASH-USD` - Dash
- `ZEC-USD` - Zcash

## Core Features

### 1. Market Analysis

Comprehensive analysis of individual cryptocurrencies including price analysis, technical indicators, market position, and social sentiment.

```python
from tradingagents.crypto_tools import analyze_crypto_market

# Analyze Bitcoin for the last 30 days
analysis = analyze_crypto_market("BTC-USD", 30)
print(analysis)
```

**Output Includes:**
- Current price and price change
- Volatility and volume analysis
- Technical indicators (RSI, SMA, etc.)
- Market position vs moving averages
- Social sentiment metrics
- Recent news summary

### 2. Portfolio Analysis

Analyze multiple cryptocurrencies together for portfolio construction and optimization.

```python
from tradingagents.crypto_tools import get_crypto_portfolio_analysis

# Analyze a portfolio of top cryptocurrencies
portfolio = get_crypto_portfolio_analysis("BTC-USD,ETH-USD,SOL-USD,ADA-USD", 90)
print(portfolio)
```

**Output Includes:**
- Individual performance metrics
- Portfolio diversification analysis
- Risk assessment
- Performance comparison
- Recommended allocations

### 3. Correlation Analysis (New Feature)

Analyze correlations between multiple cryptocurrencies to identify diversification opportunities.

```python
from tradingagents.crypto_tools import get_crypto_correlation_analysis

# Analyze correlations between major cryptocurrencies
correlation = get_crypto_correlation_analysis("BTC-USD,ETH-USD,SOL-USD,ADA-USD", 30)
print(correlation)
```

**Output Includes:**
- Correlation matrix between all pairs
- Correlation insights and interpretation
- Diversification recommendations
- Period analysis

### 4. Market Overview

Get a comprehensive overview of the entire cryptocurrency market.

```python
from tradingagents.crypto_tools import get_crypto_market_overview

# Get market overview
overview = get_crypto_market_overview()
print(overview)
```

**Output Includes:**
- Total market capitalization
- Market dominance by asset
- Top gainers and losers
- Market sentiment
- Volume analysis

### 5. Technical Analysis

Detailed technical analysis with crypto-specific indicators.

```python
from tradingagents.crypto_tools import get_crypto_technical_analysis

# Technical analysis with multiple indicators
technical = get_crypto_technical_analysis("BTC-USD", "rsi,macd,bollinger_bands")
print(technical)
```

**Supported Indicators:**
- `rsi` - Relative Strength Index
- `macd` - Moving Average Convergence Divergence
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `bollinger_bands` - Bollinger Bands
- `atr` - Average True Range

## Advanced Usage

### Custom Configuration

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create custom config for crypto
config = DEFAULT_CONFIG.copy()
config["data_vendors"] = {
    "core_stock_apis": "crypto",
    "technical_indicators": "crypto",
    "news_data": "crypto"
}

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# Analyze with enhanced crypto data
_, decision = ta.propagate("BTC-USD", "2024-05-10")
```

### Error Handling & Fallbacks

The system automatically handles API rate limits and errors:

```python
from tradingagents.dataflows.crypto_enhanced import get_crypto_data

# System will automatically fallback between APIs
data = get_crypto_data("BTC-USD", "2024-01-01", "2024-01-10")

# Check for errors
if "Error" in data:
    print("Data retrieval failed, check API keys or try later")
else:
    print("Data retrieved successfully")
```

### Batch Processing

```python
from tradingagents.crypto_tools import analyze_crypto_market

# Analyze multiple cryptocurrencies
symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD"]
for symbol in symbols:
    analysis = analyze_crypto_market(symbol, 30)
    print(f"\n=== {symbol} Analysis ===")
    print(analysis[:500] + "...")  # Print first 500 chars
```

## Data Sources & API Priority

### Primary Data Sources
1. **CoinGecko** - Primary source (free tier, good rate limits)
2. **CoinMarketCap** - Premium data (requires API key)
3. **CryptoCompare** - Historical data and social metrics
4. **Yahoo Finance** - Fallback data source

### Automatic Fallback

The system automatically:
- Detects available API keys
- Prioritizes APIs with higher rate limits
- Falls back gracefully when APIs are unavailable
- Handles rate limiting automatically

## Performance & Best Practices

### Rate Limiting
- Built-in rate limiting for all API calls
- Automatic retry with exponential backoff
- Graceful degradation when limits are reached

### Response Times
- Basic data retrieval: < 10 seconds
- Market analysis: < 15 seconds
- Portfolio analysis: < 30 seconds
- Correlation analysis: < 45 seconds

### Best Practices
1. **Use API Keys**: For production use, configure all optional API keys
2. **Cache Results**: Cache analysis results for repeated queries
3. **Batch Requests**: Group related requests together
4. **Monitor Usage**: Keep track of API usage and rate limits

## Troubleshooting

### Common Issues

#### "Error retrieving data"
- Check API keys are correctly set
- Verify internet connection
- Check API service status

#### "Rate limit exceeded"
- Wait before making more requests
- Consider upgrading API tier
- Use fewer symbols in batch requests

#### "Symbol not found"
- Verify symbol format (e.g., BTC-USD, not BTC)
- Check if symbol is in supported list
- Try alternative data source

### Debug Mode

Enable debug mode for detailed logging:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

ta = TradingAgentsGraph(debug=True)
_, decision = ta.propagate("BTC-USD", "2024-05-10")
```

## Examples

### Complete Trading Session

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.crypto_tools import (
    analyze_crypto_market,
    get_crypto_portfolio_analysis
)

# Initialize trading graph
ta = TradingAgentsGraph(debug=True)

# Analyze individual cryptocurrencies
symbols = ["BTC-USD", "ETH-USD", "SOL-USD"]
for symbol in symbols:
    print(f"\n{'='*50}")
    print(f"Analyzing {symbol}")
    print(f"{'='*50}")
    
    # Get market analysis
    analysis = analyze_crypto_market(symbol, 30)
    print(analysis)
    
    # Get trading decision
    _, decision = ta.propagate(symbol, "2024-05-10")
    print(f"\nTrading Decision: {decision}")

# Portfolio analysis
print(f"\n{'='*50}")
print("Portfolio Analysis")
print(f"{'='*50}")
portfolio = get_crypto_portfolio_analysis(",".join(symbols), 90)
print(portfolio)
```

### Correlation Analysis Example

```python
from tradingagents.crypto_tools import get_crypto_correlation_analysis

# Analyze correlations for portfolio diversification
correlation = get_crypto_correlation_analysis(
    "BTC-USD,ETH-USD,SOL-USD,ADA-USD,DOGE-USD", 
    30
)
print(correlation)
```

## Support & Resources

- **Documentation**: Check the main README.md for updates
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join the TradingAgents Discord community
- **API Documentation**: Refer to individual API provider documentation

## Changelog

### v1.0.0 - Initial Crypto Integration
- Multi-API support for crypto data
- Comprehensive market analysis tools
- Portfolio and correlation analysis
- Social sentiment integration
- Enhanced error handling and fallbacks

---

For questions or support, please refer to the main TradingAgents documentation or join our community channels.