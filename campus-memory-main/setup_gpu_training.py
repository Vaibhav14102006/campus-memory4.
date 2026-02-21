"""
GPU Setup Checker & Installer for ML Model Training
Checks GPU availability and installs required packages for CUDA acceleration
"""

import subprocess
import sys
import platform

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def check_nvidia_gpu():
    """Check if NVIDIA GPU is available"""
    print("🔍 Checking for NVIDIA GPU...")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ NVIDIA GPU detected!")
                print("\nGPU Information:")
                print(result.stdout.split('\n')[8])  # GPU info line
                return True
        else:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ NVIDIA GPU detected!")
                return True
    except:
        pass
    
    print("❌ No NVIDIA GPU detected")
    print("   You can still train models on CPU (slower)")
    return False

def check_cuda():
    """Check CUDA installation"""
    print("\n🔍 Checking CUDA installation...")
    try:
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = [line for line in result.stdout.split('\n') if 'release' in line.lower()][0]
            print(f"✅ CUDA installed: {version_line.strip()}")
            return True
    except:
        pass
    
    print("⚠️  CUDA toolkit not found")
    return False

def check_pytorch():
    """Check PyTorch and CUDA support"""
    print("\n🔍 Checking PyTorch installation...")
    try:
        import torch
        print(f"✅ PyTorch installed: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ PyTorch CUDA support: Enabled")
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   GPU count: {torch.cuda.device_count()}")
            print(f"   GPU name: {torch.cuda.get_device_name(0)}")
            print(f"   GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
            return True
        else:
            print("⚠️  PyTorch installed but CUDA not available")
            print("   CPU-only version detected")
            return False
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def install_gpu_pytorch():
    """Install PyTorch with CUDA support"""
    print("\n📦 Installing PyTorch with CUDA 12.1 support...")
    print("   This will download ~2.4GB")
    
    cmd = [
        sys.executable, "-m", "pip", "install",
        "torch", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu121"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ PyTorch with CUDA installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install PyTorch with CUDA")
        return False

def install_ml_packages():
    """Install ML training packages"""
    print("\n📦 Installing ML training packages...")
    
    packages = [
        "transformers",
        "datasets",
        "accelerate",
        "scikit-learn"
    ]
    
    for package in packages:
        print(f"   Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"   ✅ {package} installed")
        except:
            print(f"   ⚠️  {package} installation failed")
    
    print("✅ ML packages installation complete!")

def main():
    print_header("GPU SETUP FOR ML MODEL TRAINING")
    
    print("This script will:")
    print("1. Check for NVIDIA GPU")
    print("2. Check CUDA installation")
    print("3. Install PyTorch with GPU support")
    print("4. Install ML training libraries")
    
    # Check GPU
    has_gpu = check_nvidia_gpu()
    
    # Check CUDA
    has_cuda = check_cuda()
    
    if not has_gpu:
        print("\n" + "="*70)
        print("⚠️  NO GPU DETECTED")
        print("="*70)
        print("\nYour system doesn't have an NVIDIA GPU.")
        print("You can still train models on CPU, but it will be slower.")
        print("\nOptions:")
        print("1. Continue with CPU-only installation")
        print("2. Exit and check GPU drivers")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice == "2":
            print("\nPlease install NVIDIA GPU drivers from:")
            print("https://www.nvidia.com/download/index.aspx")
            sys.exit(0)
    
    # Check PyTorch
    has_pytorch_cuda = check_pytorch()
    
    if not has_pytorch_cuda and has_gpu:
        print("\n" + "="*70)
        print("📥 PYTORCH WITH CUDA INSTALLATION REQUIRED")
        print("="*70)
        
        if not has_cuda:
            print("\n⚠️  CUDA Toolkit Not Found!")
            print("\nBefore installing PyTorch with CUDA, you need:")
            print("1. NVIDIA GPU drivers")
            print("2. CUDA Toolkit 12.1 or 12.6")
            print("\nDownload from: https://developer.nvidia.com/cuda-downloads")
            print("\nOr, install PyTorch which bundles CUDA libraries:")
            
        response = input("\nInstall PyTorch with CUDA support? (y/n): ").strip().lower()
        if response == 'y':
            install_gpu_pytorch()
            
            # Verify installation
            print("\n🔍 Verifying installation...")
            try:
                import torch
                if torch.cuda.is_available():
                    print("✅ SUCCESS! GPU acceleration is ready!")
                    print(f"   GPU: {torch.cuda.get_device_name(0)}")
                else:
                    print("⚠️  PyTorch installed but GPU not detected")
                    print("   You may need to restart your terminal")
            except:
                print("❌ Installation verification failed")
    
    # Install other ML packages
    print("\n" + "="*70)
    response = input("\nInstall ML training packages (transformers, datasets, etc.)? (y/n): ").strip().lower()
    if response == 'y':
        install_ml_packages()
    
    # Summary
    print_header("SETUP COMPLETE")
    
    print("✅ Setup finished!\n")
    print("📋 Next Steps:")
    print("\n1. Test GPU availability:")
    print("   python -c \"import torch; print(f'CUDA available: {torch.cuda.is_available()}')\"\n")
    print("2. Train models with GPU:")
    print("   python train_models_gpu.py\n")
    print("3. Or use fast training:")
    print("   python train_all_models_fast.py\n")
    
    if has_gpu and has_pytorch_cuda:
        print("🚀 Your system is ready for GPU-accelerated training!")
        print("   Training will be 5-10x faster than CPU!\n")
    else:
        print("💡 Training will use CPU (slower but still works)\n")
    
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
