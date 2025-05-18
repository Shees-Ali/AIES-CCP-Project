# setup.ps1
# PowerShell script to set up Python venv environment

# Creates a virtual environment if it doesn't exist
if (-not (Test-Path .\venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
Write-Host "To activate the environment manually, run: .\venv\Scripts\Activate.ps1"
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Install the project in development mode
Write-Host "Installing project in development mode..."
pip install -e .

Write-Host "Setup complete!"
Write-Host "You can now run the demo with: python -m sample_agent.demo"
