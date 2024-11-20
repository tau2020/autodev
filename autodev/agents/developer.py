# autodev/agents/developer.py

from typing import Dict, Any
import logging
import os
from ..core.agent import Agent
from ..core.types import Result
from ..prompts.agent_prompts import get_prompt
from ..services.llm_service import call_llm

logger = logging.getLogger(__name__)

def implement_tasks(context_variables: Dict[str, Any]) -> Result:
    tasks = context_variables.get("tasks", [])
    output_dir = context_variables.get("output_dir", os.path.join(os.getcwd(), 'output'))
    project_name = context_variables.get("project_name", "project")

    # Create a directory for the project
    project_dir = os.path.join(output_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)

    logger.info(f"Starting implementation of {len(tasks)} tasks.")
    implemented_tasks = []
    for task in tasks:
        logger.info(f"Implementing task {task['task_id']}: {task['description']}")
        prompt = f"""
{get_prompt('developer_agent')}

Task Description:
\"\"\"{task['description']}\"\"\"

Instructions:
- Write code to implement the task.
- Include documentation as docstrings within the code.
- **Do not** include any comments, explanations, or code block markers like ```.
- Return only the code.

"""
        code = call_llm(prompt)
        # Remove any code block markers or extra text
        code_clean = code.strip()
        if code_clean.startswith("```") and code_clean.endswith("```"):
            code_clean = "\n".join(code_clean.strip("```").split("\n")[1:])
            code_clean = code_clean.strip()
        logger.debug(f"Generated code for task {task['task_id']}:\n{code_clean}")
        implemented_tasks.append({
            "task_id": task["task_id"],
            "description": task["description"],
            "code": code_clean
        })

        # Save the code to a file
        file_name = f"task_{task['task_id']}.py"
        file_path = os.path.join(project_dir, file_name)
        with open(file_path, 'w') as code_file:
            code_file.write(code_clean)
        logger.info(f"Saved code for task {task['task_id']} to {file_path}")

    logger.info("All tasks implemented.")
    context_variables['project_dir'] = project_dir
    return Result(
        value="Tasks implemented.",
        context_variables={"implemented_tasks": implemented_tasks, "project_dir": project_dir},
        agent='TestingAgent'
    )

developer_agent = Agent(
    name="DeveloperAgent",
    instructions=get_prompt("developer_agent"),
    functions=[implement_tasks]
)
