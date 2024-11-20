# autodev/agents/solution_architect.py

from typing import Dict, Any
import logging
import json
import re
from ..core.agent import Agent
from ..core.types import Result
from ..prompts.agent_prompts import get_prompt
from ..services.llm_service import call_llm

logger = logging.getLogger(__name__)

def architect_solution(context_variables: Dict[str, Any]) -> Result:
    tasks = context_variables.get("tasks", [])
    project_description = context_variables.get("project_description", "")
    prompt = f"""
{get_prompt('solution_architect_agent')}

Project Description:
\"\"\"{project_description}\"\"\"

Initial Coding Tasks:
{tasks}

Instructions:
- Analyze the project description and initial coding tasks.
- Decide on the best programming languages, frameworks, libraries, and architectural patterns to use.
- Provide a high-level system architecture focused solely on code components (e.g., modules, classes, functions).
- Further decompose and redefine the tasks into more detailed, actionable coding tasks.
- Ensure that the tasks are clear, unambiguous, and can be directly implemented by developers.
- Return the architecture and the updated tasks as a JSON object with keys "architecture" and "tasks".
- Do not include any comments, explanations, or non-code considerations.
- Do not include any code block markers like ```.

Output Format:
{{
    "architecture": "Description of the system architecture focused on code components.",
    "tasks": [
        {{"task_id": 1, "description": "Detailed coding task description"}},
        {{"task_id": 2, "description": "Detailed coding task description"}}
    ]
}}
"""
    response = call_llm(prompt)
    try:
        logger.debug(f"LLM raw response:\n{response}")
        # Remove any code block markers or extra text
        response_clean = response.strip()
        if response_clean.startswith("```") and response_clean.endswith("```"):
            response_clean = "\n".join(response_clean.strip("```").split("\n")[1:])
            response_clean = response_clean.strip()
        # Extract JSON object from response
        json_match = re.search(r'{.*}', response_clean, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            result_data = json.loads(json_str)
            architecture = result_data.get("architecture", "")
            updated_tasks = result_data.get("tasks", tasks)
            context_variables["architecture"] = architecture
            context_variables["tasks"] = updated_tasks
            logger.info("Solution architecture defined and coding tasks updated.")
            logger.info(f"Architecture: {architecture}")
            logger.info(f"Updated Coding Tasks: {updated_tasks}")
            return Result(
                value="Solution architecture defined and coding tasks updated.",
                context_variables=context_variables,
                agent='ProjectManagerAgent'
            )
        else:
            logger.error("No JSON object found in LLM response.")
            logger.error(f"LLM response was:\n{response_clean}")
            return Result(
                value="Failed to define solution architecture due to JSON error.",
                agent='ProjectManagerAgent'
            )
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"LLM response was:\n{response_clean}")
        return Result(
            value="Failed to define solution architecture due to JSON error.",
            agent='ProjectManagerAgent'
        )

solution_architect_agent = Agent(
    name="SolutionArchitectAgent",
    instructions=get_prompt("solution_architect_agent"),
    functions=[architect_solution]
)
