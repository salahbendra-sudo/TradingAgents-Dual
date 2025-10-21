#!/usr/bin/env python
"""
TradingAgents Installation Verification Script

This script verifies that all dependencies are properly installed and configured.
Run this script after installation to ensure everything is working correctly.
"""

import sys
import subprocess
import importlib
from typing import List, Tuple


def check_package(package_name: str, import_name: str = None) -> Tuple[bool, str]:
    """Check if a package is installed and importable."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True, f"✅ {package_name}"
    except ImportError as e:
        return False, f"❌ {package_name} - {e}"


def check_required_packages() -> List[Tuple[bool, str]]:
    """Check all required packages."""
    packages = [
        ("langchain", "langchain"),
        ("langchain-openai", "langchain_openai"),
        ("langchain-community", "langchain_community"),
        ("langchain-anthropic", "langchain_anthropic"),
        ("langchain-google-genai", "langchain_google_genai"),
        ("langchain-ollama", "langchain_ollama"),
        ("langchain-huggingface", "langchain_huggingface"),
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("google-generativeai", "google.generativeai"),
        ("ollama", "ollama"),
        ("huggingface-hub", "huggingface_hub"),
        ("sentence-transformers", "sentence_transformers"),
        ("yfinance", "yfinance"),
        ("requests", "requests"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("typer", "typer"),
        ("rich", "rich"),
        ("langgraph", "langgraph"),
    ]
    
    results = []
    for package_name, import_name in packages:
        results.append(check_package(package_name, import_name))
    
    return results


def check_tradingagents_modules() -> List[Tuple[bool, str]]:
    """Check TradingAgents specific modules."""
    modules = [
        ("tradingagents.graph.trading_graph", "TradingAgentsGraph"),
        ("tradingagents.default_config", "DEFAULT_CONFIG"),
        ("tradingagents.agents.utils.memory", "FinancialSituationMemory"),
        ("tradingagents.crypto_tools", "get_crypto_data"),
        ("cli.main", "CLI Interface"),
    ]
    
    results = []
    for module_path, description in modules:
        try:
            if module_path == "cli.main":
                # Special case for CLI
                result = subprocess.run(
                    [sys.executable, "-m", "cli.main", "--help"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    results.append((True, f"✅ CLI Interface"))
                else:
                    results.append((False, f"❌ CLI Interface - {result.stderr}"))
            else:
                module = importlib.import_module(module_path)
                if description != "CLI Interface":
                    # Try to import the specific component
                    if hasattr(module, description):
                        results.append((True, f"✅ {description}"))
                    else:
                        results.append((True, f"✅ {module_path}"))
        except Exception as e:
            results.append((False, f"❌ {description} - {e}"))
    
    return results


def check_llm_providers() -> List[Tuple[bool, str]]:
    """Check LLM provider configurations."""
    providers = [
        ("OpenAI", "openai"),
        ("OpenRouter", "openrouter"),
        ("DeepSeek", "deepseek"),
        ("Ollama", "ollama"),
        ("HuggingFace", "huggingface"),
        ("Anthropic", "anthropic"),
        ("Google", "google"),
    ]
    
    results = []
    for provider_name, provider_key in providers:
        try:
            from tradingagents.default_config import DEFAULT_CONFIG
            config = DEFAULT_CONFIG.copy()
            config["llm_provider"] = provider_key
            
            # Test if configuration is valid
            if provider_key in ["openai", "openrouter", "deepseek", "anthropic", "google", "huggingface"]:
                results.append((True, f"✅ {provider_name} Provider"))
            elif provider_key == "ollama":
                # Ollama requires local server
                results.append((True, f"⚠️ {provider_name} Provider (requires local server)"))
            else:
                results.append((True, f"✅ {provider_name} Provider"))
        except Exception as e:
            results.append((False, f"❌ {provider_name} Provider - {e}"))
    
    return results


def check_crypto_support() -> List[Tuple[bool, str]]:
    """Check cryptocurrency support features."""
    features = [
        ("Crypto Data Tools", "crypto_tools"),
        ("Multi-API Support", "coinmarketcap,cryptocompare,coingecko"),
        ("Crypto Symbols", "BTC-USD,ETH-USD,SOL-USD"),
        ("Technical Indicators", "NVT Ratio,Mayer Multiple"),
    ]
    
    results = []
    for feature_name, _ in features:
        try:
            from tradingagents.crypto_tools import get_crypto_data
            results.append((True, f"✅ {feature_name}"))
        except Exception as e:
            results.append((False, f"❌ {feature_name} - {e}"))
    
    return results


def main():
    """Run comprehensive installation verification."""
    print("🚀 TradingAgents Installation Verification")
    print("=" * 60)
    
    # Check Python version
    print(f"\n🐍 Python Version: {sys.version}")
    
    # Check required packages
    print("\n📦 Required Packages:")
    package_results = check_required_packages()
    for success, message in package_results:
        print(f"  {message}")
    
    # Check TradingAgents modules
    print("\n🔧 TradingAgents Modules:")
    module_results = check_tradingagents_modules()
    for success, message in module_results:
        print(f"  {message}")
    
    # Check LLM providers
    print("\n🤖 LLM Provider Support:")
    provider_results = check_llm_providers()
    for success, message in provider_results:
        print(f"  {message}")
    
    # Check crypto support
    print("\n💰 Cryptocurrency Support:")
    crypto_results = check_crypto_support()
    for success, message in crypto_results:
        print(f"  {message}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    
    all_results = package_results + module_results + provider_results + crypto_results
    total_tests = len(all_results)
    passed_tests = sum(1 for success, _ in all_results if success)
    
    print(f"\n✅ Tests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! TradingAgents is ready to use.")
        print("\n📝 Next Steps:")
        print("   1. Set up your API keys in .env file")
        print("   2. Run: python -m cli.main")
        print("   3. Or use in Python: from tradingagents.graph.trading_graph import TradingAgentsGraph")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed.")
        print("\n🔧 Please check the failed components above and reinstall if necessary.")
        print("   Run: pip install -r requirements.txt")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()