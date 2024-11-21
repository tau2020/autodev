# autodev/agents/task_decomposer.py

from typing import Dict, Any
import logging
import json
import re
from autodev.core.agent import Agent
from autodev.core.types import Result
from autodev.prompts.agent_prompts import get_prompt
from autodev.services.llm_service import call_llm

logger = logging.getLogger(__name__)

class TaskDecomposerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="TaskDecomposerAgent",
            instructions=get_prompt("task_decomposer_agent"),
            functions=[self.decompose_project],
        )

    def decompose_project(self, context_variables: Dict[str, Any]) -> Result:
        project_description = context_variables.get("project_description", "")
        logger.info("Starting task decomposition.")
        logger.debug(f"Project description: {project_description}")

        prompt = f"""
{get_prompt('task_decomposer_agent')}

Project Description:
\"\"\"{project_description}\"\"\"

Instructions:
- Decompose the project into detailed, actionable coding tasks.
- Return the tasks **only** as a JSON array.
- **Do not** include any comments, explanations, or code block markers (like triple backticks).
- Each task must have "task_id" (integer) and "description" (string).
- Ensure the JSON is properly formatted.

Example Output:
[
    {{"task_id": 1, "description": "First coding task description"}},
    {{"task_id": 2, "description": "Second coding task description"}}
]
"""
        response = call_llm(prompt)
        try:
            logger.debug(f"LLM raw response:\n{response}")
            response_clean = response.strip()

            # Remove code block markers if present
            if response_clean.startswith("```") and response_clean.endswith("```"):
                response_clean = response_clean[3:-3].strip()

            # Extract JSON array from the response
            json_match = re.search(r'\[\s*{.*}\s*\]', response_clean, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                tasks = json.loads(json_str)
                logger.info("Task decomposition successful.")
                logger.debug(f"Decomposed Tasks: {tasks}")
                return Result(
                    value="Tasks decomposed.",
                    context_variables={"tasks": tasks},
                    agent="ProjectManagerAgent",
                )
            else:
                logger.error("No JSON array found in LLM response.")
                logger.error(f"LLM response was:\n{response_clean}")
                return Result(
                    value="Failed to decompose tasks due to missing JSON array.",
                    agent="ProjectManagerAgent",
                )
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"LLM response was:\n{response_clean}")
            return Result(
                value="Failed to decompose tasks due to JSON error.",
                agent="ProjectManagerAgent",
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(f"LLM response was:\n{response_clean}")
            return Result(
                value="Failed to decompose tasks due to an unexpected error.",
                agent="ProjectManagerAgent",
            )
