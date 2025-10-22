# 🔧 TradingAgents Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: `ModuleNotFoundError: No module named 'langchain_community'`

**Problem**: This error occurs when there are version conflicts between langchain packages.

**Solution**:

#### Option A: Quick Fix Script
```bash
# Run the dependency fix script
python fix_dependencies.py
```

#### Option B: Manual Fix
```bash
# 1. Remove conflicting packages
pip uninstall -y langchain langchain-community langchain-core langchain-openai langchain-anthropic langchain-google-genai langchain-ollama langchain-huggingface

# 2. Install compatible versions
pip install langchain-core>=0.3.79,<1.0.0
pip install langchain>=0.3.27,<1.0.0
pip install langchain-community>=0.3.31,<1.0.0
pip install langchain-openai>=0.3.35,<1.0.0
pip install langchain-anthropic>=0.3.22,<1.0.0
pip install langchain-google-genai>=2.1.12,<3.0.0
pip install langchain-ollama>=0.3.10,<1.0.0
pip install langchain-huggingface>=0.3.1,<1.0.0

# 3. Install LLM provider dependencies
pip install openai>=1.0.0,<2.0.0
pip install anthropic>=0.7.0,<1.0.0
pip install google-generativeai>=0.8.5,<1.0.0
pip install ollama>=0.6.0,<1.0.0
pip install huggingface-hub>=0.35.3,<1.0.0
```

#### Option C: Fresh Installation
```bash
# Create a new virtual environment
python -m venv tradingagents_env
source tradingagents_env/bin/activate  # On Windows: tradingagents_env\Scripts\activate

# Install from updated requirements
pip install -r requirements.txt
```

### Issue 2: API Key Errors

**Problem**: Missing or invalid API keys for LLM providers or data vendors.

**Solution**:
1. Copy `.env.example` to `.env`
2. Add your API keys to `.env`
3. Required keys:
   - `OPENAI_API_KEY`
   - `ALPHA_VANTAGE_API_KEY`
4. Optional keys for enhanced features:
   - `COINMARKETCAP_API_KEY` (crypto data)
   - `CRYPTOCOMPARE_API_KEY` (crypto data)
   - `COINGECKO_API_KEY` (crypto data)
   - `OPENROUTER_API_KEY` (OpenRouter)
   - `DEEPSEEK_API_KEY` (DeepSeek)
   - `HUGGINGFACE_API_KEY` (HuggingFace)

### Issue 3: Memory System Errors

**Problem**: Issues with ChromaDB or embedding models.

**Solution**:
```bash
# Install sentence-transformers for local embeddings
pip install sentence-transformers

# Or use OpenAI embeddings (requires API key)
# Set in .env: OPENAI_API_KEY=your_key_here
```

### Issue 4: Crypto Data Not Working

**Problem**: Cryptocurrency data not loading.

**Solution**:
1. Ensure you have at least one crypto API key
2. Test with basic symbols: `BTC-USD`, `ETH-USD`
3. The system will fall back to yfinance if premium APIs fail

### Issue 5: LLM Provider Not Working

**Problem**: Specific LLM provider not responding.

**Solution**:
1. Check API key is set in `.env`
2. Verify provider is available (OpenAI, OpenRouter, etc.)
3. Test with different provider:
   ```python
   from tradingagents.graph.trading_graph import TradingAgentsGraph
   from tradingagents.default_config import DEFAULT_CONFIG
   
   config = DEFAULT_CONFIG.copy()
   config.update({"llm_provider": "openai"})  # or "openrouter", "deepseek", etc.
   ta = TradingAgentsGraph(config=config)
   ```

## Environment Setup

### Recommended Python Version
- Python 3.9, 3.10, or 3.11
- Python 3.12 may have compatibility issues with some packages

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv tradingagents_env

# Activate on Linux/Mac
source tradingagents_env/bin/activate

# Activate on Windows
tradingagents_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Alternative
```bash
# Build and run with Docker
docker build -t tradingagents .
docker run -it tradingagents
```

## Verification Steps

After installation, run these verification steps:

1. **Basic Verification**:
   ```bash
   python verify_installation.py
   ```

2. **CLI Test**:
   ```bash
   python -m cli.main --help
   ```

3. **Import Test**:
   ```python
   from tradingagents.graph.trading_graph import TradingAgentsGraph
   print("✅ Import successful!")
   ```

## Common Error Messages and Solutions

### `ImportError: cannot import name 'X' from 'Y'`
- Usually a version conflict
- Run the dependency fix script

### `APIError: Invalid API key`
- Check your `.env` file
- Verify API key is correct
- Ensure provider service is accessible

### `ConnectionError: Failed to connect`
- Check internet connection
- Verify API endpoints are accessible
- For Ollama: Ensure local server is running

### `MemoryError: Collection already exists`
- Normal behavior - memory system reusing existing collections
- Can be safely ignored

## Getting Help

If you continue to experience issues:

1. Check the [GitHub Issues](https://github.com/salahbendra-sudo/TradingAgents-Dual/issues)
2. Run the verification script: `python verify_installation.py`
3. Check your Python environment: `python --version`
4. Verify all dependencies: `pip list | grep langchain`

## Performance Tips

- Use virtual environments to avoid conflicts
- Set up API keys for better performance
- For local development, use Ollama with local models
- Monitor API usage to avoid rate limits