"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";
import { ClickupSpace, Space } from "./types/ClickupSpace";
import { List } from "./types/ClickupList";
import { Task } from "./types/ClickupTask";

export default function CopilotKitPage() {
  const [themeColor, setThemeColor] = useState("#6366f1");

  // 🪁 Frontend Actions: https://docs.copilotkit.ai/guides/frontend-actions
  useCopilotAction({
    name: "setThemeColor",
    parameters: [
      {
        name: "themeColor",
        description: "The theme color to set. Make sure to pick nice colors.",
        required: true,
      },
    ],
    handler({ themeColor }) {
      setThemeColor(themeColor);
    },
  });

  return (
    <main
      className="overflow-x-hidden"
      style={
        { "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties
      }
    >
      <YourMainContent themeColor={themeColor} />
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Project Manager Assistant",
          initial:
            '👋 Hi there! I\'m your ClickUp Project Management assistant. I can help you manage your projects efficiently.\n\nTry asking me:\n- **Change Theme**: "Set the theme to blue"\n- **ClickUp Spaces**: "Show me my ClickUp spaces"\n- **Manage Tasks**: "Create a new task for the marketing campaign"\n\nAs we interact, you\'ll see the UI update in real-time to reflect your ClickUp data and changes.',
        }}
      />
    </main>
  );
}

// State of the agent, make sure this aligns with your agent's state.
type AgentState = {
  spaces: Space[];
  lists: List[];
  tasks: Task[];
};

function YourMainContent({ themeColor }: { themeColor: string }) {
  // 🪁 Shared State: https://docs.copilotkit.ai/coagents/shared-state
  const { state, setState } = useCoAgent<AgentState>({
    name: "project_manager_agent",
    initialState: {
      spaces: [],
      lists: [],
      tasks: [],
    },
  });

  useCopilotAction({
    name: "showSpacesFromClickUp",
    description:
      "Gets the spaces from the ClickUp API and then shows them on the UI.",
    parameters: [
      {
        name: "spaces",
        description: "spaces that are fetched from the clickup API",
        required: true,
        type: "string",
      },
    ],
    handler: ({ spaces }) => {
      console.log("Received spaces from clickUp:", spaces);
      // Replace Python boolean values with JavaScript boolean values
      try {
        // Check if spaces is a string or already an object
        let parsedSpaces;
        if (typeof spaces === 'string') {
          // Replace Python Boolean/None values with JavaScript equivalents
          const normalizedJson = spaces
            .replace(/False/g, 'false')
            .replace(/True/g, 'true')
            .replace(/None/g, 'null')
            .replace(/'/g, '"'); // Replace single quotes with double quotes
          
          parsedSpaces = JSON.parse(normalizedJson);
        } else {
          parsedSpaces = spaces;
        }
        
        // Handle both direct space array or nested object structure
        const spacesArray = Array.isArray(parsedSpaces) 
          ? parsedSpaces 
          : (parsedSpaces.spaces || parsedSpaces.get_clickup_spaces_response?.spaces);
        
        setState((prevState: AgentState | undefined) => ({
          spaces: spacesArray || [],
          lists: prevState?.lists || [],
          tasks: prevState?.tasks || [],
        }));
      } catch (error) {
        console.error("Error processing spaces data:", error);
        console.log("Received data:", spaces);
      }
    },
  });

  // Add action for fetching lists within a space
  useCopilotAction({
    name: "showListsFromClickUp",
    description:
      "Gets the lists for a specific space from the ClickUp API and then shows them on the UI.",
    parameters: [
      {
        name: "spaceId",
        description: "ID of the space to get lists for",
        required: true,
        type: "string",
      },
      {
        name: "lists",
        description: "lists that are fetched from the clickup API",
        required: true,
        type: "string",
      },
    ],
    handler: ({ spaceId, lists }) => {
      console.log(`Fetching lists for space: ${spaceId}`);
      console.log("Received lists from clickUp:", lists);
      
      try {
        // Check if lists is a string or already an object
        let parsedLists;
        if (typeof lists === 'string') {
          // Replace Python Boolean/None values with JavaScript equivalents
          const normalizedJson = lists
            .replace(/False/g, 'false')
            .replace(/True/g, 'true')
            .replace(/None/g, 'null')
            .replace(/'/g, '"'); // Replace single quotes with double quotes
          
          parsedLists = JSON.parse(normalizedJson);
        } else {
          parsedLists = lists;
        }
        
        // Handle both direct list array or nested object structure
        const listsArray = Array.isArray(parsedLists) 
          ? parsedLists 
          : (parsedLists.lists || parsedLists.get_clickup_lists_response?.lists);
        
        // Add space_id to each list if it doesn't exist already
        const listsWithSpaceId = (listsArray || []).map((list: any) => ({
          ...list,
          space_id: list.space_id || spaceId
        }));
        
        setState((prevState: AgentState | undefined) => ({
          lists: [
            ...(prevState?.lists || []).filter((list: List) => list.space_id !== spaceId),
            ...listsWithSpaceId
          ],
          spaces: prevState?.spaces || [],
          tasks: prevState?.tasks || [],
        }));
      } catch (error) {
        console.error("Error processing lists data:", error);
        console.log("Received data:", lists);
      }
    },
  });

  // Add action for fetching tasks within a list
  useCopilotAction({
    name: "showTasksFromClickUp",
    description:
      "Gets the tasks for a specific list from the ClickUp API and then shows them on the UI.",
    parameters: [
      {
        name: "listId",
        description: "ID of the list to get tasks for",
        required: true,
        type: "string",
      },
      {
        name: "tasks",
        description: "tasks that are fetched from the clickup API",
        required: true,
        type: "string",
      },
    ],
    handler: ({ listId, tasks }) => {
      console.log(`Fetching tasks for list: ${listId}`);
      console.log("Received tasks from clickUp:", tasks);
      
      try {
        // Check if tasks is a string or already an object
        let parsedTasks;
        if (typeof tasks === 'string') {
          // Replace Python Boolean/None values with JavaScript equivalents
          const normalizedJson = tasks
            .replace(/False/g, 'false')
            .replace(/True/g, 'true')
            .replace(/None/g, 'null')
            .replace(/'/g, '"'); // Replace single quotes with double quotes
          
          parsedTasks = JSON.parse(normalizedJson);
        } else {
          parsedTasks = tasks;
        }
        
        // Handle both direct task array or nested object structure
        const tasksArray = Array.isArray(parsedTasks) 
          ? parsedTasks 
          : (parsedTasks.tasks || parsedTasks.get_clickup_tasks_response?.tasks);
        
        // Add list_id to each task if it doesn't exist already
        const tasksWithListId = (tasksArray || []).map((task: any) => ({
          ...task,
          list_id: task.list_id || listId
        }));
        
        setState((prevState: AgentState | undefined) => ({
          tasks: [
            ...(prevState?.tasks || []).filter((task: Task) => task.list_id !== listId),
            ...tasksWithListId
          ],
          spaces: prevState?.spaces || [],
          lists: prevState?.lists || [],
        }));
      } catch (error) {
        console.error("Error processing tasks data:", error);
        console.log("Received data:", tasks);
      }
    },
  });

  return (
    <div
      style={{ backgroundColor: themeColor }}
      className="min-h-screen w-screen flex justify-center items-center flex-col transition-colors duration-300 py-8"
    >
      <div className="bg-white/20 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-4xl w-full my-4">
        <h1 className="text-4xl font-bold text-white mb-2 text-center">
          Project Manager Agent
        </h1>
        <p className="text-gray-200 text-center italic mb-6">
          Your AI-powered project management assistant
        </p>
        <hr className="border-white/20 my-6" />
        <div className="flex flex-col gap-3">
          {state.spaces?.map((space) => (
            <div
              key={`space-${space.id}`}
              className="bg-white/15 p-4 rounded-xl text-white relative group hover:bg-white/20 transition-all space-item"
            >
              {/* Space */}
              <p className="pr-8 font-semibold text-lg">{space.name + " - " + "ID: " + space.id}</p>
              
              {/* Lists for this space */}
              <div className="pl-4 mt-2">
                {state.lists
                  .filter(list => list.space_id === space.id)
                  .map((list) => (
                    <div
                      key={`list-${list.id}`}
                      className="bg-white/10 p-3 rounded-lg mt-2 text-white relative group hover:bg-white/15 transition-all list-item"
                    >
                      {/* List */}
                      <p className="pr-8 font-medium">{list.name + " - " + "ID: " + list.id}</p>
                      
                      {/* Tasks for this list */}
                      <div className="pl-4 mt-1">
                        {state.tasks
                          .filter(task => task.list_id === list.id)
                          .map((task) => (
                            <div
                              key={`task-${task.id}`}
                              className="bg-white/05 p-2 rounded-md mt-1 text-white/90 group hover:bg-white/10 transition-all task-item"
                            >
                              {/* Task */}
                                <p>{task.name} {task.id && <span className="text-white/60 text-xs">- ID: {task.id}</span>}</p>
                              {task.description && (
                                <p className="text-white/70 text-sm mt-1">{task.description}</p>
                              )}
                            </div>
                          ))}
                        
                        {state.tasks.filter(task => task.list_id === list.id).length === 0 && (
                          <p className="text-white/50 italic text-sm py-1">
                            No tasks yet. Ask the assistant to fetch tasks for this list!
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                
                {state.lists.filter(list => list.space_id === space.id).length === 0 && (
                  <p className="text-white/60 italic text-sm py-1">
                    No lists yet. Ask the assistant to fetch lists for this space!
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
        {state.spaces?.length === 0 && (
          <p className="text-center text-white/80 italic my-8">
            No spaces yet. Ask the assistant to fetch some!
          </p>
        )}
      </div>
    </div>
  );
}
