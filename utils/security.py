import random
import time
import requests
from fake_useragent import UserAgent
from typing import List, Dict, Optional
from utils.proxy_manager import ProxyManager

class SecurityManager:
    def __init__(self, proxy_file: str = "proxies.txt", user_agent_file: str = "user_agents.txt", 
                 use_proxy_api: bool = True, logger=None, config=None):
        self.proxy_file = proxy_file
        self.user_agent_file = user_agent_file
        self.use_proxy_api = use_proxy_api
        self.logger = logger
        self.config = config
        self.proxy_manager = ProxyManager(use_api=use_proxy_api, proxy_file=proxy_file, logger=logger, config=config)
        self.user_agents = self.load_user_agents()
        self.ua = UserAgent()
    
    def load_proxies(self) -> List[str]:
        """Load proxies from file (legacy method)"""
        try:
            with open(self.proxy_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    def load_user_agents(self) -> List[str]:
        """Load custom user agents from file"""
        try:
            with open(self.user_agent_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    def get_random_user_agent(self) -> str:
        """Get random user agent"""
        if self.user_agents:
            return random.choice(self.user_agents)
        return self.ua.random
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """Get random proxy using API or file"""
        if self.use_proxy_api:
            return self.proxy_manager.get_proxy()
        else:
            # Fallback to file-based method
            if not hasattr(self, 'proxies'):
                self.proxies = self.load_proxies()
            
            if not self.proxies:
                return None
            
            proxy = random.choice(self.proxies)
            if '://' in proxy:
                return {
                    'http': proxy,
                    'https': proxy
                }
            else:
                return {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
    
    def test_proxy(self, proxy: Dict[str, str]) -> bool:
        """Test if proxy is working"""
        try:
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxy,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def get_working_proxy(self) -> Optional[Dict[str, str]]:
        """Get a working proxy"""
        if self.use_proxy_api:
            return self.proxy_manager.get_proxy()
        else:
            # Fallback to file-based method
            if not hasattr(self, 'proxies'):
                self.proxies = self.load_proxies()
            
            if not self.proxies:
                return None
            
            # Test up to 5 random proxies
            for _ in range(5):
                proxy = self.get_random_proxy()
                if proxy and self.test_proxy(proxy):
                    return proxy
            
            return None

class AntiDetection:
    def __init__(self):
        self.security_manager = SecurityManager()
    
    def random_delay(self, min_delay: float = 2, max_delay: float = 5):
        """Random delay between actions"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def human_like_delay(self):
        """More human-like delay pattern"""
        # Sometimes longer delays
        if random.random() < 0.1:  # 10% chance
            time.sleep(random.uniform(8, 15))
        else:
            time.sleep(random.uniform(1, 4))
    
    def get_browser_options(self, headless: bool = False):
        """Get browser options with anti-detection measures"""
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        
        if headless:
            options.add_argument('--headless')
        
        # Anti-detection measures
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agent = self.security_manager.get_random_user_agent()
        options.add_argument(f'--user-agent={user_agent}')
        
        # Window size
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        options.add_argument(f'--window-size={width},{height}')
        
        return options
    
    def execute_script(self, driver, script: str):
        """Execute JavaScript to remove automation indicators"""
        driver.execute_script(script)
    
    def remove_automation_indicators(self, driver):
        """Remove automation indicators from browser"""
        scripts = [
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
            "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})"
        ]
        
        for script in scripts:
            try:
                driver.execute_script(script)
            except:
                pass

class CookieManager:
    def __init__(self):
        self.cookies = {}
    
    def save_cookies(self, driver, account_email: str):
        """Save cookies for an account"""
        try:
            cookies = driver.get_cookies()
            self.cookies[account_email] = cookies
        except Exception as e:
            print(f"Error saving cookies: {e}")
    
    def load_cookies(self, driver, account_email: str):
        """Load cookies for an account"""
        if account_email in self.cookies:
            try:
                for cookie in self.cookies[account_email]:
                    driver.add_cookie(cookie)
                return True
            except Exception as e:
                print(f"Error loading cookies: {e}")
        return False