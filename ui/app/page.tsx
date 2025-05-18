"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";
import { ClickupSpace, Space } from "./types/ClickupSpace";

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
};

function YourMainContent({ themeColor }: { themeColor: string }) {
  // 🪁 Shared State: https://docs.copilotkit.ai/coagents/shared-state
  const { state, setState } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState: {
      spaces: [],
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
        
        setState((prevState) => ({
          ...prevState,
          spaces: spacesArray || [],
        }));
      } catch (error) {
        console.error("Error processing spaces data:", error);
        console.log("Received data:", spaces);
      }
    },
  });

  return (
    <div
      style={{ backgroundColor: themeColor }}
      className="h-screen w-screen flex justify-center items-center flex-col transition-colors duration-300"
    >
      <div className="bg-white/20 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-white mb-2 text-center">
          Project Manager Agent
        </h1>
        <p className="text-gray-200 text-center italic mb-6">
          Your AI-powered project management assistant
        </p>
        <hr className="border-white/20 my-6" />
        <div className="flex flex-col gap-3">
          {state.spaces?.map((space, index) => (
            <div
              key={index}
              className="bg-white/15 p-4 rounded-xl text-white relative group hover:bg-white/20 transition-all"
            >
              <p className="pr-8">{space.name + " - " + "ID: " + space.id}</p>
            </div>
          ))}
        </div>
        {state.spaces?.length === 0 && (
          <p className="text-center text-white/80 italic my-8">
            No spaces yet. Ask the assistant to add some!
          </p>
        )}
      </div>
    </div>
  );
}
