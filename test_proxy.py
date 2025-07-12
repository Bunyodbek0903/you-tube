#!/usr/bin/env python3
"""
Proxy Test Script
Test proxy functionality with ProxyScrape API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils.logger import Logger
from utils.proxy_manager import ProxyManager, ProxyScrapeManager

def test_proxy_api():
    """Test ProxyScrape API functionality"""
    print("🔍 Testing ProxyScrape API...")
    
    config = Config()
    logger = Logger()
    
    # Test ProxyScrape API directly
    proxy_scraper = ProxyScrapeManager(logger, config)
    
    print("\n📡 Fetching proxies from API...")
    proxies = proxy_scraper.fetch_proxies_from_api(
        proxy_type=config.PROXY_TYPE,
        timeout=config.PROXY_TIMEOUT,
        ssl=config.PROXY_SSL,
        anonymity=config.PROXY_ANONYMITY,
        country=config.PROXY_COUNTRY
    )
    
    if proxies:
        print(f"✅ Successfully fetched {len(proxies)} proxies")
        
        # Test first few proxies
        print("\n🧪 Testing proxies...")
        working_proxies = 0
        for i, proxy in enumerate(proxies[:5]):
            print(f"Testing proxy {i+1}: {proxy['http']}")
            if proxy_scraper.test_proxy(proxy):
                print(f"✅ Proxy {i+1} is working")
                working_proxies += 1
            else:
                print(f"❌ Proxy {i+1} failed")
        
        print(f"\n📊 Results: {working_proxies}/5 proxies working")
        
        # Get statistics
        stats = proxy_scraper.get_proxy_stats()
        print(f"\n📈 Proxy Statistics:")
        print(f"Total proxies: {stats['total_proxies']}")
        print(f"Tested proxies: {stats['tested_proxies']}")
        print(f"Working proxies: {stats['working_proxies']}")
        print(f"Success rate: {stats['success_rate']}")
        
    else:
        print("❌ Failed to fetch proxies from API")
        return False
    
    return True

def test_proxy_manager():
    """Test ProxyManager functionality"""
    print("\n🔧 Testing ProxyManager...")
    
    config = Config()
    logger = Logger()
    
    # Test with API
    print("Testing with API enabled...")
    proxy_manager = ProxyManager(use_api=True, logger=logger, config=config)
    
    proxy = proxy_manager.get_proxy()
    if proxy:
        print(f"✅ Got working proxy: {proxy['http']}")
        
        # Test proxy stats
        stats = proxy_manager.get_proxy_stats()
        print(f"📊 Stats: {stats}")
        
    else:
        print("❌ No working proxy found")
    
    # Test with file fallback
    print("\nTesting with file fallback...")
    proxy_manager_file = ProxyManager(use_api=False, logger=logger, config=config)
    
    proxy = proxy_manager_file.get_proxy()
    if proxy:
        print(f"✅ Got proxy from file: {proxy['http']}")
    else:
        print("❌ No proxy found in file")

def main():
    """Main test function"""
    print("🚀 Starting Proxy Tests...")
    print("=" * 50)
    
    # Test API
    if test_proxy_api():
        print("\n✅ API test passed")
    else:
        print("\n❌ API test failed")
    
    # Test Manager
    test_proxy_manager()
    
    print("\n" + "=" * 50)
    print("🏁 Proxy tests completed!")

if __name__ == "__main__":
    main()