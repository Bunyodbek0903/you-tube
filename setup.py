#!/usr/bin/env python3
"""
Setup script for YouTube Automation
"""

import os
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'data', 'config']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_files():
    """Create necessary files if they don't exist"""
    files_to_create = {
        'accounts.txt': 'accounts.txt.example',
        'proxies.txt': 'proxies.txt.example', 
        'user_agents.txt': 'user_agents.txt.example',
        '.env': '.env.example'
    }
    
    for target, source in files_to_create.items():
        if not os.path.exists(target) and os.path.exists(source):
            shutil.copy2(source, target)
            print(f"✓ Created {target} from {source}")
        elif os.path.exists(target):
            print(f"✓ {target} already exists")
        else:
            print(f"⚠ {source} not found, please create {target} manually")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import selenium
        print("✓ Selenium installed")
    except ImportError:
        print("✗ Selenium not installed. Run: pip install selenium")
    
    try:
        import requests
        print("✓ Requests installed")
    except ImportError:
        print("✗ Requests not installed. Run: pip install requests")
    
    try:
        import fake_useragent
        print("✓ Fake-useragent installed")
    except ImportError:
        print("✗ Fake-useragent not installed. Run: pip install fake-useragent")

def main():
    """Main setup function"""
    print("🚀 Setting up YouTube Automation...")
    print()
    
    # Create directories
    print("📁 Creating directories...")
    create_directories()
    print()
    
    # Create files
    print("📄 Creating configuration files...")
    create_files()
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    check_dependencies()
    print()
    
    print("✅ Setup completed!")
    print()
    print("📋 Next steps:")
    print("1. Edit .env file with your settings")
    print("2. Add your Google accounts to accounts.txt")
    print("3. Add proxies to proxies.txt (optional)")
    print("4. Get Anti-captcha API key from https://anti-captcha.com")
    print("5. Run: python youtube_automation.py")
    print()
    print("⚠️  Remember: Only use this with your own accounts!")

if __name__ == "__main__":
    main()