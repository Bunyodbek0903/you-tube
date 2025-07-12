#!/usr/bin/env python3
"""
YouTube Channel Creation Automation
Automates YouTube channel creation using Google accounts
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
        self.security_manager = SecurityManager()
        self.anti_detection = AntiDetection()
        self.cookie_manager = CookieManager()
        self.captcha_solver = CaptchaSolver(self.config.ANTICAPTCHA_API_KEY)
        self.channel_generator = ChannelDataGenerator()
        self.account_generator = AccountDataGenerator()
        self.driver = None
        
    def setup_driver(self, proxy=None):
        """Setup Chrome driver with anti-detection measures"""
        try:
            options = self.anti_detection.get_browser_options(self.config.HEADLESS)
            
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Remove automation indicators
            self.anti_detection.remove_automation_indicators(self.driver)
            
            # Set window size
            self.driver.set_window_size(
                random.randint(1200, 1920),
                random.randint(800, 1080)
            )
            
            self.logger.success("Browser setup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup driver: {e}")
            return False
    
    def load_accounts(self):
        """Load accounts from file"""
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
            
            self.logger.info(f"Loaded {len(accounts)} accounts")
            return accounts
            
        except FileNotFoundError:
            self.logger.error(f"Accounts file not found: {self.config.ACCOUNTS_FILE}")
            return []
        except Exception as e:
            self.logger.error(f"Error loading accounts: {e}")
            return []
    
    def login_to_google(self, account):
        """Login to Google account"""
        try:
            self.logger.info(f"Logging in to: {account['email']}")
            
            # Go to Google login page
            self.driver.get(self.config.YOUTUBE_LOGIN_URL)
            self.anti_detection.random_delay()
            
            # Enter email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            email_input.clear()
            self.type_like_human(email_input, account['email'])
            email_input.send_keys(Keys.ENTER)
            
            self.anti_detection.human_like_delay()
            
            # Check for captcha
            if self.detect_and_solve_captcha():
                self.logger.warning("Captcha detected and solved")
            
            # Enter password
            try:
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                password_input.clear()
                self.type_like_human(password_input, account['password'])
                password_input.send_keys(Keys.ENTER)
                
                self.anti_detection.human_like_delay()
                
                # Check for captcha again
                if self.detect_and_solve_captcha():
                    self.logger.warning("Captcha detected and solved")
                
            except TimeoutException:
                self.logger.warning("Password field not found, might be already logged in")
            
            # Wait for login to complete
            time.sleep(3)
            
            # Check if login was successful
            if self.is_logged_in():
                self.logger.success(f"Successfully logged in to: {account['email']}")
                self.cookie_manager.save_cookies(self.driver, account['email'])
                return True
            else:
                self.logger.error(f"Login failed for: {account['email']}")
                return False
                
        except Exception as e:
            self.logger.error(f"Login error for {account['email']}: {e}")
            return False
    
    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            # Check for Google account avatar or profile picture
            avatar_selectors = [
                '[data-email]',
                '[aria-label*="Google Account"]',
                'img[alt*="profile"]',
                '.gb_Aa',  # Google account button
                '[data-ved]'  # Google account indicator
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
        """Detect and solve captcha if present"""
        try:
            captcha_detector = CaptchaDetector(self.driver)
            
            # Check for reCAPTCHA
            if captcha_detector.detect_recaptcha():
                site_key = captcha_detector.get_recaptcha_site_key()
                if site_key:
                    solution = self.captcha_solver.solve_recaptcha_v2(
                        site_key, self.driver.current_url
                    )
                    if solution:
                        # Inject the solution
                        self.driver.execute_script(
                            f'document.getElementById("g-recaptcha-response").innerHTML = "{solution}";'
                        )
                        return True
            
            # Check for image captcha
            if captcha_detector.detect_image_captcha():
                image_src = captcha_detector.get_captcha_image()
                if image_src:
                    solution = self.captcha_solver.solve_image_captcha_base64(image_src)
                    if solution:
                        # Find captcha input and fill it
                        try:
                            captcha_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name*="captcha"]')
                            captcha_input.clear()
                            captcha_input.send_keys(solution)
                            return True
                        except NoSuchElementException:
                            pass
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error solving captcha: {e}")
            return False
    
    def type_like_human(self, element, text):
        """Type text like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def navigate_to_youtube(self):
        """Navigate to YouTube"""
        try:
            self.driver.get("https://www.youtube.com")
            self.anti_detection.random_delay()
            
            # Check if we need to switch to channel
            if self.is_logged_in():
                self.logger.info("Navigated to YouTube successfully")
                return True
            else:
                self.logger.error("Not logged in, cannot navigate to YouTube")
                return False
                
        except Exception as e:
            self.logger.error(f"Error navigating to YouTube: {e}")
            return False
    
    def create_youtube_channel(self, account):
        """Create YouTube channel for the account"""
        try:
            self.logger.info(f"Creating YouTube channel for: {account['email']}")
            
            # Navigate to YouTube
            if not self.navigate_to_youtube():
                return False
            
            # Go to channel creation page
            self.driver.get("https://www.youtube.com/channel_switcher")
            self.anti_detection.random_delay()
            
            # Look for "Create channel" button
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
                # Try to find any link that might lead to channel creation
                try:
                    create_button = self.driver.find_element(By.CSS_SELECTOR, 'a[href*="channel"]')
                except NoSuchElementException:
                    self.logger.error("Could not find channel creation button")
                    return False
            
            create_button.click()
            self.anti_detection.human_like_delay()
            
            # Generate channel data
            channel_data = self.channel_generator.generate_channel_data()
            
            # Fill channel name
            try:
                name_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name*="name"], input[placeholder*="name"]'))
                )
                name_input.clear()
                self.type_like_human(name_input, channel_data['name'])
            except TimeoutException:
                self.logger.warning("Could not find channel name input")
            
            # Fill channel description
            try:
                desc_input = self.driver.find_element(By.CSS_SELECTOR, 'textarea[name*="description"], textarea[placeholder*="description"]')
                desc_input.clear()
                self.type_like_human(desc_input, channel_data['description'])
            except NoSuchElementException:
                self.logger.warning("Could not find description input")
            
            # Select category
            try:
                category_select = self.driver.find_element(By.CSS_SELECTOR, 'select[name*="category"], select[aria-label*="category"]')
                from selenium.webdriver.support.ui import Select
                select = Select(category_select)
                select.select_by_visible_text(channel_data['category'])
            except NoSuchElementException:
                self.logger.warning("Could not find category select")
            
            # Submit the form
            try:
                submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
                submit_button.click()
                self.anti_detection.human_like_delay()
            except NoSuchElementException:
                self.logger.warning("Could not find submit button")
            
            # Wait for channel creation to complete
            time.sleep(5)
            
            # Check if channel was created successfully
            if self.check_channel_created():
                self.logger.success(f"Channel created successfully for: {account['email']}")
                return True
            else:
                self.logger.error(f"Channel creation failed for: {account['email']}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating channel for {account['email']}: {e}")
            return False
    
    def check_channel_created(self):
        """Check if channel was created successfully"""
        try:
            # Look for indicators of successful channel creation
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
        """Process a single account"""
        try:
            self.logger.info(f"Processing account: {account['email']}")
            
            # Setup driver with proxy if available
            proxy = self.security_manager.get_working_proxy() if self.config.USE_PROXY else None
            if not self.setup_driver(proxy):
                return False
            
            # Login to Google
            if not self.login_to_google(account):
                return False
            
            # Create YouTube channel
            if not self.create_youtube_channel(account):
                return False
            
            self.logger.success(f"Successfully processed account: {account['email']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing account {account['email']}: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def run(self):
        """Main execution method"""
        try:
            self.logger.info("Starting YouTube automation")
            
            # Load accounts
            accounts = self.load_accounts()
            if not accounts:
                self.logger.error("No accounts found to process")
                return
            
            # Process each account
            for i, account in enumerate(accounts, 1):
                self.logger.info(f"Processing account {i}/{len(accounts)}")
                
                success = self.process_account(account)
                
                # Log result
                details = "Channel created successfully" if success else "Failed to create channel"
                self.result_logger.add_result(account, success, details)
                
                # Random delay between accounts
                if i < len(accounts):
                    delay = random.uniform(30, 60)
                    self.logger.info(f"Waiting {delay:.1f} seconds before next account...")
                    time.sleep(delay)
            
            # Print summary
            summary = self.result_logger.get_summary()
            self.logger.success(f"Processing completed!")
            self.logger.info(f"Total accounts: {summary['total']}")
            self.logger.info(f"Successful: {summary['successful']}")
            self.logger.info(f"Failed: {summary['failed']}")
            self.logger.info(f"Success rate: {summary['success_rate']}")
            
        except KeyboardInterrupt:
            self.logger.warning("Process interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    automation = YouTubeAutomation()
    automation.run()