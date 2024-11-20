from typing import Callable, Any, Dict, Optional, List
from .types import Result

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        functions: Optional[List[Callable[[Dict[str, Any]], Result]]] = None
    ):
        self.name = name
        self.instructions = instructions
        self.functions = functions or []

    def execute(self, context_variables: Dict[str, Any]) -> Result:
        for function in self.functions:
            result = function(context_variables)
            if result:
                return result
        return Result(
            value=f"{self.name} has no actions to perform.",
            agent=None,
            context_variables={}
        )
