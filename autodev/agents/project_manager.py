# autodev/agents/project_manager.py

from typing import Dict, Any
from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt

class ProjectManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ProjectManagerAgent",
            instructions=get_prompt("project_manager_agent"),
            functions=[self.manage_project],
        )

    def manage_project(self, context_variables: Dict[str, Any]) -> Result:
        tasks = context_variables.get("tasks", [])
        if not tasks:
            return Result(
                value="Decomposing project into initial tasks.",
                agent="TaskDecomposerAgent"
            )
        elif "architecture" not in context_variables:
            return Result(
                value="Defining solution architecture and refining tasks.",
                agent="SolutionArchitectAgent",
            )
        else:
            return Result(
                value="Assigning tasks to DeveloperAgent.",
                agent="DeveloperAgent",
                context_variables=context_variables,
            )
