@echo off
REM GPU Setup Script for Campus Memory ML Training
REM Installs PyTorch with CUDA 12.1 support for NVIDIA GPUs

echo ========================================
echo GPU SETUP FOR ML TRAINING
echo ========================================
echo.
echo Your GPU: NVIDIA GeForce RTX 3050 6GB
echo CUDA Version: 12.6
echo.
echo This will install:
echo - PyTorch 2.5+ with CUDA 12.1 support (~2.4 GB download)
echo - Transformers library
echo - Additional ML dependencies
echo.
echo Download size: ~2.4 GB
echo Installation time: ~10-15 minutes
echo.
pause

echo.
echo ========================================
echo STEP 1: Installing PyTorch with GPU
echo ========================================
echo.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: PyTorch installation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 2: Installing Transformers
echo ========================================
echo.
pip install transformers accelerate

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Transformers installation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 3: Verifying GPU Setup
echo ========================================
echo.
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not detected')"

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo You can now train models with GPU acceleration:
echo   python train_models_gpu.py
echo.
echo Expected training time with GPU:
echo   - Category Classifier: ~5-8 minutes
echo   - School Classifier: ~5-8 minutes
echo   - Total: ~10-15 minutes (vs 30-60 minutes on CPU)
echo.
pause
