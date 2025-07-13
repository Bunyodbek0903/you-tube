#!/usr/bin/env python3
"""
YouTube Avtomatizatsiyasi uchun o'rnatish skripti
"""

import os
import shutil
from pathlib import Path

def create_directories():
    """Kerakli papkalarni yaratish"""
    directories = ['logs', 'data', 'config']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Papka yaratildi: {directory}")

def create_files():
    """Kerakli fayllarni yaratish (agar mavjud bo'lmasa)"""
    files_to_create = {
        'accounts.txt': 'accounts.txt.example',
        'proxies.txt': 'proxies.txt.example', 
        'user_agents.txt': 'user_agents.txt.example',
        '.env': '.env.example'
    }
    
    for target, source in files_to_create.items():
        if not os.path.exists(target) and os.path.exists(source):
            shutil.copy2(source, target)
            print(f"✓ {target} {source} dan yaratildi")
        elif os.path.exists(target):
            print(f"✓ {target} allaqachon mavjud")
        else:
            print(f"⚠ {source} topilmadi, {target} ni qo'lda yarating")

def check_dependencies():
    """Kerakli dasturlar o'rnatilganini tekshirish"""
    try:
        import selenium
        print("✓ Selenium o'rnatilgan")
    except ImportError:
        print("✗ Selenium o'rnatilmagan. Bajarish: pip install selenium")
    
    try:
        import requests
        print("✓ Requests o'rnatilgan")
    except ImportError:
        print("✗ Requests o'rnatilmagan. Bajarish: pip install requests")
    
    try:
        import fake_useragent
        print("✓ Fake-useragent o'rnatilgan")
    except ImportError:
        print("✗ Fake-useragent o'rnatilmagan. Bajarish: pip install fake-useragent")

def main():
    """Asosiy o'rnatish funksiyasi"""
    print("🚀 YouTube Avtomatizatsiyasi o'rnatilmoqda...")
    print()
    
    # Papkalarni yaratish
    print("📁 Papkalar yaratilmoqda...")
    create_directories()
    print()
    
    # Fayllarni yaratish
    print("📄 Konfiguratsiya fayllari yaratilmoqda...")
    create_files()
    print()
    
    # Dasturlarni tekshirish
    print("🔍 Dasturlar tekshirilmoqda...")
    check_dependencies()
    print()
    
    print("✅ O'rnatish tugallandi!")
    print()
    print("📋 Keyingi qadamlari:")
    print("1. .env faylini sozlamalaringiz bilan tahrirlang")
    print("2. accounts.txt ga Google hisoblaringizni qo'shing")
    print("3. proxies.txt ga proxylarni qo'shing (ixtiyoriy)")
    print("4. https://anti-captcha.com dan Anti-captcha API kalitini oling")
    print("5. Bajarish: python youtube_automation.py")
    print()
    print("⚠️  Eslatma: Faqat o'z hisoblaringizda ishlating!")

if __name__ == "__main__":
    main()