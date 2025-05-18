"""
ClickUp API Service for Project Manager Agent

This module provides a service class for interacting with the ClickUp API.
It includes methods for retrieving spaces, lists, tasks, and creating tasks.
"""

import os
import requests
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClickUpService:
    """
    A service class for interacting with the ClickUp API.
    
    This class provides methods to interact with ClickUp's API, such as
    retrieving spaces, lists, tasks, and creating tasks.
    """
    
    BASE_URL = "https://api.clickup.com/api/v2"
    
    def __init__(self):
        """
        Initialize the ClickUp service with API key and team ID from environment variables.
        """
        self.api_key = os.getenv("CLICKUP_API_KEY")
        self.team_id = os.getenv("CLICKUP_TEAM_ID")
        
        if not self.api_key:
            raise ValueError("CLICKUP_API_KEY environment variable not set")
        if not self.team_id:
            raise ValueError("CLICKUP_TEAM_ID environment variable not set")
        
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get_spaces(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all spaces for the team.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary containing a list of spaces
        
        Example response:
        {
            "spaces": [
                {
                    "id": "90183095898",
                    "name": "Blueprint Manager (AI Architecture Project Management)",
                    ...
                }
            ]
        }
        """
        url = f"{self.BASE_URL}/team/{self.team_id}/space"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    
    def get_lists(self, space_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all lists for a specific space.
        
        Args:
            space_id (str): The ID of the space
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary containing a list of lists
            
        Example response:
        {
            "lists": [
                {
                    "id": "901805707059",
                    "name": "Tasks List",
                    ...
                }
            ]
        }
        """
        url = f"{self.BASE_URL}/space/{space_id}/list"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_tasks(self, list_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all tasks for a specific list.
        
        Args:
            list_id (str): The ID of the list
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary containing a list of tasks and last_page boolean
            
        Example response:
        {
            "tasks": [
                {
                    "id": "86et5jp8a",
                    "name": "Firm Registration and Firm Management",
                    ...
                }
            ],
            "last_page": true
        }
        """
        url = f"{self.BASE_URL}/list/{list_id}/task"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_task(
        self, 
        list_id: str, 
        name: str, 
        description: Optional[str] = None,
        due_date: Optional[int] = None,
        priority: Optional[int] = None,
        due_date_time: bool = False,
        time_estimate: Optional[int] = None,
        start_date: Optional[int] = None,
        start_date_time: bool = False,
        assignees: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        status: Optional[str] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a new task in a specific list.
        
        Args:
            list_id (str): The ID of the list
            name (str): The name of the task
            description (Optional[str], optional): The description of the task. Defaults to None.
            due_date (Optional[int], optional): The due date as unix timestamp. Defaults to None.
            priority (Optional[int], optional): The priority of the task (1=urgent, 2=high, 3=normal, 4=low). Defaults to None.
            due_date_time (bool, optional): Whether the due date includes time. Defaults to False.
            time_estimate (Optional[int], optional): The time estimate in milliseconds. Defaults to None.
            start_date (Optional[int], optional): The start date as unix timestamp. Defaults to None.
            start_date_time (bool, optional): Whether the start date includes time. Defaults to False.
            assignees (Optional[List[int]], optional): List of assignee user IDs. Defaults to None.
            tags (Optional[List[str]], optional): List of tags. Defaults to None.
            status (Optional[str], optional): The status of the task. Defaults to None.
            custom_fields (Optional[List[Dict[str, Any]]], optional): List of custom fields. Defaults to None.
            
        Returns:
            Dict[str, Any]: The created task object
            
        Example response:
        {
            "id": "86etgdukw",
            "name": "Test",
            "description": "testing task creation",
            ...
        }
        """
        url = f"{self.BASE_URL}/list/{list_id}/task"
        
        data = {
            "name": name,
            "due_date_time": due_date_time,
            "start_date_time": start_date_time
        }
        
        # Add optional parameters if they are provided
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date
        if priority:
            data["priority"] = priority
        if time_estimate:
            data["time_estimate"] = time_estimate
        if start_date:
            data["start_date"] = start_date
        if assignees:
            data["assignees"] = assignees
        if tags:
            data["tags"] = tags
        if status:
            data["status"] = status
        if custom_fields:
            data["custom_fields"] = custom_fields
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def update_task(
        self,
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
        assignees: Optional[List[int]] = None,
        archived: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update an existing task.
        
        Args:
            task_id (str): The ID of the task to update
            name (Optional[str], optional): New name for the task. Defaults to None.
            description (Optional[str], optional): New description for the task. Defaults to None.
            status (Optional[str], optional): New status for the task. Defaults to None.
            priority (Optional[int], optional): New priority (1=urgent, 2=high, 3=normal, 4=low). Defaults to None.
            due_date (Optional[int], optional): New due date as unix timestamp. Defaults to None.
            due_date_time (Optional[bool], optional): Whether the due date includes time. Defaults to None.
            time_estimate (Optional[int], optional): New time estimate in milliseconds. Defaults to None.
            start_date (Optional[int], optional): New start date as unix timestamp. Defaults to None.
            start_date_time (Optional[bool], optional): Whether the start date includes time. Defaults to None.
            assignees (Optional[List[int]], optional): New list of assignee user IDs. Defaults to None.
            archived (Optional[bool], optional): Whether the task is archived. Defaults to None.
            
        Returns:
            Dict[str, Any]: The updated task object
        """
        url = f"{self.BASE_URL}/task/{task_id}"
        
        data = {}
        
        # Add optional parameters if they are provided
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if status:
            data["status"] = status
        if priority is not None:
            data["priority"] = priority
        if due_date is not None:
            data["due_date"] = due_date
        if due_date_time is not None:
            data["due_date_time"] = due_date_time
        if time_estimate is not None:
            data["time_estimate"] = time_estimate
        if start_date is not None:
            data["start_date"] = start_date
        if start_date_time is not None:
            data["start_date_time"] = start_date_time
        if assignees is not None:
            data["assignees"] = assignees
        if archived is not None:
            data["archived"] = archived
        
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        Delete a task.
        
        Args:
            task_id (str): The ID of the task to delete
            
        Returns:
            Dict[str, Any]: The response from the API
        """
        url = f"{self.BASE_URL}/task/{task_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_task_by_id(self, task_id: str) -> Dict[str, Any]:
        """
        Get a task by its ID.
        
        Args:
            task_id (str): The ID of the task
            
        Returns:
            Dict[str, Any]: The task object
        """
        url = f"{self.BASE_URL}/task/{task_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def set_custom_field_value(
        self,
        task_id: str,
        field_id: str,
        value: Any
    ) -> Dict[str, Any]:
        """
        Set a value for a custom field on a task.
        
        Args:
            task_id (str): The ID of the task
            field_id (str): The ID of the custom field
            value (Any): The value to set for the custom field
            
        Returns:
            Dict[str, Any]: The response from the API
        """
        url = f"{self.BASE_URL}/task/{task_id}/field/{field_id}"
        
        data = {
            "value": value
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
