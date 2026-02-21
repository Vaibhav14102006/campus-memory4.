"""
Quick Setup for Poster Information Extraction
This script helps you set up all dependencies for automatic poster analysis
"""

import subprocess
import sys

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(cmd, description):
    """Run a command and display the result"""
    print(f"📦 {description}...")
    try:
        subprocess.check_call(cmd, shell=True)
        print(f"✅ {description} - SUCCESS\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e}\n")
        return False

def main():
    print_header("Poster Extraction Feature Setup")
    
    print("This script will install all dependencies needed for")
    print("automatic poster information extraction using AI/ML.\n")
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️  Warning: Python 3.8+ recommended")
    print()
    
    # Install dependencies
    steps = [
        ("pip install paddleocr paddlepaddle", "Installing PaddleOCR (Text Extraction)"),
        ("pip install transformers torch", "Installing Transformers & PyTorch (NLP)"),
        ("pip install spacy", "Installing spaCy (NER)"),
        ("python -m spacy download en_core_web_sm", "Downloading spaCy English model"),
        ("pip install python-dateutil", "Installing date parsing utilities"),
        ("pip install Pillow", "Installing image processing library"),
    ]
    
    success_count = 0
    for cmd, desc in steps:
        if run_command(cmd, desc):
            success_count += 1
    
    print_header("Setup Complete")
    
    print(f"✅ {success_count}/{len(steps)} components installed successfully\n")
    
    if success_count == len(steps):
        print("🎉 All dependencies installed!")
        print("\nNext steps:")
        print("1. Test the system:")
        print("   python test_poster_extraction.py")
        print()
        print("2. Start the API server:")
        print("   python event_api_server.py")
        print()
        print("3. Open the frontend and test poster upload")
        print()
        print("📖 Full documentation: POSTER_EXTRACTION_GUIDE.md")
    else:
        print("⚠️  Some components failed to install.")
        print("Please check the errors above and try again.")
        print("You may need to install them manually.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Setup error: {e}")
        import traceback
        traceback.print_exc()
