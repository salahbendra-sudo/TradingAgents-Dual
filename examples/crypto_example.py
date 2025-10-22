"""
Crypto Analysis Example for TradingAgents

This example demonstrates how to use TradingAgents for cryptocurrency analysis.
The framework automatically detects crypto symbols and adjusts the analysis accordingly.
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def analyze_crypto(symbol, trade_date):
    """
    Analyze a cryptocurrency using TradingAgents.
    
    Args:
        symbol (str): Crypto symbol (e.g., "BTC-USD", "ETH-USD")
        trade_date (str): Trading date in YYYY-MM-DD format
    """
    print(f"\n{'='*60}")
    print(f"Analyzing {symbol} for {trade_date}")
    print(f"{'='*60}")
    
    # Create configuration
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = "gpt-4o-mini"
    config["quick_think_llm"] = "gpt-4o-mini"
    
    # Initialize trading graph
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Check if symbol is detected as crypto
    is_crypto = ta._is_crypto_symbol(symbol)
    print(f"Symbol type: {'Cryptocurrency' if is_crypto else 'Stock'}")
    
    # Get adjusted analysts
    analysts = ta._get_adjusted_analysts_for_symbol(symbol)
    print(f"Analysts used: {analysts}")
    
    # Run analysis
    try:
        _, decision = ta.propagate(symbol, trade_date)
        print(f"\nDecision: {decision}")
        return decision
    except Exception as e:
        print(f"\nError analyzing {symbol}: {e}")
        return None

if __name__ == "__main__":
    # Example crypto analysis
    crypto_symbols = ["BTC-USD", "ETH-USD", "SOL-USD"]
    trade_date = "2024-05-10"
    
    print("TradingAgents Crypto Analysis Demo")
    print("This demo shows how TradingAgents can analyze cryptocurrencies")
    print("alongside traditional stocks with automatic symbol detection.\n")
    
    # Analyze each cryptocurrency
    for symbol in crypto_symbols:
        analyze_crypto(symbol, trade_date)
    
    # Compare with a stock
    print("\n" + "="*60)
    print("For comparison, here's a stock analysis:")
    print("="*60)
    analyze_crypto("AAPL", trade_date)
    
    print("\n" + "="*60)
    print("Crypto Analysis Complete!")
    print("="*60)
    print("\nKey Features:")
    print("✓ Automatic crypto symbol detection")
    print("✓ Adjusted analyst selection (no fundamentals for crypto)")
    print("✓ Same technical analysis tools as stocks")
    print("✓ Market, social, and news analysis for crypto")