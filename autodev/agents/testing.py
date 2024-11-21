# autodev/agents/testing.py

from typing import Dict, Any
import logging
import os
from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt
from autodev.services.llm_service import call_llm
from autodev.services.git_manager import GitManagerService

logger = logging.getLogger(__name__)

class TestingAgent(Agent):
    def __init__(self):
        super().__init__(
            name="TestingAgent",
            instructions=get_prompt("testing_agent"),
            functions=[self.test_tasks],
        )

    def test_tasks(self, context_variables: Dict[str, Any]) -> Result:
        implemented_tasks = context_variables.get("implemented_tasks", [])
        programming_language = context_variables.get(
            "programming_language", "python"
        ).lower()
        project_dir = context_variables.get(
            "project_dir", os.path.join(os.getcwd(), "output", "project")
        )

        git_manager = GitManagerService(repo_path=project_dir)
        # Pull latest changes
        git_manager.pull()

        logger.info(f"Starting testing of {len(implemented_tasks)} tasks.")
        tested_tasks = []
        for task in implemented_tasks:
            logger.info(f"Testing task {task['task_id']}: {task['description']}")
            prompt = f"""
{get_prompt('testing_agent')}

Programming Language: {programming_language}

Code:
\"\"\"{task['code']}\"\"\"

Instructions:
- Write unit tests in {programming_language} for the provided code.
- Return only the test code.
- Do not include any comments, explanations, or code block markers like ```.

"""
            tests = call_llm(prompt)
            # Remove code block markers if present
            tests_clean = tests.strip()
            if tests_clean.startswith("```") and tests_clean.endswith("```"):
                tests_clean = "\n".join(tests_clean.strip("```").split("\n")[1:])
                tests_clean = tests_clean.strip()
            logger.debug(f"Generated tests for task {task['task_id']}:\n{tests_clean}")
            tested_tasks.append(
                {
                    "task_id": task["task_id"],
                    "description": task["description"],
                    "file_path": task["file_path"],
                    "code": task["code"],
                    "tests": tests_clean,
                }
            )

            # Save the tests to a test file
            test_file_name = f"test_{os.path.basename(task['file_path'])}"
            test_file_path = os.path.join(
                project_dir, os.path.dirname(task["file_path"]), test_file_name
            )
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
            with open(test_file_path, "w") as test_file:
                test_file.write(tests_clean)
            logger.info(f"Saved tests for task {task['task_id']} to {test_file_path}")

            # Add and commit the tests
            git_manager.add(test_file_path)
            git_manager.commit(f"Added tests for task {task['task_id']}")

        # Push changes to remote (if remote is set)
        try:
            git_manager.push()
        except Exception as e:
            logger.error(f"Git push failed: {e}")

        logger.info("All tasks tested.")
        return Result(
            value="Tasks tested.",
            context_variables={"tested_tasks": tested_tasks},
            agent="IntegrationAgent",
        )
