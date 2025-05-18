@echo off
REM setup.bat - Setup script for Windows CMD

REM Creates a virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
echo Activating virtual environment...
echo To activate the environment manually, run: .\venv\Scripts\activate.bat
call .\venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install the project in development mode
echo Installing project in development mode...
pip install -e .

echo Setup complete!
echo You can now run the demo with: python -m project_manager_agent.demo
