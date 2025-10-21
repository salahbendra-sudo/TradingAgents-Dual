# Enhanced LLM Provider Support Guide

## Overview

TradingAgents now supports multiple LLM providers beyond OpenAI, including OpenRouter, DeepSeek, Ollama, and HuggingFace models. This guide covers how to configure and use these providers.

## Supported Providers

### 1. OpenAI (Default)
- **Provider**: `openai`
- **Models**: GPT-4o, GPT-4o-mini, o4-mini, etc.
- **API**: Standard OpenAI API

### 2. OpenRouter
- **Provider**: `openrouter`
- **Models**: Access to 100+ models from Anthropic, Google, Meta, Mistral, etc.
- **API**: OpenAI-compatible API
- **Cost**: Pay-per-use with unified billing

### 3. DeepSeek
- **Provider**: `deepseek`
- **Models**: DeepSeek Chat, DeepSeek Coder
- **API**: OpenAI-compatible API
- **Features**: Free tier available, strong reasoning capabilities

### 4. Ollama (Local)
- **Provider**: `ollama`
- **Models**: Llama, Mistral, Gemma, and other local models
- **API**: Local server
- **Features**: Completely offline, privacy-focused

### 5. HuggingFace
- **Provider**: `huggingface`
- **Models**: Any model from HuggingFace Hub
- **API**: Inference API or local models
- **Features**: Open-source models, customizable

## Configuration

### Environment Variables

```bash
# Required for OpenAI
OPENAI_API_KEY=your_openai_api_key

# Optional for other providers
OPENROUTER_API_KEY=your_openrouter_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### Configuration Dictionary

```python
from tradingagents.default_config import DEFAULT_CONFIG

# Example configurations for different providers

# OpenAI (Default)
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",
    "quick_think_llm": "gpt-4o-mini",
    "backend_url": "https://api.openai.com/v1",
    "openai_api_key": "your_openai_api_key"  # Optional if set in env
})

# OpenRouter
config.update({
    "llm_provider": "openrouter",
    "deep_think_llm": "anthropic/claude-3.5-sonnet",
    "quick_think_llm": "google/gemini-flash-1.5",
    "openrouter_api_key": "your_openrouter_api_key"
})

# DeepSeek
config.update({
    "llm_provider": "deepseek",
    "deep_think_llm": "deepseek-chat",
    "quick_think_llm": "deepseek-chat",
    "deepseek_api_key": "your_deepseek_api_key"
})

# Ollama (Local)
config.update({
    "llm_provider": "ollama",
    "deep_think_llm": "llama3.1:8b",
    "quick_think_llm": "llama3.1:8b",
    "backend_url": "http://localhost:11434"
})

# HuggingFace (Local)
config.update({
    "llm_provider": "huggingface",
    "deep_think_llm": "microsoft/DialoGPT-medium",
    "quick_think_llm": "microsoft/DialoGPT-medium",
    "local_embeddings": True,
    "embedding_model": "all-MiniLM-L6-v2"
})

# HuggingFace (API)
config.update({
    "llm_provider": "huggingface",
    "deep_think_llm": "microsoft/DialoGPT-medium",
    "quick_think_llm": "microsoft/DialoGPT-medium",
    "backend_url": "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
    "huggingface_api_key": "your_huggingface_api_key"
})
```

## Usage Examples

### Basic Usage with Different Providers

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure for OpenRouter
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "openrouter",
    "deep_think_llm": "anthropic/claude-3.5-sonnet",
    "quick_think_llm": "google/gemini-flash-1.5",
    "openrouter_api_key": "your_openrouter_api_key"
})

# Initialize TradingAgents
ta = TradingAgentsGraph(config=config)

# Use as normal
_, decision = ta.propagate("AAPL", "2024-05-10")
print(f"Trading Decision: {decision}")
```

### Local Ollama Setup

1. **Install Ollama**:
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download from https://ollama.ai/download
   ```

2. **Pull Models**:
   ```bash
   ollama pull llama3.1:8b
   ollama pull nomic-embed-text  # For embeddings
   ```

3. **Configure TradingAgents**:
   ```python
   config = DEFAULT_CONFIG.copy()
   config.update({
       "llm_provider": "ollama",
       "deep_think_llm": "llama3.1:8b",
       "quick_think_llm": "llama3.1:8b",
       "backend_url": "http://localhost:11434"
   })
   
   ta = TradingAgentsGraph(config=config)
   ```

### Local HuggingFace Models

```python
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "huggingface",
    "deep_think_llm": "microsoft/DialoGPT-medium",
    "quick_think_llm": "microsoft/DialoGPT-medium",
    "local_embeddings": True,
    "embedding_model": "all-MiniLM-L6-v2"
})

ta = TradingAgentsGraph(config=config)
```

## Embedding Models

### Supported Embedding Options

1. **OpenAI Embeddings** (Default)
   - Model: `text-embedding-3-small`
   - Provider: OpenAI API

2. **Ollama Embeddings**
   - Model: `nomic-embed-text`
   - Provider: Local Ollama server

3. **Local HuggingFace Embeddings**
   - Model: `all-MiniLM-L6-v2` (default) or any SentenceTransformer model
   - Provider: Local installation

### Embedding Configuration

```python
# Enable local embeddings with HuggingFace
config.update({
    "local_embeddings": True,
    "embedding_model": "all-MiniLM-L6-v2"  # or "multi-qa-mpnet-base-dot-v1", etc.
})

# Use Ollama embeddings
config.update({
    "llm_provider": "ollama",
    "backend_url": "http://localhost:11434"
})
```

## API Key Sources

### OpenRouter
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up and get API key
3. Models: `anthropic/claude-3.5-sonnet`, `google/gemini-flash-1.5`, `meta-llama/llama-3.1-8b-instruct`, etc.

### DeepSeek
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Sign up and get API key
3. Models: `deepseek-chat`, `deepseek-coder`

### HuggingFace
1. Visit [HuggingFace](https://huggingface.co/settings/tokens)
2. Create access token
3. Use for Inference API or local models

## Performance Considerations

### Response Times
- **OpenAI/OpenRouter/DeepSeek**: Fastest (API-based)
- **Ollama**: Medium (local server)
- **HuggingFace Local**: Slowest (model loading + inference)

### Cost Comparison
- **OpenAI**: Pay-per-token
- **OpenRouter**: Unified billing across providers
- **DeepSeek**: Free tier available
- **Ollama/HuggingFace Local**: Free (compute cost only)

### Memory Usage
- **API Providers**: Minimal local memory
- **Ollama**: Moderate (model loaded in RAM)
- **HuggingFace Local**: High (model + embeddings in RAM)

## Troubleshooting

### Common Issues

#### "API key not provided"
- Ensure API key is set in environment or config
- Check provider-specific API key requirements

#### "Model not found"
- Verify model name spelling
- Check if model is available for your provider
- For OpenRouter, use full model path (e.g., `anthropic/claude-3.5-sonnet`)

#### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check if models are downloaded: `ollama list`
- Verify backend URL: `http://localhost:11434`

#### Local Embedding Issues
- Install required packages: `pip install sentence-transformers torch`
- Check available disk space for model downloads
- Verify model name in HuggingFace Hub

### Debug Mode

Enable debug mode for detailed logging:

```python
ta = TradingAgentsGraph(debug=True, config=config)
```

## Best Practices

1. **Start with OpenAI**: Use OpenAI for initial testing and development
2. **Cost Optimization**: Use OpenRouter for access to multiple providers with unified billing
3. **Privacy**: Use Ollama for sensitive data and offline operation
4. **Customization**: Use HuggingFace for specific model requirements
5. **Performance**: Test different providers for your specific use case

## Model Recommendations

### For Trading Analysis
- **Best Overall**: `gpt-4o-mini` (OpenAI) or `anthropic/claude-3.5-sonnet` (OpenRouter)
- **Cost-Effective**: `deepseek-chat` (DeepSeek)
- **Local**: `llama3.1:8b` (Ollama)

### For Embeddings
- **Performance**: `text-embedding-3-small` (OpenAI)
- **Local**: `nomic-embed-text` (Ollama) or `all-MiniLM-L6-v2` (HuggingFace)

## Migration Guide

### From OpenAI to Other Providers

1. **Update Provider**: Change `llm_provider` to desired provider
2. **Update Models**: Use provider-specific model names
3. **Set API Key**: Configure provider-specific API key
4. **Test**: Run basic analysis to verify functionality

### Example Migration

```python
# Before (OpenAI)
config = {
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",
    "quick_think_llm": "gpt-4o-mini"
}

# After (OpenRouter)
config = {
    "llm_provider": "openrouter",
    "deep_think_llm": "anthropic/claude-3.5-sonnet",
    "quick_think_llm": "google/gemini-flash-1.5",
    "openrouter_api_key": "your_key"
}
```

## Support

For issues with specific providers:
- **OpenAI**: [OpenAI Documentation](https://platform.openai.com/docs)
- **OpenRouter**: [OpenRouter Documentation](https://openrouter.ai/docs)
- **DeepSeek**: [DeepSeek Documentation](https://platform.deepseek.com/api-docs/)
- **Ollama**: [Ollama Documentation](https://github.com/ollama/ollama)
- **HuggingFace**: [HuggingFace Documentation](https://huggingface.co/docs)

---

This enhanced LLM provider support gives you flexibility to choose the best model provider for your trading analysis needs, whether you prioritize cost, performance, privacy, or specific model capabilities.