import time
import base64
from typing import Optional
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from anticaptchaofficial.recaptchav3proxyless import recaptchaV3Proxyless
from anticaptchaofficial.imagecaptcha import imagecaptcha

class CaptchaSolver:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.solver = None
    
    def solve_recaptcha_v2(self, site_key: str, url: str) -> Optional[str]:
        """Solve reCAPTCHA v2"""
        try:
            solver = recaptchaV2Proxyless()
            solver.set_verbose(1)
            solver.set_key(self.api_key)
            solver.set_website_url(url)
            solver.set_website_key(site_key)
            
            response = solver.solve_and_return_solution()
            if response != 0:
                return response
            else:
                print(f"Error solving captcha: {solver.error_code}")
                return None
        except Exception as e:
            print(f"Error in solve_recaptcha_v2: {e}")
            return None
    
    def solve_recaptcha_v3(self, site_key: str, url: str, action: str = "submit") -> Optional[str]:
        """Solve reCAPTCHA v3"""
        try:
            solver = recaptchaV3Proxyless()
            solver.set_verbose(1)
            solver.set_key(self.api_key)
            solver.set_website_url(url)
            solver.set_website_key(site_key)
            solver.set_action(action)
            solver.set_min_score(0.3)
            
            response = solver.solve_and_return_solution()
            if response != 0:
                return response
            else:
                print(f"Error solving captcha: {solver.error_code}")
                return None
        except Exception as e:
            print(f"Error in solve_recaptcha_v3: {e}")
            return None
    
    def solve_image_captcha(self, image_path: str) -> Optional[str]:
        """Solve image captcha"""
        try:
            solver = imagecaptcha()
            solver.set_verbose(1)
            solver.set_key(self.api_key)
            
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            solver.set_image(image_data)
            response = solver.solve_and_return_solution()
            
            if response != 0:
                return response
            else:
                print(f"Error solving image captcha: {solver.error_code}")
                return None
        except Exception as e:
            print(f"Error in solve_image_captcha: {e}")
            return None
    
    def solve_image_captcha_base64(self, image_base64: str) -> Optional[str]:
        """Solve image captcha from base64 string"""
        try:
            solver = imagecaptcha()
            solver.set_verbose(1)
            solver.set_key(self.api_key)
            
            # Remove data:image/...;base64, prefix if present
            if ',' in image_base64:
                image_base64 = image_base64.split(',')[1]
            
            image_data = base64.b64decode(image_base64)
            solver.set_image(image_data)
            response = solver.solve_and_return_solution()
            
            if response != 0:
                return response
            else:
                print(f"Error solving image captcha: {solver.error_code}")
                return None
        except Exception as e:
            print(f"Error in solve_image_captcha_base64: {e}")
            return None
    
    def wait_for_captcha_solution(self, timeout: int = 60) -> Optional[str]:
        """Wait for captcha solution with timeout"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if hasattr(self.solver, 'get_solution') and self.solver.get_solution():
                return self.solver.get_solution()
            time.sleep(2)
        
        return None

class CaptchaDetector:
    def __init__(self, driver):
        self.driver = driver
    
    def detect_recaptcha(self) -> bool:
        """Detect if reCAPTCHA is present"""
        try:
            # Check for reCAPTCHA elements
            recaptcha_selectors = [
                'iframe[src*="recaptcha"]',
                '.g-recaptcha',
                '#recaptcha',
                '[data-sitekey]'
            ]
            
            for selector in recaptcha_selectors:
                elements = self.driver.find_elements_by_css_selector(selector)
                if elements:
                    return True
            
            return False
        except:
            return False
    
    def get_recaptcha_site_key(self) -> Optional[str]:
        """Get reCAPTCHA site key"""
        try:
            # Try different selectors for site key
            selectors = [
                '[data-sitekey]',
                '.g-recaptcha[data-sitekey]',
                'div[data-sitekey]'
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements_by_css_selector(selector)
                for element in elements:
                    site_key = element.get_attribute('data-sitekey')
                    if site_key:
                        return site_key
            
            return None
        except:
            return None
    
    def detect_image_captcha(self) -> bool:
        """Detect if image captcha is present"""
        try:
            # Check for common image captcha elements
            captcha_selectors = [
                'img[src*="captcha"]',
                '.captcha',
                '#captcha',
                '[class*="captcha"]'
            ]
            
            for selector in captcha_selectors:
                elements = self.driver.find_elements_by_css_selector(selector)
                if elements:
                    return True
            
            return False
        except:
            return False
    
    def get_captcha_image(self) -> Optional[str]:
        """Get captcha image as base64"""
        try:
            # Find captcha image
            img_selectors = [
                'img[src*="captcha"]',
                '.captcha img',
                '#captcha img'
            ]
            
            for selector in img_selectors:
                elements = self.driver.find_elements_by_css_selector(selector)
                for element in elements:
                    src = element.get_attribute('src')
                    if src and 'captcha' in src.lower():
                        return src
            
            return None
        except:
            return None