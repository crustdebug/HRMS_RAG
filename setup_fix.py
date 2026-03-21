"""
Script to fix Python 3.14 compatibility issues
Run this to reinstall packages with correct versions
"""
import subprocess
import sys

print("=" * 60)
print("FIXING PYTHON 3.14 COMPATIBILITY ISSUES")
print("=" * 60)

print("\nStep 1: Uninstalling problematic packages...")
packages_to_remove = [
    "langchain",
    "langchain-community", 
    "langchain-core",
    "langchain-huggingface",
    "langchain-google-genai"
]

for pkg in packages_to_remove:
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", pkg], 
                      capture_output=True)
        print(f"  ✓ Uninstalled {pkg}")
    except:
        print(f"  - {pkg} not found")

print("\nStep 2: Installing compatible versions...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

print("\n" + "=" * 60)
print("SETUP COMPLETE!")
print("=" * 60)
print("\nNow run:")
print("  uvicorn app.main:app --reload --port 8000")
