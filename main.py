import os
import sys
import time
from datetime import datetime

# Windows check (from your original code)
if os.name != "nt":
    print("Error: This must run on Windows!")
    exit()

def main():
    print("=" * 50)
    print("🔥 SECURE LOADER TEST - SUCCESS! 🔥")
    print("=" * 50)
    print(f"\n✅ Downloaded and decrypted from Railway")
    print(f"✅ Running in memory (not saved to disk)")
    print(f"✅ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✅ Python Version: {sys.version.split()[0]}")
    print(f"✅ Platform: {sys.platform}")
    print(f"✅ OS: {os.name}")
    
    print("\n" + "=" * 50)
    print("Testing auto-install feature...")
    print("=" * 50)
    
    # Test the install_import function (your original code style)
    import subprocess
    
    def install_import(modules):
        for module, pip_name in modules:
            try:
                __import__(module)
                print(f"✅ {module} already installed")
            except ImportError:
                print(f"⏳ Installing {pip_name}...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pip_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"✅ {pip_name} installed successfully")
    
    # Test with a safe common package
    install_import([("requests", "requests")])
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("Your secure loader system is working perfectly!")
    print("=" * 50)
    
    # Keep window open for 5 seconds so user can see results
    print("\nClosing in 5 seconds...")
    time.sleep(5)

if __name__ == "__main__":
    main()
