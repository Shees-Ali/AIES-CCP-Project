# ClickUp API Service

This service provides a Python interface for interacting with the ClickUp API. It includes methods for retrieving spaces, lists, tasks, and creating tasks.

## Setup

1. Ensure you have the required dependencies:
   ```
   pip install requests python-dotenv
   ```

2. Create a `.env` file in the root of your project with your ClickUp API key and team ID:
   ```
   CLICKUP_API_KEY=your_api_key_here
   CLICKUP_TEAM_ID=your_team_id_here
   ```

## Usage

### Initializing the Service

```python
from server.clickup_service import ClickUpService

# Initialize the ClickUp service
clickup = ClickUpService()
```

### Getting Spaces

```python
# Get all spaces for the team
spaces = clickup.get_spaces()
```

### Getting Lists

```python
# Get all lists for a specific space
space_id = "90183095898"  # Replace with your space ID
lists = clickup.get_lists(space_id)
```

### Getting Tasks

```python
# Get all tasks for a specific list
list_id = "901805707059"  # Replace with your list ID
tasks = clickup.get_tasks(list_id)
```

### Creating a Task

```python
# Create a new task
new_task = clickup.create_task(
    list_id="901805707059",  # Replace with your list ID
    name="Example Task",
    description="This is an example task created via the API",
    priority=3,  # Normal priority
    due_date=1508369194377,  # Unix timestamp in milliseconds
    start_date=1567780450202,  # Unix timestamp in milliseconds
    time_estimate=8640000  # Time estimate in milliseconds
)
```

### Updating a Task

```python
# Update a task
updated_task = clickup.update_task(
    task_id="86etgdukw",  # Replace with your task ID
    name="Updated Task Name",
    description="Updated description",
    priority=2,  # High priority
)
```

### Deleting a Task

```python
# Delete a task
response = clickup.delete_task("86etgdukw")  # Replace with your task ID
```

### Getting a Task by ID

```python
# Get a task by ID
task = clickup.get_task_by_id("86etgdukw")  # Replace with your task ID
```

### Setting a Custom Field Value

```python
# Set a custom field value
response = clickup.set_custom_field_value(
    task_id="86etgdukw",  # Replace with your task ID
    field_id="dab7f3ca-328b-4519-9698-c0275158ff8d",  # Replace with your field ID
    value="some value"  # The value to set
)
```

## Example

See the `examples/clickup_example.py` file for a complete example of how to use this service.
