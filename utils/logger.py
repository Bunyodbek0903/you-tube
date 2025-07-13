import json
import time
from datetime import datetime
from loguru import logger
from colorama import Fore, Style, init

init(autoreset=True)

class Logger:
    def __init__(self, log_file="youtube_automation.log"):
        self.log_file = log_file
        self.setup_logger()
    
    def setup_logger(self):
        """Logger konfiguratsiyasini o'rnatish"""
        logger.remove()
        logger.add(
            self.log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO",
            rotation="10 MB",
            retention="7 days"
        )
        logger.add(
            lambda msg: print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}"),
            format="{time:HH:mm:ss} | {level} | {message}",
            level="INFO"
        )
    
    def info(self, message):
        """Ma'lumot xabarini log qilish"""
        logger.info(message)
    
    def success(self, message):
        """Muvaffaqiyat xabarini log qilish"""
        logger.success(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    def warning(self, message):
        """Ogohlantirish xabarini log qilish"""
        logger.warning(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    def error(self, message):
        """Xato xabarini log qilish"""
        logger.error(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    def debug(self, message):
        """Debug xabarini log qilish"""
        logger.debug(message)

class ResultLogger:
    def __init__(self, results_file="results.json"):
        self.results_file = results_file
        self.results = self.load_results()
    
    def load_results(self):
        """Mavjud natijalarni fayldan yuklash"""
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "start_time": datetime.now().isoformat(),
                "total_accounts": 0,
                "successful": 0,
                "failed": 0,
                "accounts": []
            }
    
    def add_result(self, account_info, success, details):
        """Hisob uchun natija qo'shish"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "email": account_info.get("email", ""),
            "success": success,
            "details": details
        }
        
        self.results["accounts"].append(result)
        self.results["total_accounts"] += 1
        
        if success:
            self.results["successful"] += 1
        else:
            self.results["failed"] += 1
        
        self.save_results()
    
    def save_results(self):
        """Natijalarni faylga saqlash"""
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
    
    def get_summary(self):
        """Natijalar xulosasini olish"""
        return {
            "total": self.results["total_accounts"],
            "successful": self.results["successful"],
            "failed": self.results["failed"],
            "success_rate": f"{(self.results['successful'] / max(self.results['total_accounts'], 1)) * 100:.1f}%"
        }