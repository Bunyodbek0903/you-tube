import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Anti-captcha API key
    ANTICAPTCHA_API_KEY = os.getenv('ANTICAPTCHA_API_KEY', '')
    
    # Proxy settings
    USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
    USE_PROXY_API = os.getenv('USE_PROXY_API', 'True').lower() == 'true'
    PROXY_LIST_FILE = os.getenv('PROXY_LIST_FILE', 'proxies.txt')
    
    # ProxyScrape API settings
    PROXY_TYPE = os.getenv('PROXY_TYPE', 'http')  # http, https, socks4, socks5
    PROXY_TIMEOUT = int(os.getenv('PROXY_TIMEOUT', '10000'))  # milliseconds
    PROXY_SSL = os.getenv('PROXY_SSL', 'all')  # yes, no, all
    PROXY_ANONYMITY = os.getenv('PROXY_ANONYMITY', 'all')  # elite, anonymous, transparent, all
    PROXY_COUNTRY = os.getenv('PROXY_COUNTRY', 'all')  # country code or 'all'
    PROXY_CACHE_DURATION = int(os.getenv('PROXY_CACHE_DURATION', '300'))  # seconds
    
    # Browser settings
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    BROWSER_TIMEOUT = int(os.getenv('BROWSER_TIMEOUT', '30'))
    
    # Delay settings (seconds)
    MIN_DELAY = float(os.getenv('MIN_DELAY', '2'))
    MAX_DELAY = float(os.getenv('MAX_DELAY', '5'))
    
    # YouTube URLs
    YOUTUBE_LOGIN_URL = "https://accounts.google.com/signin"
    YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel_switcher"
    
    # File paths
    ACCOUNTS_FILE = os.getenv('ACCOUNTS_FILE', 'accounts.txt')
    RESULTS_FILE = os.getenv('RESULTS_FILE', 'results.json')
    LOG_FILE = os.getenv('LOG_FILE', 'youtube_automation.log')
    
    # User agent rotation
    USER_AGENT_FILE = os.getenv('USER_AGENT_FILE', 'user_agents.txt')
    
    # Captcha settings
    CAPTCHA_TIMEOUT = int(os.getenv('CAPTCHA_TIMEOUT', '60'))
    
    # Retry settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '10'))