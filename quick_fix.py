#!/usr/bin/env python
"""
Quick Fix for TradingAgents Dependency Issues

This script provides a simple solution for the common error:
ModuleNotFoundError: No module named 'langchain_community'
"""

import subprocess
import sys

def run_command(cmd):
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def main():
    print("🔧 TradingAgents Quick Fix")
    print("=" * 50)
    print("\nThis will fix: ModuleNotFoundError: No module named 'langchain_community'")
    
    # Step 1: Install the specific missing package
    print("\n📦 Step 1: Installing langchain-community")
    if run_command("pip install langchain-community==0.3.31"):
        print("   ✅ langchain-community installed successfully")
    else:
        print("   ❌ Failed to install langchain-community")
    
    # Step 2: Install other core langchain packages
    print("\n📦 Step 2: Installing core langchain packages")
    
    core_packages = [
        "langchain-core==0.3.79",
        "langchain==0.3.27",
        "langchain-openai==0.3.35",
        "langchain-anthropic==0.3.22",
        "langchain-google-genai==2.1.12",
        "langchain-ollama==0.3.10",
        "langchain-huggingface==0.3.1"
    ]
    
    for package in core_packages:
        if run_command(f"pip install {package}"):
            print(f"   ✅ {package} installed")
        else:
            print(f"   ❌ Failed to install {package}")
    
    # Step 3: Test the import
    print("\n🧪 Step 3: Testing imports")
    
    try:
        import langchain_community
        print("   ✅ langchain_community import successful")
    except ImportError as e:
        print(f"   ❌ langchain_community import failed: {e}")
    
    try:
        from langchain_community.chat_models import ChatOllama
        print("   ✅ ChatOllama import successful")
    except ImportError as e:
        print(f"   ❌ ChatOllama import failed: {e}")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        print("   ✅ TradingAgentsGraph import successful")
    except ImportError as e:
        print(f"   ❌ TradingAgentsGraph import failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Quick Fix Complete!")
    print("\n📝 Next Steps:")
    print("   1. Try running: python -m cli.main")
    print("   2. If issues persist, run: python verify_installation.py")
    print("   3. For comprehensive fix, run: python fix_dependencies.py")

if __name__ == "__main__":
    main()