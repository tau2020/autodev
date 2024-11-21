# main.py

import os
import sys
import logging
from dotenv import load_dotenv
from typing import Dict, Any

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from autodev.core.swarm import Swarm
from autodev.agents.user_interface import UserInterfaceAgent
from autodev.agents.project_manager import ProjectManagerAgent
from autodev.agents.task_decomposer import TaskDecomposerAgent
from autodev.agents.solution_architect import SolutionArchitectAgent
from autodev.agents.developer import DeveloperAgent
from autodev.agents.testing import TestingAgent
from autodev.agents.integration import IntegrationAgent
from autodev.agents.deployment import DeploymentAgent

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Define the output directory
OUTPUT_DIR = os.path.join(os.getcwd(), "output")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Map agent names to agent instances
agent_map = {
    "UserInterfaceAgent": UserInterfaceAgent(),
    "ProjectManagerAgent": ProjectManagerAgent(),
    "TaskDecomposerAgent": TaskDecomposerAgent(),
    "SolutionArchitectAgent": SolutionArchitectAgent(),
    "DeveloperAgent": DeveloperAgent(),
    "TestingAgent": TestingAgent(),
    "IntegrationAgent": IntegrationAgent(),
    "DeploymentAgent": DeploymentAgent(),
}

def run_system():
    try:
        swarm = Swarm(agents=agent_map)
        context_variables: Dict[str, Any] = {"output_dir": OUTPUT_DIR}
        current_agent_name = "UserInterfaceAgent"

        for _ in range(20):
            logger.info(f"Current agent: {current_agent_name}")
            response = swarm.run(
                agent_name=current_agent_name,
                context_variables=context_variables,
            )
            context_variables = response.context_variables
            next_agent_name = response.agent

            logger.info(f"Next agent: {next_agent_name}")
            if not next_agent_name or next_agent_name not in agent_map:
                logger.info("Workflow complete or unknown agent encountered.")
                break

            current_agent_name = next_agent_name
        else:
            logger.info("Maximum number of iterations reached.")

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_system()
