# autodev/agents/user_interface.py

from typing import Dict, Any
from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt

class UserInterfaceAgent(Agent):
    def __init__(self):
        super().__init__(
            name="UserInterfaceAgent",
            instructions=get_prompt("user_interface_agent"),
            functions=[self.get_user_input],
        )

    def get_user_input(self, context_variables: Dict[str, Any]) -> Result:
        project_description = input("Enter the project description: ")
        project_name = input("Enter the project name (for GitHub repository): ")
        context_variables["project_description"] = project_description
        context_variables["project_name"] = project_name
        return Result(
            value="Project description and name received.",
            context_variables=context_variables,
            agent="ProjectManagerAgent",
        )
