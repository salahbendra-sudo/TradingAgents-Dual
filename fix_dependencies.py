#!/usr/bin/env python
"""
Dependency Fix Script for TradingAgents

This script fixes the common dependency issues that cause:
- ModuleNotFoundError: No module named 'langchain_community'
- Version conflicts with langchain packages
- Missing dependencies for enhanced LLM providers
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"   Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success")
            return True
        else:
            print(f"   ❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🚀 TradingAgents Dependency Fix Script")
    print("=" * 60)
    print("\nThis script will fix the common dependency issues:")
    print("  - langchain_community module not found")
    print("  - Version conflicts with langchain packages")
    print("  - Missing dependencies for enhanced LLM providers")
    
    # Step 1: Uninstall conflicting packages
    print("\n📦 Step 1: Removing conflicting packages")
    
    packages_to_remove = [
        "langchain",
        "langchain-community", 
        "langchain-core",
        "langchain-openai",
        "langchain-anthropic",
        "langchain-google-genai",
        "langchain-ollama",
        "langchain-huggingface"
    ]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall -y {package}", f"Uninstalling {package}")
    
    # Step 2: Install compatible versions using requirements.txt
    print("\n📦 Step 2: Installing compatible versions from requirements.txt")
    run_command("pip install -r requirements.txt", "Installing all dependencies from requirements.txt")
    
    # Step 3: Install specific packages that might need additional handling
    print("\n🤖 Step 3: Installing specific LLM provider dependencies")
    
    specific_packages = [
        "openai",
        "anthropic", 
        "google-generativeai",
        "ollama",
        "huggingface-hub"
    ]
    
    for package in specific_packages:
        run_command(f"pip install {package}", f"Installing {package}")
    
    # Step 4: Install optional dependencies
    print("\n📚 Step 4: Installing optional dependencies")
    
    optional_packages = [
        "sentence-transformers",
        "numpy",
        "scipy", 
        "scikit-learn"
    ]
    
    for package in optional_packages:
        run_command(f"pip install {package}", f"Installing {package}")
    
    # Step 5: Verify installation
    print("\n🧪 Step 5: Verifying installation")
    
    verification_imports = [
        ("langchain_community", "langchain_community"),
        ("langchain_openai", "langchain_openai"),
        ("langchain_anthropic", "langchain_anthropic"),
        ("langchain_google_genai", "langchain_google_genai"),
        ("langchain_community.chat_models", "ChatOllama"),
        ("tradingagents.graph.trading_graph", "TradingAgentsGraph")
    ]
    
    print("\n🔍 Testing imports:")
    for module_name, import_name in verification_imports:
        try:
            if module_name == "tradingagents.graph.trading_graph":
                exec(f"from {module_name} import {import_name}")
            else:
                exec(f"import {module_name}")
            print(f"   ✅ {module_name} - OK")
        except ImportError as e:
            print(f"   ❌ {module_name} - Failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Dependency Fix Complete!")
    print("\n📝 Next Steps:")
    print("   1. Run: python verify_installation.py")
    print("   2. Test: python -m cli.main")
    print("   3. If issues persist, restart your Python environment")
    print("\n🚀 TradingAgents should now work without dependency errors!")

if __name__ == "__main__":
    main()