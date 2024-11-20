from typing import Dict, Any
import logging
import os
from ..core.agent import Agent
from ..core.types import Result
from ..prompts.agent_prompts import get_prompt

logger = logging.getLogger(__name__)

def integrate_tasks(context_variables: Dict[str, Any]) -> Result:
    tested_tasks = context_variables.get("tested_tasks", [])
    project_dir = context_variables.get('project_dir', os.path.join(os.getcwd(), 'output', 'project'))
    integrated_code = ""

    logger.info("Integrating tested tasks.")
    for task in tested_tasks:
        integrated_code += f"\n# Task {task['task_id']}: {task['description']}\n"
        integrated_code += task['code']
        integrated_code += "\n# Tests\n"
        integrated_code += task['tests']
    
    # Save the integrated code to a file
    integrated_file_path = os.path.join(project_dir, 'integrated_code.py')
    with open(integrated_file_path, 'w') as integrated_file:
        integrated_file.write(integrated_code)
    logger.info(f"Integrated code saved to {integrated_file_path}")

    context_variables['integrated_code'] = integrated_code
    context_variables['integrated_file_path'] = integrated_file_path
    return Result(
        value="Tasks integrated.",
        context_variables=context_variables,
        agent='DeploymentAgent'
    )

integration_agent = Agent(
    name="IntegrationAgent",
    instructions=get_prompt("integration_agent"),
    functions=[integrate_tasks]
)
