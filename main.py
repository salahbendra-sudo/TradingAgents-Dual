from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"  # Use a different model
config["quick_think_llm"] = "gpt-4o-mini"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds

# Configure data vendors (default uses yfinance and alpha_vantage)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # Options: yfinance, alpha_vantage, local, crypto
    "technical_indicators": "yfinance",      # Options: yfinance, alpha_vantage, local, crypto
    "fundamental_data": "alpha_vantage",     # Options: openai, alpha_vantage, local
    "news_data": "alpha_vantage",            # Options: openai, alpha_vantage, google, local, crypto
}

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

print("=== Stock Analysis Example ===")
# forward propagate for stock
_, decision = ta.propagate("NVDA", "2024-05-10")
print(f"Stock Decision: {decision}")

print("\n=== Crypto Analysis Example ===")
# forward propagate for crypto (automatically adjusts analysts)
_, crypto_decision = ta.propagate("BTC-USD", "2024-05-10")
print(f"Crypto Decision: {crypto_decision}")

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
