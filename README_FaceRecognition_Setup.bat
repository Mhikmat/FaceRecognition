@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
title FaceRecognition Setup Wizard

:: Clear screen
cls
echo ============================================
echo  FaceRecognition Setup Wizard - Let's Go!
echo ============================================
echo.
echo Make sure you've done the following:
echo - Installed Python 3.9 or higher
echo - Downloaded or cloned this project
echo - Placed this script inside the "FaceRecognition" folder
echo.
pause

:: STEP 1: Check Python
echo Checking if Python is installed...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python is not installed or not added to PATH.
    echo Please install Python 3.9+ and try again.
    pause
    exit /b
)
echo Python detected!
echo.
pause

:: STEP 2: Make virtual environment
echo Step 1: Making virtual environment...
python -m venv FaceRecognitionEnv
echo Virtual environment made: FaceRecognitionEnv
echo.
pause

:: STEP 3: Activate the environment
echo Step 2: Activating environment...
call FaceRecognitionEnv\Scripts\activate
echo Environment activated.
echo.
pause

:: STEP 4: Upgrade pip
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo pip upgraded.
echo.
pause

:: STEP 5: Install required packages
echo Step 4: Installing required packages...
pip install ipykernel jupyterlab
pip install tensorflow opencv-python matplotlib numpy
echo All packages installed successfully.
echo.
pause

:: STEP 6: Register Jupyter kernel
echo Step 5: Registering kernel with Jupyter...
python -m ipykernel install --name=FaceRecognitionEnv
echo Kernel registered.
echo.
pause

:: STEP 7: Launch Jupyter Lab
echo Step 6: Launching Jupyter Lab...
echo When Jupyter opens in your browser:
echo - Open "updated_facial_verification.ipynb"
echo - Press Shift + Enter to run each cell
echo.
jupyter lab
