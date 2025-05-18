# Project Management Co-Agent

This project provides an AI-powered project management assistant that integrates with ClickUp to help manage tasks, lists, and workspaces. It demonstrates building an intelligent agent system with LangGraph that can interface with external APIs.

## Project Overview

The project consists of two main components:
- **Python Agent**: A LangGraph-powered agent that interfaces with the ClickUp API
- **Next.js UI**: A modern web interface built with React and CopilotKit

The agent can perform various project management tasks including:
- Retrieving and displaying ClickUp spaces and lists
- Creating, updating, and deleting tasks
- Setting custom field values
- Managing project timelines and assignees

## Tech Stack

### Backend (Python Agent)
- LangGraph/LangChain for agent orchestration
- Google Gemini for AI processing (primary LLM)
- FastAPI for API endpoints
- CopilotKit for agent integration

### Frontend (Next.js UI)
- Next.js for the React framework
- CopilotKit UI components
- TypeScript for type safety
- TailwindCSS for styling

## Setup Instructions

### Environment Requirements
- Python 3.10+ (Python 3.12 recommended)
- Node.js and pnpm for the UI

### Python Agent Setup

1. Navigate to the agent directory:
```sh
cd agent-py
```

2. Create a virtual environment:
```sh
# Using PowerShell
.\setup.ps1

# Or using CMD
setup.bat
```

Alternatively, you can set up manually:
```sh
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
pip install -e .
```

3. Create a `.env` file in the `agent-py` directory with:
```
OPENAI_API_KEY=...  # For OpenAI LLM (optional)
GEMINI_KEY=...      # For Google Gemini LLM (required)
CLICKUP_API_KEY=... # Your ClickUp API key
CLICKUP_TEAM_ID=... # Your ClickUp Team ID
```

4. Run the demo:
```sh
uvicorn project_manager_agent.demo:app
```

### UI Setup

1. Navigate to the UI directory:
```sh
cd ui
```

2. Install dependencies:
```sh
pnpm i
```

3. Create a `.env` file inside `./ui` with:
```
OPENAI_API_KEY=...  # Required for CopilotKit
```

4. Start the development server:
```sh
pnpm run dev
```

## Usage

1. Start both the agent server and the UI server
2. Navigate to [http://localhost:3000](http://localhost:3000)
3. Interact with the Project Management Assistant through the sidebar

You can ask the agent to:
- Show your ClickUp spaces
- Create new tasks
- Update existing tasks
- Check project timelines
- And more...

## LangGraph Studio Integration

For development and debugging, you can use LangGraph studio:

1. Run LangGraph studio
2. Load the `./agent-py` folder into it
3. Ensure your `.env` file is properly configured

## Troubleshooting

Common issues:
1. Make sure no other application is running on port 8000
2. If you have connectivity issues, try changing the host in `project_manager_agent/demo.py` from `0.0.0.0` to `127.0.0.1` or `localhost`
3. Ensure all required API keys are set in your `.env` files
4. Check that your ClickUp API key has the necessary permissions
