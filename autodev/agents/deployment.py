# autodev/agents/deployment.py

from typing import Dict, Any
import logging
import os

from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt

logger = logging.getLogger(__name__)

class DeploymentAgent(Agent):
    def __init__(self):
        super().__init__(
            name="DeploymentAgent",
            instructions=get_prompt("deployment_agent"),
            functions=[self.deploy_application],
        )

    def deploy_application(self, context_variables: Dict[str, Any]) -> Result:
        project_dir = context_variables.get(
            "project_dir", os.path.join(os.getcwd(), "output", "project")
        )

        logger.info("Deployment agent is skipping GitHub deployment for local assessment.")
        logger.info(f"The project is available at: {project_dir}")

        # Optionally, you can print a summary or next steps
        return Result(
            value=f"Application ready for deployment. Project files are saved at {project_dir}",
            agent=None,
        )
