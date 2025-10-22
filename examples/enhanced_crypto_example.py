"""
Enhanced Crypto Integration Example
Demonstrates the comprehensive cryptocurrency analysis capabilities in TradingAgents.
"""

import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.crypto_tools import (
    analyze_crypto_market,
    get_crypto_portfolio_analysis,
    get_crypto_market_overview,
    get_crypto_technical_analysis
)
from tradingagents.dataflows.crypto_enhanced import (
    get_crypto_data,
    get_crypto_info,
    get_crypto_news,
    get_crypto_social_sentiment
)

def main():
    """Demonstrate enhanced crypto integration features."""
    
    print("=" * 60)
    print("ENHANCED CRYPTO INTEGRATION DEMONSTRATION")
    print("=" * 60)
    
    # Check for API keys
    print("\n1. API Key Status:")
    api_keys = {
        "COINMARKETCAP_API_KEY": os.getenv("COINMARKETCAP_API_KEY"),
        "CRYPTOCOMPARE_API_KEY": os.getenv("CRYPTOCOMPARE_API_KEY"),
        "COINGECKO_API_KEY": os.getenv("COINGECKO_API_KEY")
    }
    
    for key_name, key_value in api_keys.items():
        status = "✓ SET" if key_value else "✗ NOT SET (using free tier)"
        print(f"   {key_name}: {status}")
    
    # 1. Comprehensive Crypto Market Analysis
    print("\n2. Comprehensive Crypto Market Analysis:")
    print("-" * 40)
    
    try:
        btc_analysis = analyze_crypto_market("BTC-USD", 30)
        print("✓ Bitcoin Analysis Generated")
        # Print first few lines
        lines = btc_analysis.split('\n')[:15]
        for line in lines:
            print(f"   {line}")
        print("   ... (analysis continues)")
    except Exception as e:
        print(f"✗ Bitcoin analysis failed: {e}")
    
    # 2. Portfolio Analysis
    print("\n3. Multi-Crypto Portfolio Analysis:")
    print("-" * 40)
    
    try:
        portfolio = get_crypto_portfolio_analysis("BTC-USD,ETH-USD,SOL-USD", 90)
        print("✓ Portfolio Analysis Generated")
        # Print first few lines
        lines = portfolio.split('\n')[:12]
        for line in lines:
            print(f"   {line}")
        print("   ... (analysis continues)")
    except Exception as e:
        print(f"✗ Portfolio analysis failed: {e}")
    
    # 3. Market Overview
    print("\n4. Crypto Market Overview:")
    print("-" * 40)
    
    try:
        overview = get_crypto_market_overview()
        print("✓ Market Overview Generated")
        # Print first few lines
        lines = overview.split('\n')[:10]
        for line in lines:
            print(f"   {line}")
        print("   ... (overview continues)")
    except Exception as e:
        print(f"✗ Market overview failed: {e}")
    
    # 4. Technical Analysis with Crypto-Specific Indicators
    print("\n5. Technical Analysis with Crypto-Specific Indicators:")
    print("-" * 40)
    
    try:
        technical = get_crypto_technical_analysis("BTC-USD", "rsi,macd,nvt_ratio")
        print("✓ Technical Analysis Generated")
        # Print first few lines
        lines = technical.split('\n')[:20]
        for line in lines:
            print(f"   {line}")
        print("   ... (technical analysis continues)")
    except Exception as e:
        print(f"✗ Technical analysis failed: {e}")
    
    # 5. Individual Crypto Data Functions
    print("\n6. Individual Crypto Data Functions:")
    print("-" * 40)
    
    # Crypto Data
    try:
        data = get_crypto_data("ETH-USD", "2024-01-01", "2024-01-10")
        print("✓ Ethereum Data Retrieved")
        lines = data.split('\n')[:8]
        for line in lines:
            print(f"   {line}")
        print("   ... (data continues)")
    except Exception as e:
        print(f"✗ Ethereum data failed: {e}")
    
    # Crypto Info
    try:
        info = get_crypto_info("SOL-USD")
        print("\n✓ Solana Info Retrieved")
        lines = info.split('\n')[:10]
        for line in lines:
            print(f"   {line}")
        print("   ... (info continues)")
    except Exception as e:
        print(f"✗ Solana info failed: {e}")
    
    # Social Sentiment
    try:
        sentiment = get_crypto_social_sentiment("ADA-USD")
        print("\n✓ Cardano Social Sentiment Retrieved")
        lines = sentiment.split('\n')[:8]
        for line in lines:
            print(f"   {line}")
        print("   ... (sentiment continues)")
    except Exception as e:
        print(f"✗ Cardano sentiment failed: {e}")
    
    # 6. Trading Graph Integration
    print("\n7. Trading Graph Integration:")
    print("-" * 40)
    
    try:
        # Initialize trading graph
        ta = TradingAgentsGraph(debug=False)
        
        # Analyze Bitcoin
        print("Analyzing Bitcoin with Trading Graph...")
        _, btc_decision = ta.propagate("BTC-USD", "2024-05-10")
        print(f"✓ Bitcoin Trading Decision: {btc_decision}")
        
        # Analyze Ethereum
        print("Analyzing Ethereum with Trading Graph...")
        _, eth_decision = ta.propagate("ETH-USD", "2024-05-10")
        print(f"✓ Ethereum Trading Decision: {eth_decision}")
        
    except Exception as e:
        print(f"✗ Trading graph analysis failed: {e}")
    
    print("\n" + "=" * 60)
    print("ENHANCED CRYPTO INTEGRATION DEMONSTRATION COMPLETE")
    print("=" * 60)
    
    print("\n📈 Key Features Demonstrated:")
    print("  • Multi-API crypto data integration")
    print("  • Real-time market analysis")
    print("  • Portfolio construction tools")
    print("  • Crypto-specific technical indicators")
    print("  • Social sentiment analysis")
    print("  • Seamless integration with Trading Graph")
    print("  • Graceful fallback between data sources")
    
    print("\n🔧 To enable premium features:")
    print("  • Set COINMARKETCAP_API_KEY for premium data")
    print("  • Set CRYPTOCOMPARE_API_KEY for enhanced metrics")
    print("  • Set COINGECKO_API_KEY for higher rate limits")

if __name__ == "__main__":
    main()