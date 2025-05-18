"""
Project Management Agent
This is the main entry point for the Project Management Agent.
It defines the workflow graph, state, tools, nodes and edges that allow the agent
to interact with ClickUp for project management tasks.
"""

from typing_extensions import Literal
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from langgraph.prebuilt import ToolNode
from copilotkit import CopilotKitState
from dotenv import load_dotenv
import json
import os
# Import checkpointer for conversation state persistence
from langgraph.checkpoint.memory import MemorySaver
# Import the ClickUp service for project management API interactions
from server.clickup_service import ClickUpService

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_KEY")

class AgentState(CopilotKitState):
    """
    Defines the state of the Project Management Agent
    
    This state tracks the conversation history and project management data
    such as ClickUp spaces, lists, and tasks.
    
    Inherits from CopilotKitState to leverage built-in conversation
    management capabilities.
    """
    proverbs: list[str]
    spaces: list[str]  # Stores ClickUp workspace spaces
    lists: list[str]   # Stores ClickUp lists within spaces
    tasks: list[str]   # Stores ClickUp tasks within lists
    # your_custom_agent_state: str = ""

@tool
def get_clickup_spaces():
    """
    Get all workspace spaces from ClickUp.
    
    Returns:
        A list of all spaces available in the user's ClickUp workspace.
    """
    
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Get all spaces for the team
    spaces = clickup.get_spaces()
    return spaces

@tool
def get_clickup_lists(space_id: str):
    """
    Get all lists for a specific ClickUp space.
    
    Args:
        space_id: The ID of the ClickUp space
        
    Returns:
        All lists in the specified space, which can contain tasks.
    """
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Get all lists for the space
    lists = clickup.get_lists(space_id)
    return lists

@tool
def get_clickup_tasks(list_id: str):
    """
    Get all tasks for a specific ClickUp list.
    
    Args:
        list_id: The ID of the ClickUp list
        
    Returns:
        All tasks in the specified list, representing individual work items.
    """
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Get all tasks for the list
    tasks = clickup.get_tasks(list_id)
    return tasks

@tool
def create_clickup_task(
    list_id: str,
    name: str,
    description: Optional[str] = None,
    due_date: Optional[int] = None,
    priority: Optional[int] = None,
    due_date_time: Optional[bool] = False,
    time_estimate: Optional[int] = None,
    start_date: Optional[int] = None,
    start_date_time: Optional[bool] = False,
    assignees: Optional[str] = None,
    tags: Optional[str] = None,
    status: Optional[str] = None,
):
    """
    Create a new project task in a specific ClickUp list.
    
    Args:
        list_id: The ID of the ClickUp list
        name: The name of the task
        description: The description of the task
        due_date: The due date as unix timestamp (in milliseconds)
        priority: The priority of the task (1=urgent, 2=high, 3=normal, 4=low)
        due_date_time: Whether the due date includes time
        time_estimate: The time estimate in milliseconds
        start_date: The start date as unix timestamp (in milliseconds)
        start_date_time: Whether the start date includes time
        assignees: JSON string of assignee user IDs (e.g., "[123, 456]")
        tags: JSON string of tags (e.g., '["tag1", "tag2"]')
        status: The status of the task
        
    Returns:
        The details of the created project task.
    """
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Parse assignees and tags if provided
    assignees_list = json.loads(assignees) if assignees else None
    tags_list = json.loads(tags) if tags else None
    
    # Create the task
    task = clickup.create_task(
        list_id=list_id,
        name=name,
        description=description,
        due_date=due_date,
        priority=priority,
        due_date_time=False if due_date_time is None else due_date_time,
        time_estimate=time_estimate,
        start_date=start_date,
        start_date_time=False if start_date_time is None else start_date_time,
        assignees=assignees_list,
        tags=tags_list,
        status=status
    )
    
    return task

@tool
def update_clickup_task(
    task_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[int] = None,
    due_date: Optional[int] = None,
    due_date_time: Optional[bool] = None,
    time_estimate: Optional[int] = None,
    start_date: Optional[int] = None,
    start_date_time: Optional[bool] = None,
    assignees: Optional[str] = None,
    archived: Optional[bool] = None,
):
    """
    Update an existing project task in ClickUp.
    
    Args:
        task_id: The ID of the task to update
        name: New name for the task
        description: New description for the task
        status: New status for the task
        priority: New priority (1=urgent, 2=high, 3=normal, 4=low)
        due_date: New due date as unix timestamp (in milliseconds)
        due_date_time: Whether the due date includes time
        time_estimate: New time estimate in milliseconds
        start_date: New start date as unix timestamp (in milliseconds)
        start_date_time: Whether the start date includes time
        assignees: JSON string of assignee user IDs (e.g., "[123, 456]")
        archived: Whether the task is archived
        
    Returns:
        The details of the updated project task.
    """
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Parse assignees if provided
    assignees_list = json.loads(assignees) if assignees else None
    
    # Update the task
    task = clickup.update_task(
        task_id=task_id,
        name=name,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
        due_date_time=None if due_date_time is None else due_date_time,
        time_estimate=time_estimate,
        start_date=start_date,
        start_date_time=None if start_date_time is None else start_date_time,
        assignees=assignees_list,
        archived=archived
    )
    
    return task

@tool
def delete_clickup_task(task_id: str):
    """
    Delete a project task from ClickUp.
    
    Args:
        task_id: The ID of the task to delete
        
    Returns:
        The response from the API confirming deletion.
    """
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Delete the task
    response = clickup.delete_task(task_id)
    
    return response

@tool
def get_clickup_task_by_id(task_id: str):
    """
    Get a specific project task by its ID from ClickUp.
    
    Args:
        task_id: The ID of the task
        
    Returns:
        The complete task details including status, assignees, and dates.
    """
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Get the task
    task = clickup.get_task_by_id(task_id)
    
    return task

@tool
def set_clickup_custom_field_value(task_id: str, field_id: str, value: str):
    """
    Set a value for a custom field on a ClickUp task.
    
    Args:
        task_id: The ID of the task
        field_id: The ID of the custom field
        value: The value to set for the custom field (as a string; will be converted to appropriate type)
        
    Returns:
        The response from the API confirming the update.
    """
    # Initialize the ClickUp service
    clickup = ClickUpService()
    
    # Try to parse the value as JSON, if it fails, use it as a string
    try:
        parsed_value = json.loads(value)
    except json.JSONDecodeError:
        parsed_value = value
        
    # Set the custom field value
    response = clickup.set_custom_field_value(
        task_id=task_id,
        field_id=field_id,
        value=parsed_value
    )
    
    return response

# Define the tools available to the Project Management Agent
tools = [
    get_clickup_spaces,
    get_clickup_lists,
    get_clickup_tasks,
    create_clickup_task,
    update_clickup_task,
    delete_clickup_task,
    get_clickup_task_by_id,
    set_clickup_custom_field_value,
]

async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:
    """
    Main chat processing node for the Project Management Agent.
    
    This node follows the ReAct design pattern to:
    1. Process user input using an LLM (Gemini)
    2. Decide whether to call project management tools
    3. Return responses to the user
    
    Args:
        state: The current agent state containing conversation history
        config: The runnable configuration
        
    Returns:
        Command indicating the next node to execute
    """
    
    # 1. Define the model for project management interactions
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY
    )

    # 2. Bind the ClickUp tools and CopilotKit actions to the model
    model_with_tools = model.bind_tools(
        [
            *state["copilotkit"]["actions"],
            get_clickup_spaces,
            get_clickup_lists,
            get_clickup_tasks,
            create_clickup_task,
            update_clickup_task,
            delete_clickup_task,
            get_clickup_task_by_id,
            set_clickup_custom_field_value
        ],
    )

    # 3. Define the system message instructing the agent on project management
    system_message = SystemMessage(
        content=f"You are a helpful project management assistant capable of managing tasks in ClickUp. Talk in {state.get('language', 'english')}."
    )

    # 4. Generate a response based on conversation history
    response = await model_with_tools.ainvoke([
        system_message,
        *state["messages"],
    ], config)

    # 5. Check for tool calls in the response and handle them
    if isinstance(response, AIMessage) and response.tool_calls:
        actions = state["copilotkit"]["actions"]

        # 5.1 Route to tool node when needed for project management actions
        if not any(
            action.get("name") == response.tool_calls[0].get("name")
            for action in actions
        ):
            return Command(goto="tool_node", update={"messages": response})

    # 6. End the conversation turn when no tools need to be called
    return Command(
        goto="__end__",
        update={
            "messages": response
        }
    )

# Define the workflow graph for the Project Management Agent
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", ToolNode(tools=tools))
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

# Create a memory checkpointer to maintain conversation state
memory_checkpointer = MemorySaver()

# Compile the workflow graph with the checkpointer
graph = workflow.compile(checkpointer=memory_checkpointer)