# autodev/agents/integration.py

from typing import Dict, Any
import logging
import os
from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt
from autodev.services.git_manager import GitManagerService

logger = logging.getLogger(__name__)

class IntegrationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="IntegrationAgent",
            instructions=get_prompt("integration_agent"),
            functions=[self.integrate_tasks],
        )

    def integrate_tasks(self, context_variables: Dict[str, Any]) -> Result:
        tested_tasks = context_variables.get("tested_tasks", [])
        project_dir = context_variables.get(
            "project_dir", os.path.join(os.getcwd(), "output", "project")
        )

        git_manager = GitManagerService(repo_path=project_dir)
        # Pull latest changes
        git_manager.pull()

        logger.info("Integrating tested tasks.")
        # In this simplified example, assume that code is already integrated via Git commits
        # Additional integration steps can be added if necessary

        # Commit any integration changes
        git_manager.add(".")
        git_manager.commit("Integrated all tasks")

        # Push changes to remote (if remote is set)
        try:
            git_manager.push()
        except Exception as e:
            logger.error(f"Git push failed: {e}")

        logger.info("All tasks integrated.")
        return Result(
            value="Tasks integrated.",
            context_variables=context_variables,
            agent="DeploymentAgent",
        )
