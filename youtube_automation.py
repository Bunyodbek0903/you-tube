#!/usr/bin/env python3
"""
YouTube Kanal Yaratish Avtomatizatsiyasi
Google hisoblarini ishlatib YouTube kanallarini avtomatik yaratish
"""

import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from config import Config
from utils.logger import Logger, ResultLogger
from utils.security import SecurityManager, AntiDetection, CookieManager
from utils.captcha_solver import CaptchaSolver, CaptchaDetector
from utils.data_generator import ChannelDataGenerator, AccountDataGenerator

class YouTubeAutomation:
    def __init__(self):
        self.config = Config()
        self.logger = Logger(self.config.LOG_FILE)
        self.result_logger = ResultLogger(self.config.RESULTS_FILE)
        self.security_manager = SecurityManager(
            proxy_file=self.config.PROXY_LIST_FILE,
            use_proxy_api=self.config.USE_PROXY_API,
            logger=self.logger,
            config=self.config
        )
        self.anti_detection = AntiDetection()
        self.cookie_manager = CookieManager()
        self.captcha_solver = CaptchaSolver(self.config.ANTICAPTCHA_API_KEY)
        self.channel_generator = ChannelDataGenerator()
        self.account_generator = AccountDataGenerator()
        self.driver = None
        
    def setup_driver(self, proxy=None):
        """Anti-detection choralari bilan Chrome driver o'rnatish"""
        try:
            options = self.anti_detection.get_browser_options(self.config.HEADLESS)
            
            if proxy:
                # Proxy URL ni proxy dict dan ajratib olish
                proxy_url = proxy.get('http', '').replace('http://', '')
                if proxy_url:
                    options.add_argument(f'--proxy-server={proxy_url}')
                    self.logger.info(f"Browserga proxy qo'shildi: {proxy_url}")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Avtomatlashtirish belgilarini olib tashlash
            self.anti_detection.remove_automation_indicators(self.driver)
            
            # Oyna o'lchamini o'rnatish
            self.driver.set_window_size(
                random.randint(1200, 1920),
                random.randint(800, 1080)
            )
            
            self.logger.success("Browser o'rnatish tugallandi")
            return True
            
        except Exception as e:
            self.logger.error(f"Driver o'rnatishda xato: {e}")
            return False
    
    def load_accounts(self):
        """Fayldan hisoblarni yuklash"""
        try:
            accounts = []
            with open(self.config.ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        email, password = line.split(':', 1)
                        accounts.append({
                            'email': email.strip(),
                            'password': password.strip()
                        })
            
            self.logger.info(f"{len(accounts)} ta hisob yuklandi")
            return accounts
            
        except FileNotFoundError:
            self.logger.error(f"Hisoblar fayli topilmadi: {self.config.ACCOUNTS_FILE}")
            return []
        except Exception as e:
            self.logger.error(f"Hisoblarni yuklashda xato: {e}")
            return []
    
    def login_to_google(self, account):
        """Google hisobiga kirish"""
        try:
            self.logger.info(f"Kirish amalga oshirilmoqda: {account['email']}")
            
            # Google kirish sahifasiga o'tish
            self.driver.get(self.config.YOUTUBE_LOGIN_URL)
            self.anti_detection.random_delay()
            
            # Email kiritish
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            email_input.clear()
            self.type_like_human(email_input, account['email'])
            email_input.send_keys(Keys.ENTER)
            
            self.anti_detection.human_like_delay()
            
            # Captcha mavjudligini tekshirish
            if self.detect_and_solve_captcha():
                self.logger.warning("Captcha aniqlandi va yechildi")
            
            # Parol kiritish
            try:
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                password_input.clear()
                self.type_like_human(password_input, account['password'])
                password_input.send_keys(Keys.ENTER)
                
                self.anti_detection.human_like_delay()
                
                # Yana captcha tekshirish
                if self.detect_and_solve_captcha():
                    self.logger.warning("Captcha aniqlandi va yechildi")
                
            except TimeoutException:
                self.logger.warning("Parol maydoni topilmadi, allaqachon kiringan bo'lishi mumkin")
            
            # Kirish tugashini kutish
            time.sleep(3)
            
            # Kirish muvaffaqiyatini tekshirish
            if self.is_logged_in():
                self.logger.success(f"Google hisobiga muvaffaqiyatli kirdi: {account['email']}")
                self.cookie_manager.save_cookies(self.driver, account['email'])
                return True
            else:
                self.logger.error(f"Kirish amalga oshmadi: {account['email']}")
                return False
                
        except Exception as e:
            self.logger.error(f"{account['email']} uchun kirish xatosi: {e}")
            return False
    
    def is_logged_in(self):
        """Foydalanuvchi kiringanini tekshirish"""
        try:
            # Google hisob avatar yoki profil rasmini tekshirish
            avatar_selectors = [
                '[data-email]',
                '[aria-label*="Google Account"]',
                'img[alt*="profile"]',
                '.gb_Aa',  # Google hisob tugmasi
                '[data-ved]'  # Google hisob ko'rsatkichi
            ]
            
            for selector in avatar_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        return True
                except NoSuchElementException:
                    continue
            
            return False
            
        except Exception:
            return False
    
    def detect_and_solve_captcha(self):
        """Captcha mavjudligini aniqlash va yechish"""
        try:
            captcha_detector = CaptchaDetector(self.driver)
            
            # reCAPTCHA ni tekshirish
            if captcha_detector.detect_recaptcha():
                site_key = captcha_detector.get_recaptcha_site_key()
                if site_key:
                    solution = self.captcha_solver.solve_recaptcha_v2(
                        site_key, self.driver.current_url
                    )
                    if solution:
                        # Yechimni kiritish
                        self.driver.execute_script(
                            f'document.getElementById("g-recaptcha-response").innerHTML = "{solution}";'
                        )
                        return True
            
            # Rasm captcha ni tekshirish
            if captcha_detector.detect_image_captcha():
                image_src = captcha_detector.get_captcha_image()
                if image_src:
                    solution = self.captcha_solver.solve_image_captcha_base64(image_src)
                    if solution:
                        # Captcha input ni topish va to'ldirish
                        try:
                            captcha_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name*="captcha"]')
                            captcha_input.clear()
                            captcha_input.send_keys(solution)
                            return True
                        except NoSuchElementException:
                            pass
            
            return False
            
        except Exception as e:
            self.logger.error(f"Captcha yechishda xato: {e}")
            return False
    
    def type_like_human(self, element, text):
        """Matnni inson kabi tasodifiy kechikishlar bilan yozish"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def navigate_to_youtube(self):
        """YouTube ga o'tish"""
        try:
            self.driver.get("https://www.youtube.com")
            self.anti_detection.random_delay()
            
            # Kanalga o'tish kerakligini tekshirish
            if self.is_logged_in():
                self.logger.info("YouTube ga muvaffaqiyatli o'tildi")
                return True
            else:
                self.logger.error("Kirmagan, YouTube ga o'ta olmaydi")
                return False
                
        except Exception as e:
            self.logger.error(f"YouTube ga o'tishda xato: {e}")
            return False
    
    def create_youtube_channel(self, account):
        """Hisob uchun YouTube kanal yaratish"""
        try:
            self.logger.info(f"YouTube kanal yaratilmoqda: {account['email']}")
            
            # YouTube ga o'tish
            if not self.navigate_to_youtube():
                return False
            
            # Kanal yaratish sahifasiga o'tish
            self.driver.get("https://www.youtube.com/channel_switcher")
            self.anti_detection.random_delay()
            
            # "Kanal yaratish" tugmasini qidirish
            create_channel_selectors = [
                'a[href*="create_channel"]',
                'button[aria-label*="Create channel"]',
                'a[aria-label*="Create channel"]',
                '[data-ved*="create_channel"]',
                'a:contains("Create channel")'
            ]
            
            create_button = None
            for selector in create_channel_selectors:
                try:
                    create_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not create_button:
                # Kanal yaratishga olib boradigan har qanday havolani topishga harakat qilish
                try:
                    create_button = self.driver.find_element(By.CSS_SELECTOR, 'a[href*="channel"]')
                except NoSuchElementException:
                    self.logger.error("Kanal yaratish tugmasi topilmadi")
                    return False
            
            create_button.click()
            self.anti_detection.human_like_delay()
            
            # Kanal ma'lumotlarini yaratish
            channel_data = self.channel_generator.generate_channel_data()
            
            # Kanal nomini to'ldirish
            try:
                name_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name*="name"], input[placeholder*="name"]'))
                )
                name_input.clear()
                self.type_like_human(name_input, channel_data['name'])
            except TimeoutException:
                self.logger.warning("Kanal nomi input maydoni topilmadi")
            
            # Kanal tavsifini to'ldirish
            try:
                desc_input = self.driver.find_element(By.CSS_SELECTOR, 'textarea[name*="description"], textarea[placeholder*="description"]')
                desc_input.clear()
                self.type_like_human(desc_input, channel_data['description'])
            except NoSuchElementException:
                self.logger.warning("Tavsif input maydoni topilmadi")
            
            # Kategoriyani tanlash
            try:
                category_select = self.driver.find_element(By.CSS_SELECTOR, 'select[name*="category"], select[aria-label*="category"]')
                from selenium.webdriver.support.ui import Select
                select = Select(category_select)
                select.select_by_visible_text(channel_data['category'])
            except NoSuchElementException:
                self.logger.warning("Kategoriya tanlash maydoni topilmadi")
            
            # Formani yuborish
            try:
                submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
                submit_button.click()
                self.anti_detection.human_like_delay()
            except NoSuchElementException:
                self.logger.warning("Yuborish tugmasi topilmadi")
            
            # Kanal yaratish tugashini kutish
            time.sleep(5)
            
            # Kanal muvaffaqiyatli yaratilganini tekshirish
            if self.check_channel_created():
                self.logger.success(f"Kanal muvaffaqiyatli yaratildi: {account['email']}")
                return True
            else:
                self.logger.error(f"Kanal yaratish amalga oshmadi: {account['email']}")
                return False
                
        except Exception as e:
            self.logger.error(f"{account['email']} uchun kanal yaratishda xato: {e}")
            return False
    
    def check_channel_created(self):
        """Kanal muvaffaqiyatli yaratilganini tekshirish"""
        try:
            # Muvaffaqiyatli kanal yaratish ko'rsatkichlarini qidirish
            success_indicators = [
                'a[href*="/channel/"]',
                '[data-ved*="channel"]',
                'img[alt*="channel"]',
                '.ytd-channel-name'
            ]
            
            for selector in success_indicators:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        return True
                except NoSuchElementException:
                    continue
            
            return False
            
        except Exception:
            return False
    
    def process_account(self, account):
        """Bitta hisobni qayta ishlash"""
        try:
            self.logger.info(f"Hisob qayta ishlanmoqda: {account['email']}")
            
            # Proxy mavjud bo'lsa driver o'rnatish
            proxy = None
            if self.config.USE_PROXY:
                proxy = self.security_manager.get_working_proxy()
                if proxy:
                    self.logger.info(f"Proxy ishlatilmoqda: {proxy['http']}")
                else:
                    self.logger.warning("Ishlayotgan proxy topilmadi, proxy siz davom etilmoqda")
            
            if not self.setup_driver(proxy):
                return False
            
            # Google ga kirish
            if not self.login_to_google(account):
                return False
            
            # YouTube kanal yaratish
            if not self.create_youtube_channel(account):
                return False
            
            self.logger.success(f"Hisob muvaffaqiyatli qayta ishlandi: {account['email']}")
            return True
            
        except Exception as e:
            self.logger.error(f"{account['email']} hisobini qayta ishlashda xato: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def run(self):
        """Asosiy bajarish metodi"""
        try:
            self.logger.info("YouTube avtomatizatsiyasi boshlanmoqda")
            
            # Hisoblarni yuklash
            accounts = self.load_accounts()
            if not accounts:
                self.logger.error("Qayta ishlash uchun hisob topilmadi")
                return
            
            # Har bir hisobni qayta ishlash
            for i, account in enumerate(accounts, 1):
                self.logger.info(f"Hisob qayta ishlanmoqda {i}/{len(accounts)}")
                
                success = self.process_account(account)
                
                # Natijani log qilish
                details = "Kanal muvaffaqiyatli yaratildi" if success else "Kanal yaratish amalga oshmadi"
                self.result_logger.add_result(account, success, details)
                
                # Hisoblar orasida tasodifiy kechikish
                if i < len(accounts):
                    delay = random.uniform(30, 60)
                    self.logger.info(f"Keyingi hisob oldidan {delay:.1f} soniya kutilmoqda...")
                    time.sleep(delay)
            
            # Xulosa chop etish
            summary = self.result_logger.get_summary()
            self.logger.success(f"Qayta ishlash tugallandi!")
            self.logger.info(f"Jami hisoblar: {summary['total']}")
            self.logger.info(f"Muvaffaqiyatli: {summary['successful']}")
            self.logger.info(f"Amalga oshmagan: {summary['failed']}")
            self.logger.info(f"Muvaffaqiyat darajasi: {summary['success_rate']}")
            
        except KeyboardInterrupt:
            self.logger.warning("Foydalanuvchi tomonidan jarayon to'xtatildi")
        except Exception as e:
            self.logger.error(f"Kutilmagan xato: {e}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    automation = YouTubeAutomation()
    automation.run()