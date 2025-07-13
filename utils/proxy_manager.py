import requests
import random
import time
from typing import List, Dict, Optional
from utils.logger import Logger

class ProxyScrapeManager:
    def __init__(self, logger: Logger = None, config=None):
        self.logger = logger or Logger()
        self.config = config
        self.base_url = "https://api.proxyscrape.com/v2"
        self.proxy_cache = []
        self.last_fetch_time = 0
        self.cache_duration = getattr(config, 'PROXY_CACHE_DURATION', 300) if config else 300
        
    def fetch_proxies_from_api(self, proxy_type: str = None, timeout: int = None, 
                              ssl: str = None, anonymity: str = None, 
                              country: str = None) -> List[Dict[str, str]]:
        """
        ProxyScrape API dan proxylarni olish
        
        Args:
            proxy_type: http, https, socks4, socks5
            timeout: millisekundlarda timeout
            ssl: yes, no, all
            anonymity: elite, anonymous, transparent, all
            country: mamlakat kodi yoki 'all'
        """
        # Konfiguratsiya qiymatlarini ishlatish
        if self.config:
            proxy_type = proxy_type or getattr(self.config, 'PROXY_TYPE', 'http')
            timeout = timeout or getattr(self.config, 'PROXY_TIMEOUT', 10000)
            ssl = ssl or getattr(self.config, 'PROXY_SSL', 'all')
            anonymity = anonymity or getattr(self.config, 'PROXY_ANONYMITY', 'all')
            country = country or getattr(self.config, 'PROXY_COUNTRY', 'all')
        else:
            proxy_type = proxy_type or "http"
            timeout = timeout or 10000
            ssl = ssl or "all"
            anonymity = anonymity or "all"
            country = country or "all"
        
        try:
            url = f"{self.base_url}/?request=get&proxy_type={proxy_type}&timeout={timeout}&ssl={ssl}&anonymity={anonymity}&country={country}"
            
            self.logger.info(f"ProxyScrape API dan proxylar olinmoqda...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                proxies = []
                proxy_lines = response.text.strip().split('\n')
                
                for line in proxy_lines:
                    if ':' in line:
                        parts = line.strip().split(':')
                        if len(parts) >= 2:
                            ip = parts[0]
                            port = parts[1]
                            
                            # Autentifikatsiya mavjud bo'lsa
                            if len(parts) >= 4:
                                username = parts[2]
                                password = parts[3]
                                proxy_dict = {
                                    'http': f'http://{username}:{password}@{ip}:{port}',
                                    'https': f'http://{username}:{password}@{ip}:{port}'
                                }
                            else:
                                proxy_dict = {
                                    'http': f'http://{ip}:{port}',
                                    'https': f'http://{ip}:{port}'
                                }
                            
                            proxies.append(proxy_dict)
                
                self.logger.success(f"API dan {len(proxies)} ta proxy olindi")
                return proxies
            else:
                self.logger.error(f"Proxylar olishda xato: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"API dan proxylar olishda xato: {e}")
            return []
    
    def get_proxies_with_cache(self, force_refresh: bool = False) -> List[Dict[str, str]]:
        """Cache mexanizmi bilan proxylarni olish"""
        current_time = time.time()
        
        # Cache haqiqatini tekshirish
        if (not force_refresh and 
            self.proxy_cache and 
            current_time - self.last_fetch_time < self.cache_duration):
            self.logger.info(f"Cache proxylar ishlatilmoqda ({len(self.proxy_cache)} ta mavjud)")
            return self.proxy_cache
        
        # Yangi proxylarni olish
        self.proxy_cache = self.fetch_proxies_from_api()
        self.last_fetch_time = current_time
        
        return self.proxy_cache
    
    def get_random_proxy(self, force_refresh: bool = False) -> Optional[Dict[str, str]]:
        """Ishlayotgan tasodifiy proxy olish"""
        proxies = self.get_proxies_with_cache(force_refresh)
        
        if not proxies:
            self.logger.warning("Hech qanday proxy mavjud emas")
            return None
        
        # 5 ta tasodifiy proxyni sinab ko'rish
        tested_proxies = []
        for _ in range(min(5, len(proxies))):
            proxy = random.choice(proxies)
            if proxy not in tested_proxies:
                tested_proxies.append(proxy)
                
                if self.test_proxy(proxy):
                    self.logger.success(f"Ishlayotgan proxy topildi: {proxy['http']}")
                    return proxy
                else:
                    self.logger.warning(f"Proxy ishlamayapti: {proxy['http']}")
        
        self.logger.error("Ishlayotgan proxy topilmadi")
        return None
    
    def test_proxy(self, proxy: Dict[str, str]) -> bool:
        """Proxy ishlayotganini tekshirish"""
        try:
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxy,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            return False
    
    def get_proxy_stats(self) -> Dict[str, any]:
        """Proxy statistikalarini olish"""
        proxies = self.get_proxies_with_cache()
        working_count = 0
        
        for proxy in proxies[:10]:  # Birinchi 10 ta proxyni sinab ko'rish
            if self.test_proxy(proxy):
                working_count += 1
        
        return {
            'total_proxies': len(proxies),
            'tested_proxies': min(10, len(proxies)),
            'working_proxies': working_count,
            'success_rate': f"{(working_count / max(min(10, len(proxies)), 1)) * 100:.1f}%"
        }

class ProxyManager:
    def __init__(self, use_api: bool = True, proxy_file: str = "proxies.txt", logger: Logger = None, config=None):
        self.use_api = use_api
        self.proxy_file = proxy_file
        self.logger = logger or Logger()
        self.config = config
        
        if use_api:
            self.proxy_scraper = ProxyScrapeManager(logger, config)
        else:
            self.proxy_scraper = None
    
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """Ishlayotgan proxy olish"""
        if self.use_api:
            return self.proxy_scraper.get_random_proxy()
        else:
            return self._get_proxy_from_file()
    
    def _get_proxy_from_file(self) -> Optional[Dict[str, str]]:
        """Mahalliy fayldan proxy olish (fallback usul)"""
        try:
            with open(self.proxy_file, 'r') as f:
                proxy_lines = [line.strip() for line in f if line.strip()]
            
            if not proxy_lines:
                return None
            
            proxy_line = random.choice(proxy_lines)
            
            if '://' in proxy_line:
                return {
                    'http': proxy_line,
                    'https': proxy_line
                }
            else:
                return {
                    'http': f'http://{proxy_line}',
                    'https': f'http://{proxy_line}'
                }
                
        except FileNotFoundError:
            self.logger.warning(f"Proxy fayli topilmadi: {self.proxy_file}")
            return None
        except Exception as e:
            self.logger.error(f"Proxy faylini o'qishda xato: {e}")
            return None
    
    def get_proxy_stats(self) -> Dict[str, any]:
        """Proxy statistikalarini olish"""
        if self.use_api and self.proxy_scraper:
            return self.proxy_scraper.get_proxy_stats()
        else:
            return {'source': 'file', 'total_proxies': 'unknown'}
    
    def refresh_proxies(self):
        """Proxy cache'ni majburiy yangilash"""
        if self.use_api and self.proxy_scraper:
            self.proxy_scraper.get_proxies_with_cache(force_refresh=True)
            self.logger.info("Proxy cache yangilandi")