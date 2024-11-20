from typing import Dict, Any
from ..core.agent import Agent
from ..core.types import Result
from ..prompts.agent_prompts import get_prompt

def capture_user_input(context_variables: Dict[str, Any]) -> Result:
    project_description = input("Enter the project description: ")
    project_name = input("Enter the project name (for GitHub repository): ")
    return Result(
        value="Project description and name captured.",
        context_variables={
            "project_description": project_description,
            "project_name": project_name
        },
        agent='ProjectManagerAgent'
    )

user_interface_agent = Agent(
    name="UserInterfaceAgent",
    instructions=get_prompt("user_interface_agent"),
    functions=[capture_user_input]
)
