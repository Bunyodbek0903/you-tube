#!/usr/bin/env python3
"""
Proxy Test Script
ProxyScrape API bilan proxy funksionalligini tekshirish
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils.logger import Logger
from utils.proxy_manager import ProxyManager, ProxyScrapeManager

def test_proxy_api():
    """ProxyScrape API funksionalligini tekshirish"""
    print("🔍 ProxyScrape API tekshirilmoqda...")
    
    config = Config()
    logger = Logger()
    
    # ProxyScrape API ni to'g'ridan-to'g'ri tekshirish
    proxy_scraper = ProxyScrapeManager(logger, config)
    
    print("\n📡 API dan proxylar olinmoqda...")
    proxies = proxy_scraper.fetch_proxies_from_api(
        proxy_type=config.PROXY_TYPE,
        timeout=config.PROXY_TIMEOUT,
        ssl=config.PROXY_SSL,
        anonymity=config.PROXY_ANONYMITY,
        country=config.PROXY_COUNTRY
    )
    
    if proxies:
        print(f"✅ {len(proxies)} ta proxy muvaffaqiyatli olindi")
        
        # Birinchi bir nechta proxyni tekshirish
        print("\n🧪 Proxylar tekshirilmoqda...")
        working_proxies = 0
        for i, proxy in enumerate(proxies[:5]):
            print(f"Proxy {i+1} tekshirilmoqda: {proxy['http']}")
            if proxy_scraper.test_proxy(proxy):
                print(f"✅ Proxy {i+1} ishlayapti")
                working_proxies += 1
            else:
                print(f"❌ Proxy {i+1} ishlamayapti")
        
        print(f"\n📊 Natijalar: {working_proxies}/5 ta proxy ishlayapti")
        
        # Statistikani olish
        stats = proxy_scraper.get_proxy_stats()
        print(f"\n📈 Proxy statistikasi:")
        print(f"Jami proxylar: {stats['total_proxies']}")
        print(f"Tekshirilgan proxylar: {stats['tested_proxies']}")
        print(f"Ishlayotgan proxylar: {stats['working_proxies']}")
        print(f"Muvaffaqiyat darajasi: {stats['success_rate']}")
        
    else:
        print("❌ API dan proxylar olish amalga oshmadi")
        return False
    
    return True

def test_proxy_manager():
    """ProxyManager funksionalligini tekshirish"""
    print("\n🔧 ProxyManager tekshirilmoqda...")
    
    config = Config()
    logger = Logger()
    
    # API bilan tekshirish
    print("API yoqilgan holda tekshirilmoqda...")
    proxy_manager = ProxyManager(use_api=True, logger=logger, config=config)
    
    proxy = proxy_manager.get_proxy()
    if proxy:
        print(f"✅ Ishlayotgan proxy olindi: {proxy['http']}")
        
        # Proxy statistikasini tekshirish
        stats = proxy_manager.get_proxy_stats()
        print(f"📊 Statistikalar: {stats}")
        
    else:
        print("❌ Ishlayotgan proxy topilmadi")
    
    # Fayl fallback bilan tekshirish
    print("\nFayl fallback bilan tekshirilmoqda...")
    proxy_manager_file = ProxyManager(use_api=False, logger=logger, config=config)
    
    proxy = proxy_manager_file.get_proxy()
    if proxy:
        print(f"✅ Fayldan proxy olindi: {proxy['http']}")
    else:
        print("❌ Faylda proxy topilmadi")

def main():
    """Asosiy test funksiyasi"""
    print("🚀 Proxy testlari boshlanmoqda...")
    print("=" * 50)
    
    # API ni tekshirish
    if test_proxy_api():
        print("\n✅ API testi o'tdi")
    else:
        print("\n❌ API testi o'tmadi")
    
    # Manager ni tekshirish
    test_proxy_manager()
    
    print("\n" + "=" * 50)
    print("🏁 Proxy testlari tugallandi!")

if __name__ == "__main__":
    main()