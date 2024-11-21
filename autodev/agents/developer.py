# autodev/agents/developer.py

import logging
import os
from typing import Dict, Any

from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt
from autodev.services.llm_service import call_llm
from autodev.services.git_manager import GitManagerService

logger = logging.getLogger(__name__)

class DeveloperAgent(Agent):
    def __init__(self):
        super().__init__(
            name="DeveloperAgent",
            instructions=get_prompt("developer_agent"),
            functions=[self.implement_tasks],
        )

    def implement_tasks(self, context_variables: Dict[str, Any]) -> Result:
        tasks = context_variables.get("tasks", [])
        programming_language = context_variables.get("programming_language", "python")
        output_dir = context_variables.get("output_dir", os.path.join(os.getcwd(), "output"))
        project_name = context_variables.get("project_name", "project")
        project_dir = os.path.join(output_dir, project_name)

        git_manager = GitManagerService(repo_path=project_dir)

        # Ensure project directory exists
        os.makedirs(project_dir, exist_ok=True)

        try:
            git_manager.pull()
        except Exception as e:
            logger.error(f"Git pull failed: {e}")

        logger.info(f"Starting implementation of {len(tasks)} tasks.")
        implemented_tasks = []

        for task in tasks:
            task_id = task.get('task_id')
            description = task.get('description', '')
            file_path = task.get('file_path', '')
            logger.info(f"Implementing task {task_id}: {description}")

            prompt = f"""
{get_prompt('developer_agent')}

Programming Language: {programming_language}

Task Description:
\"\"\"{description}\"\"\"

Instructions:
- Write code in {programming_language} to implement the task in the file: {file_path}.
- Include documentation as docstrings or comments within the code.
- Do not include any comments, explanations, or code block markers like ``` or '''.
- Return only the code.

"""

            code = call_llm(prompt)
            code_clean = code.strip('`').strip()
            logger.debug(f"Generated code for task {task_id}:\n{code_clean}")

            implemented_tasks.append({
                "task_id": task_id,
                "description": description,
                "file_path": file_path,
                "code": code_clean,
            })

            # Save the code to the specified file
            file_full_path = os.path.join(project_dir, file_path)
            os.makedirs(os.path.dirname(file_full_path), exist_ok=True)

            try:
                with open(file_full_path, "w", encoding='utf-8') as code_file:
                    code_file.write(code_clean)
                logger.info(f"Saved code for task {task_id} to {file_full_path}")
            except Exception as e:
                logger.error(f"Failed to save code for task {task_id}: {e}")
                continue

            # Add and commit the changes
            try:
                git_manager.add(file_path)
                git_manager.commit(f"Implemented task {task_id}: {description}")
            except Exception as e:
                logger.error(f"Git operations failed for task {task_id}: {e}")

        # Push changes to remote (if remote is set)
        try:
            git_manager.push()
        except Exception as e:
            logger.error(f"Git push failed: {e}")

        logger.info("All tasks implemented.")
        context_variables["project_dir"] = project_dir
        return Result(
            value="Tasks implemented.",
            context_variables={
                "implemented_tasks": implemented_tasks,
                "project_dir": project_dir,
            },
            agent="TestingAgent",
        )
