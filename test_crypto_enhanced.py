"""
Enhanced Crypto Integration Testing with New Features
Tests all aspects including the new correlation analysis
"""

import os
import sys
import traceback
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.insert(0, '/workspace/TradingAgents-Dual')

def test_new_correlation_analysis():
    """Test the new correlation analysis feature."""
    print("\n" + "="*60)
    print("TEST: CORRELATION ANALYSIS FEATURE")
    print("="*60)
    
    from tradingagents.crypto_tools import get_crypto_correlation_analysis
    
    results = {}
    
    # Test with multiple cryptocurrencies
    print("\n--- Testing correlation analysis with BTC, ETH, SOL ---")
    try:
        correlation_result = get_crypto_correlation_analysis("BTC-USD,ETH-USD,SOL-USD", 30)
        if "Crypto Correlation Analysis" in correlation_result and "Error" not in correlation_result:
            print(f"  ✓ Correlation analysis: SUCCESS")
            print(f"  First 300 chars: {correlation_result[:300]}...")
            results["correlation_analysis"] = "SUCCESS"
        else:
            print(f"  ✗ Correlation analysis: FAILED")
            results["correlation_analysis"] = "FAILED"
    except Exception as e:
        print(f"  ✗ Correlation analysis: ERROR - {str(e)}")
        results["correlation_analysis"] = "ERROR"
    
    # Test with invalid input
    print("\n--- Testing correlation analysis with invalid input ---")
    try:
        result = get_crypto_correlation_analysis("", 30)
        if "Error" in result:
            print(f"  ✓ Invalid input handling: SUCCESS")
            results["invalid_input"] = "SUCCESS"
        else:
            print(f"  ✗ Invalid input handling: FAILED")
            results["invalid_input"] = "FAILED"
    except Exception as e:
        print(f"  ✗ Invalid input handling: ERROR - {str(e)}")
        results["invalid_input"] = "ERROR"
    
    # Test with single symbol (should fail)
    print("\n--- Testing correlation analysis with single symbol ---")
    try:
        result = get_crypto_correlation_analysis("BTC-USD", 30)
        if "Error" in result and "At least 2 symbols" in result:
            print(f"  ✓ Single symbol validation: SUCCESS")
            results["single_symbol"] = "SUCCESS"
        else:
            print(f"  ✗ Single symbol validation: FAILED - {result}")
            results["single_symbol"] = "FAILED"
    except Exception as e:
        print(f"  ✗ Single symbol validation: ERROR - {str(e)}")
        results["single_symbol"] = "ERROR"
    
    return results

def test_enhanced_error_handling():
    """Test the enhanced error handling features."""
    print("\n" + "="*60)
    print("TEST: ENHANCED ERROR HANDLING")
    print("="*60)
    
    from tradingagents.dataflows.crypto_enhanced import get_crypto_data
    from tradingagents.crypto_tools import analyze_crypto_market, get_crypto_portfolio_analysis
    
    results = {}
    
    # Test empty symbol
    print("\n--- Testing empty symbol handling ---")
    try:
        result = get_crypto_data("", "2024-01-01", "2024-01-10")
        if "Error" in result and "required" in result:
            print(f"  ✓ Empty symbol validation: SUCCESS")
            results["empty_symbol"] = "SUCCESS"
        else:
            print(f"  ✗ Empty symbol validation: FAILED")
            results["empty_symbol"] = "FAILED"
    except Exception as e:
        print(f"  ✗ Empty symbol validation: ERROR - {str(e)}")
        results["empty_symbol"] = "ERROR"
    
    # Test invalid days in market analysis
    print("\n--- Testing invalid days in market analysis ---")
    try:
        result = analyze_crypto_market("BTC-USD", -5)
        if "Error" in result and "positive" in result:
            print(f"  ✓ Invalid days validation: SUCCESS")
            results["invalid_days"] = "SUCCESS"
        else:
            print(f"  ✗ Invalid days validation: FAILED")
            results["invalid_days"] = "FAILED"
    except Exception as e:
        print(f"  ✗ Invalid days validation: ERROR - {str(e)}")
        results["invalid_days"] = "ERROR"
    
    # Test empty symbols in portfolio analysis
    print("\n--- Testing empty symbols in portfolio analysis ---")
    try:
        result = get_crypto_portfolio_analysis("", 30)
        if "Error" in result and "required" in result:
            print(f"  ✓ Empty symbols validation: SUCCESS")
            results["empty_symbols"] = "SUCCESS"
        else:
            print(f"  ✗ Empty symbols validation: FAILED")
            results["empty_symbols"] = "FAILED"
    except Exception as e:
        print(f"  ✗ Empty symbols validation: ERROR - {str(e)}")
        results["empty_symbols"] = "ERROR"
    
    return results

def test_data_parsing_robustness():
    """Test the robustness of data parsing."""
    print("\n" + "="*60)
    print("TEST: DATA PARSING ROBUSTNESS")
    print("="*60)
    
    from tradingagents.dataflows.crypto_enhanced import get_crypto_data
    from tradingagents.crypto_tools import analyze_crypto_market
    
    results = {}
    
    # Test various crypto symbols
    test_symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "DOGE-USD", "LTC-USD"]
    
    for symbol in test_symbols:
        print(f"\n--- Testing data parsing for {symbol} ---")
        try:
            # Test basic data retrieval
            data_result = get_crypto_data(symbol, "2024-01-01", "2024-01-10")
            if "Error" not in data_result and "No data found" not in data_result:
                print(f"  ✓ {symbol} data retrieval: SUCCESS")
                
                # Test market analysis
                analysis_result = analyze_crypto_market(symbol, 7)
                # Allow for API rate limiting errors in social sentiment section
                if "Comprehensive Crypto Analysis" in analysis_result and not analysis_result.startswith("Error"):
                    print(f"  ✓ {symbol} market analysis: SUCCESS")
                    results[f"{symbol}_parsing"] = "SUCCESS"
                else:
                    print(f"  ✗ {symbol} market analysis: FAILED - {analysis_result[:100]}")
                    results[f"{symbol}_parsing"] = "FAILED"
            else:
                print(f"  ✗ {symbol} data retrieval: FAILED")
                results[f"{symbol}_parsing"] = "FAILED"
        except Exception as e:
            print(f"  ✗ {symbol} parsing: ERROR - {str(e)}")
            results[f"{symbol}_parsing"] = "ERROR"
    
    return results

def run_enhanced_tests():
    """Run all enhanced tests."""
    print("🚀 STARTING ENHANCED CRYPTO INTEGRATION TESTS")
    print("="*60)
    
    all_results = {}
    
    # Run all test suites
    all_results["correlation"] = test_new_correlation_analysis()
    all_results["error_handling"] = test_enhanced_error_handling()
    all_results["data_parsing"] = test_data_parsing_robustness()
    
    # Summary
    print("\n" + "="*60)
    print("ENHANCED TEST SUMMARY")
    print("="*60)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    error_tests = 0
    
    for category, tests in all_results.items():
        print(f"\n{category.upper()}:")
        for test_name, result in tests.items():
            total_tests += 1
            if result == "SUCCESS":
                passed_tests += 1
                print(f"  ✓ {test_name}: {result}")
            elif result == "FAILED":
                failed_tests += 1
                print(f"  ✗ {test_name}: {result}")
            else:
                error_tests += 1
                print(f"  ⚠ {test_name}: {result}")
    
    print(f"\n" + "="*60)
    print(f"OVERALL RESULTS:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Errors: {error_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print("="*60)
    
    if failed_tests == 0 and error_tests == 0:
        print("🎉 ALL ENHANCED TESTS PASSED! Crypto integration is robust.")
    else:
        print("⚠️ Some tests failed or had errors. Check the details above.")
    
    return all_results

if __name__ == "__main__":
    run_enhanced_tests()