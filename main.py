import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any
from autodev.core.swarm import Swarm
from autodev.agents import (
    user_interface_agent,
    project_manager_agent,
    task_decomposer_agent,
    developer_agent,
    testing_agent,
    integration_agent,
    deployment_agent,
    solution_architect_agent
)

# Load environment variables
load_dotenv()

# LLM Configuration and other settings...
# (No changes needed here)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# Define the output directory
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Map agent names to agent instances
agent_map = {
    'UserInterfaceAgent': user_interface_agent,
    'ProjectManagerAgent': project_manager_agent,
    'TaskDecomposerAgent': task_decomposer_agent,
    'SolutionArchitectAgent': solution_architect_agent,  # New agent
    'DeveloperAgent': developer_agent,
    'TestingAgent': testing_agent,
    'IntegrationAgent': integration_agent,
    'DeploymentAgent': deployment_agent
}
def run_system():
    try:
        client = Swarm()
        context_variables: Dict[str, Any] = {'output_dir': OUTPUT_DIR}
        messages = []
        current_agent = user_interface_agent

        for _ in range(20):
            logger.info(f"Current agent: {current_agent.name}")
            response = client.run(
                agent=current_agent,
                messages=messages,
                context_variables=context_variables
            )
            messages = response.messages
            context_variables = response.context_variables
            next_agent_name = response.agent
            logger.info(f"Next agent: {next_agent_name}")
            if not next_agent_name or next_agent_name not in agent_map:
                logger.info("Workflow complete or unknown agent encountered.")
                break
            current_agent = agent_map[next_agent_name]
        else:
            logger.info("Maximum number of turns reached.")

        for message in messages:
            print(f"[{message['agent']}] {message['message']}")
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user.")

if __name__ == "__main__":
    run_system()
