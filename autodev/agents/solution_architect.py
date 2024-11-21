# autodev/agents/solution_architect.py

import os
import re
import json
import logging
from typing import Dict, Any

from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt
from autodev.services.llm_service import call_llm
from autodev.services.git_manager import GitManagerService

logger = logging.getLogger(__name__)

class SolutionArchitectAgent(Agent):
    def __init__(self):
        super().__init__(
            name="SolutionArchitectAgent",
            instructions=get_prompt("solution_architect_agent"),
            functions=[self.architect_solution],
        )

    def extract_json_from_response(self, response: str) -> str:
        """Extract the JSON object from the LLM response."""
        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                return json_match.group(0)
        except Exception as e:
            logger.error(f"Error extracting JSON from response: {e}")
        return ""

    def architect_solution(self, context_variables: Dict[str, Any]) -> Result:
        tasks = context_variables.get("tasks", [])
        project_description = context_variables.get("project_description", "")
        project_name = context_variables.get("project_name", "project")
        output_dir = context_variables.get("output_dir", os.path.join(os.getcwd(), "output"))
        project_dir = os.path.join(output_dir, project_name)

        git_manager = GitManagerService(repo_path=project_dir)
        git_manager.init_repo()

        prompt = f"""
{get_prompt('solution_architect_agent')}

Project Description:
\"\"\"{project_description}\"\"\"

Initial Coding Tasks:
{tasks}

Instructions:
- Analyze the project description and initial coding tasks.
- Decide on the best technology stack, including programming language, frameworks, and libraries.
- Provide a high-level system architecture focused solely on code components (e.g., modules, classes, functions).
- Include the chosen programming language and frameworks in the architecture description.
- Define the folder structure of the project and specify **file paths with appropriate file extensions** where each task will be implemented.
- Ensure that the file structure and file names reflect the conventions of the chosen technology stack.
- Create dummy files in the repository to represent these files (e.g., empty `.js` files for JavaScript, `.java` for Java).
- Assign each task to a specific file path.
- Return the architecture, programming_language, updated tasks, and file assignments as a JSON object with keys "architecture", "programming_language", "tasks", and "file_structure".
- Do not include any comments, explanations, or non-code considerations.
- Do not include any code block markers like ```.

Output Format:
{{
    "architecture": "Description of the system architecture focused on code components, including programming language and frameworks.",
    "programming_language": "Programming language used (e.g., 'JavaScript', 'Java')",
    "tasks": [
        {{"task_id": 1, "description": "Detailed coding task description", "file_path": "path/to/file.ext"}},
        {{"task_id": 2, "description": "Detailed coding task description", "file_path": "path/to/another_file.ext"}}
    ],
    "file_structure": [
        "path/to/file.ext",
        "path/to/another_file.ext"
    ]
}}
"""

        response = call_llm(prompt)
        try:
            logger.debug(f"LLM raw response:\n{response}")
            response_clean = response.strip()
            json_str = self.extract_json_from_response(response_clean)
            if json_str:
                result_data = json.loads(json_str)
                logger.debug(f"Parsed LLM response: {result_data}")
                architecture = result_data.get("architecture", "")
                programming_language = result_data.get("programming_language", "").lower()
                updated_tasks = result_data.get("tasks", tasks)
                file_structure = result_data.get("file_structure", [])

                context_variables["architecture"] = architecture
                context_variables["programming_language"] = programming_language
                context_variables["tasks"] = updated_tasks

                extension_mapping = {
                    "javascript": ".js",
                    "java": ".java",
                    "python": ".py",
                    "c#": ".cs",
                    "c++": ".cpp",
                    "ruby": ".rb",
                    "php": ".php",
                    "go": ".go",
                    "typescript": ".ts",
                    "kotlin": ".kt",
                    "swift": ".swift",
                    # Add more mappings as needed
                }

                file_extension = extension_mapping.get(programming_language)
                if not file_extension:
                    logger.error(f"Unsupported programming language: {programming_language}")
                    return Result(
                        value="Failed to define solution architecture due to unsupported programming language.",
                        agent="ProjectManagerAgent",
                    )

                comment_syntax = {
                    "javascript": "//",
                    "java": "//",
                    "python": "#",
                    "c#": "//",
                    "c++": "//",
                    "ruby": "#",
                    "php": "//",
                    "go": "//",
                    "typescript": "//",
                    "kotlin": "//",
                    "swift": "//",
                    # Add more mappings as needed
                }
                comment_prefix = comment_syntax.get(programming_language, "#")

                for task in updated_tasks:
                    file_path = task.get("file_path", "")
                    base, ext = os.path.splitext(file_path)
                    if ext.lower() != file_extension:
                        file_path = f"{base}{file_extension}"
                        task["file_path"] = file_path
                    if file_path not in file_structure:
                        file_structure.append(file_path)

                for file_path in file_structure:
                    full_file_path = os.path.join(project_dir, file_path)
                    if full_file_path.endswith(os.sep):
                        logger.warning(f"Skipping directory path in file_structure: {file_path}")
                        continue
                    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
                    if os.path.isdir(full_file_path):
                        logger.warning(f"Expected a file but found a directory: {full_file_path}. Skipping...")
                        continue
                    try:
                        with open(full_file_path, "w", encoding="utf-8") as dummy_file:
                            dummy_file.write(f"{comment_prefix} This is a placeholder file.\n")
                        logger.info(f"Created file: {full_file_path}")
                    except Exception as e:
                        logger.error(f"Failed to create file {full_file_path}: {e}")

                git_manager.add(".")
                git_manager.commit("Initial commit with folder structure and dummy files")

                logger.info("Solution architecture defined, coding tasks updated, and folder structure created.")
                return Result(
                    value="Solution architecture defined, tasks updated, and folder structure created.",
                    context_variables=context_variables,
                    agent="ProjectManagerAgent",
                )
            else:
                logger.error("No JSON object found in LLM response.")
                logger.error(f"LLM response was:\n{response_clean}")
                return Result(
                    value="Failed to define solution architecture due to JSON error.",
                    agent="ProjectManagerAgent",
                )
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"LLM response was:\n{response_clean}")
            return Result(
                value="Failed to define solution architecture due to JSON error.",
                agent="ProjectManagerAgent",
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return Result(
                value="Failed to define solution architecture due to an unexpected error.",
                agent="ProjectManagerAgent",
            )
