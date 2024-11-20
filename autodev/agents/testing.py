from typing import Dict, Any
import logging
import os
from ..core.agent import Agent
from ..core.types import Result
from ..prompts.agent_prompts import get_prompt
from ..services.llm_service import call_llm

logger = logging.getLogger(__name__)

def test_tasks(context_variables: Dict[str, Any]) -> Result:
    implemented_tasks = context_variables.get("implemented_tasks", [])
    project_dir = context_variables.get('project_dir', os.path.join(os.getcwd(), 'output', 'project'))
    logger.info(f"Starting testing of {len(implemented_tasks)} tasks.")
    tested_tasks = []
    for task in implemented_tasks:
        logger.info(f"Testing task {task['task_id']}: {task['description']}")
        prompt = f"""
{get_prompt('testing_agent')}

Code:
\"\"\"{task['code']}\"\"\"

Instructions:
- Write unit tests for the provided code.
- Return the tests as code.
- Do not include any comments or extra text.
- Do not include any lines starting with '#' or '//'.
- Ensure the tests cover all functionalities.

"""
        tests = call_llm(prompt)
        # Remove code block markers if present
        tests_clean = tests.strip()
        if tests_clean.startswith("```") and tests_clean.endswith("```"):
            tests_clean = "\n".join(tests_clean.strip("```").split("\n")[1:])
            tests_clean = tests_clean.strip()
        logger.debug(f"Generated tests for task {task['task_id']}:\n{tests_clean}")
        tested_tasks.append({
            "task_id": task["task_id"],
            "description": task["description"],
            "code": task["code"],
            "tests": tests_clean
        })

        # Save the tests to a file
        test_file_name = f"test_task_{task['task_id']}.py"
        test_file_path = os.path.join(project_dir, test_file_name)
        with open(test_file_path, 'w') as test_file:
            test_file.write(tests_clean)
        logger.info(f"Saved tests for task {task['task_id']} to {test_file_path}")

    logger.info("All tasks tested.")
    return Result(
        value="Tasks tested.",
        context_variables={"tested_tasks": tested_tasks},
        agent='IntegrationAgent'
    )

testing_agent = Agent(
    name="TestingAgent",
    instructions=get_prompt("testing_agent"),
    functions=[test_tasks]
)
