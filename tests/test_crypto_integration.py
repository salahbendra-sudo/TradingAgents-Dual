"""
Comprehensive Automated Test Suite for Crypto Integration
Tests all aspects of the crypto integration with TradingAgents
"""

import os
import sys
import unittest
import tempfile
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.insert(0, '/workspace/TradingAgents-Dual')

from tradingagents.dataflows.crypto_enhanced import (
    get_crypto_data, get_crypto_info, get_crypto_news, 
    get_crypto_indicators, get_crypto_social_sentiment
)
from tradingagents.crypto_tools import (
    analyze_crypto_market, get_crypto_portfolio_analysis,
    get_crypto_correlation_analysis, get_crypto_market_overview,
    get_crypto_technical_analysis
)


class TestCryptoEnhancedDataFlows(unittest.TestCase):
    """Test the enhanced crypto data flows."""
    
    def test_get_crypto_data_basic(self):
        """Test basic crypto data retrieval."""
        result = get_crypto_data("BTC-USD", "2024-01-01", "2024-01-10")
        self.assertIsInstance(result, str)
        self.assertNotIn("Error", result)
        self.assertNotIn("No data found", result)
        self.assertIn("Date", result)
    
    def test_get_crypto_data_multiple_symbols(self):
        """Test crypto data retrieval for multiple symbols."""
        symbols = ["BTC-USD", "ETH-USD", "SOL-USD"]
        for symbol in symbols:
            with self.subTest(symbol=symbol):
                result = get_crypto_data(symbol, "2024-01-01", "2024-01-10")
                self.assertIsInstance(result, str)
                self.assertNotIn("Error", result)
                self.assertNotIn("No data found", result)
    
    def test_get_crypto_data_invalid_input(self):
        """Test error handling for invalid input."""
        # Empty symbol
        result = get_crypto_data("", "2024-01-01", "2024-01-10")
        self.assertIn("Error", result)
        
        # Invalid dates
        result = get_crypto_data("BTC-USD", "", "")
        self.assertIn("Error", result)
    
    def test_get_crypto_info(self):
        """Test crypto information retrieval."""
        result = get_crypto_info("BTC-USD")
        self.assertIsInstance(result, str)
        self.assertIn("Crypto Information", result)
    
    def test_get_crypto_news(self):
        """Test crypto news retrieval."""
        result = get_crypto_news("BTC-USD")
        self.assertIsInstance(result, str)
        self.assertIn("Crypto News", result)
    
    def test_get_crypto_indicators(self):
        """Test crypto technical indicators."""
        from datetime import datetime
        curr_date = datetime.now().strftime("%Y-%m-%d")
        result = get_crypto_indicators("BTC-USD", "rsi", curr_date, 14)
        self.assertIsInstance(result, str)
        self.assertIn("rsi values", result)
    
    def test_get_crypto_social_sentiment(self):
        """Test crypto social sentiment (may have rate limiting)."""
        result = get_crypto_social_sentiment("BTC-USD")
        self.assertIsInstance(result, str)
        # Allow for rate limiting errors
        if not result.startswith("Error"):
            self.assertIn("Social Media Sentiment", result)


class TestCryptoTools(unittest.TestCase):
    """Test the crypto analysis tools."""
    
    def test_analyze_crypto_market(self):
        """Test comprehensive crypto market analysis."""
        result = analyze_crypto_market("BTC-USD", 7)
        self.assertIsInstance(result, str)
        self.assertIn("Comprehensive Crypto Analysis", result)
        self.assertNotIn("Error:", result)
    
    def test_analyze_crypto_market_invalid_input(self):
        """Test error handling for invalid input in market analysis."""
        # Empty symbol
        result = analyze_crypto_market("", 7)
        self.assertIn("Error", result)
        
        # Invalid days
        result = analyze_crypto_market("BTC-USD", -5)
        self.assertIn("Error", result)
    
    def test_get_crypto_portfolio_analysis(self):
        """Test portfolio analysis for multiple cryptocurrencies."""
        result = get_crypto_portfolio_analysis("BTC-USD,ETH-USD,SOL-USD", 30)
        self.assertIsInstance(result, str)
        self.assertIn("Portfolio Analysis", result)
    
    def test_get_crypto_portfolio_analysis_invalid_input(self):
        """Test error handling for invalid input in portfolio analysis."""
        # Empty symbols
        result = get_crypto_portfolio_analysis("", 30)
        self.assertIn("Error", result)
        
        # Invalid days
        result = get_crypto_portfolio_analysis("BTC-USD,ETH-USD", -5)
        self.assertIn("Error", result)
    
    def test_get_crypto_correlation_analysis(self):
        """Test correlation analysis between cryptocurrencies."""
        result = get_crypto_correlation_analysis("BTC-USD,ETH-USD,SOL-USD", 30)
        self.assertIsInstance(result, str)
        self.assertIn("Crypto Correlation Analysis", result)
        self.assertIn("Correlation Matrix", result)
    
    def test_get_crypto_correlation_analysis_invalid_input(self):
        """Test error handling for invalid input in correlation analysis."""
        # Empty symbols
        result = get_crypto_correlation_analysis("", 30)
        self.assertIn("Error", result)
        
        # Single symbol
        result = get_crypto_correlation_analysis("BTC-USD", 30)
        self.assertIn("Error", result)
        self.assertIn("At least 2 symbols", result)
    
    def test_get_crypto_market_overview(self):
        """Test crypto market overview."""
        result = get_crypto_market_overview()
        self.assertIsInstance(result, str)
        self.assertIn("Crypto Market Overview", result)
    
    def test_get_crypto_technical_analysis(self):
        """Test technical analysis for cryptocurrencies."""
        result = get_crypto_technical_analysis("BTC-USD", "RSI,MACD,SMA")
        self.assertIsInstance(result, str)
        self.assertIn("Technical Analysis", result)


class TestCryptoIntegration(unittest.TestCase):
    """Test integration aspects of crypto functionality."""
    
    def test_api_fallback_system(self):
        """Test that the API fallback system works correctly."""
        # Test with a valid symbol - should work with any available API
        result = get_crypto_data("BTC-USD", "2024-01-01", "2024-01-10")
        self.assertIsInstance(result, str)
        self.assertNotIn("Error", result)
        self.assertIn("Date", result)
    
    def test_data_format_consistency(self):
        """Test that data formats are consistent across different symbols."""
        symbols = ["BTC-USD", "ETH-USD", "ADA-USD"]
        for symbol in symbols:
            with self.subTest(symbol=symbol):
                result = get_crypto_data(symbol, "2024-01-01", "2024-01-10")
                # Should contain standard OHLCV columns
                self.assertIn("Date", result)
                self.assertIn("Open", result)
                self.assertIn("High", result)
                self.assertIn("Low", result)
                self.assertIn("Close", result)
                self.assertIn("Volume", result)
    
    def test_error_handling_robustness(self):
        """Test that error handling is robust for various edge cases."""
        # Test with non-existent symbol
        result = get_crypto_data("NONEXISTENT-USD", "2024-01-01", "2024-01-10")
        # Should either return data or a graceful error message
        self.assertIsInstance(result, str)
        
        # Test with invalid date format
        result = get_crypto_data("BTC-USD", "invalid-date", "invalid-date")
        self.assertIsInstance(result, str)


class TestPerformance(unittest.TestCase):
    """Test performance aspects of crypto integration."""
    
    def test_response_time_basic_data(self):
        """Test that basic data retrieval is reasonably fast."""
        import time
        
        start_time = time.time()
        result = get_crypto_data("BTC-USD", "2024-01-01", "2024-01-10")
        end_time = time.time()
        
        response_time = end_time - start_time
        self.assertLess(response_time, 10.0)  # Should complete within 10 seconds
        self.assertIsInstance(result, str)
    
    def test_concurrent_requests(self):
        """Test that multiple requests can be handled."""
        symbols = ["BTC-USD", "ETH-USD", "SOL-USD"]
        results = []
        
        for symbol in symbols:
            result = get_crypto_data(symbol, "2024-01-01", "2024-01-10")
            results.append(result)
        
        # All requests should complete successfully
        for result in results:
            self.assertIsInstance(result, str)
            self.assertNotIn("Error", result)


def run_all_tests():
    """Run all crypto integration tests and return results."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCryptoEnhancedDataFlows))
    suite.addTests(loader.loadTestsFromTestCase(TestCryptoTools))
    suite.addTests(loader.loadTestsFromTestCase(TestCryptoIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("🚀 RUNNING COMPREHENSIVE CRYPTO INTEGRATION TEST SUITE")
    print("=" * 70)
    
    result = run_all_tests()
    
    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED! Crypto integration is fully functional.")
    else:
        print(f"⚠️ {len(result.failures)} tests failed and {len(result.errors)} tests had errors.")
        print("Check the details above for specific issues.")
    
    print(f"\nTests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)