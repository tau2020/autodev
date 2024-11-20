# autodev/agents/task_decomposer.py

from typing import Dict, Any
import logging
import json
import re
from ..core.agent import Agent
from ..core.types import Result
from ..prompts.agent_prompts import get_prompt
from ..services.llm_service import call_llm

logger = logging.getLogger(__name__)

def decompose_project(context_variables: Dict[str, Any]) -> Result:
    project_description = context_variables.get("project_description", "")
    logger.info("Starting task decomposition.")
    logger.debug(f"Project description: {project_description}")

    prompt = f"""
{get_prompt('task_decomposer_agent')}

Project Description:
\"\"\"{project_description}\"\"\"

Instructions:
- Decompose the project into detailed, actionable tasks.
- Return the tasks **only** as a JSON array.
- **Do not** include any comments, explanations, or code block markers (like triple backticks).
- Each task must have "task_id" (integer) and "description" (string).
- Ensure the JSON is properly formatted.

Example Output:
[
    {{"task_id": 1, "description": "First task description"}},
    {{"task_id": 2, "description": "Second task description"}}
]
"""
    response = call_llm(prompt)
    try:
        logger.debug(f"LLM raw response:\n{response}")
        # Remove code block markers if present
        response_clean = response.strip()
        if response_clean.startswith("```") and response_clean.endswith("```"):
            response_clean = "\n".join(response_clean.strip("```").split("\n")[1:])
            response_clean = response_clean.strip()
        logger.debug(f"Cleaned LLM response:\n{response_clean}")
        tasks = json.loads(response_clean)
        logger.info("Task decomposition successful.")
        logger.info(f"Decomposed Tasks: {tasks}")
        return Result(
            value="Tasks decomposed.",
            context_variables={"tasks": tasks},
            agent='ProjectManagerAgent'
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"LLM response was:\n{response}")
        return Result(
            value="Failed to decompose tasks due to JSON error.",
            agent='ProjectManagerAgent'
        )

task_decomposer_agent = Agent(
    name="TaskDecomposerAgent",
    instructions=get_prompt("task_decomposer_agent"),
    functions=[decompose_project]
)
