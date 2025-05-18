# Project Manager Agent

This is a Project Manager Agent project built with LangGraph and LangChain.

## Setup Instructions

### Prerequisites
- Python 3.10 or higher (recommended Python 3.12 as specified in langgraph.json)
- Git

### Setting Up the Project

#### 1. Clone the repository
```bash
git clone [repository-url]
cd agent-py
```

#### 2. Create and activate a virtual environment

**On Windows (PowerShell)**:
```powershell
# Run the setup script which creates venv, installs dependencies, and sets up the project
.\setup.ps1
```

**On Windows (CMD)**:
```cmd
# Run the setup script
setup.bat
```

**Manually**:
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the project in development mode
pip install -e .
```

#### 3. Set up environment variables
Create a `.env` file in the project root and add your API keys:
```
GEMINI_KEY=your_gemini_api_key
```

## Running the Project

After activating the virtual environment:
```bash
# Run the demo server
uvicorn project_manager_agent.demo:app
```

The server will start on http://0.0.0.0:8000 with hot reload enabled.

## Project Structure

- `project_manager_agent/agent.py`: Main agent code with graph, state, tools, and nodes definition
- `project_manager_agent/demo.py`: FastAPI server that hosts the agent
- `requirements.txt`: Project dependencies
