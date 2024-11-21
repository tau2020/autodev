# autodev/core/agent.py

from typing import Callable, Any, Dict, Optional, List
import logging
from .types import Result

logger = logging.getLogger(__name__)

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        functions: Optional[List[Callable[[Dict[str, Any]], Result]]] = None,
    ):
        self.name = name
        self.instructions = instructions
        self.functions = functions or []

    def execute(self, context_variables: Dict[str, Any]) -> Result:
        logger.info(f"Agent '{self.name}' is executing.")
        for function in self.functions:
            try:
                result = function(context_variables)
                if result:
                    logger.info(f"Function '{function.__name__}' executed successfully.")
                    return result
            except Exception as e:
                logger.error(f"Error in function '{function.__name__}': {e}")
                continue
        logger.warning(f"No actions performed by agent '{self.name}'.")
        return Result(
            value=f"{self.name} has no actions to perform.",
            agent=None,
            context_variables=context_variables,
        )
