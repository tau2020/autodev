from typing import List, Dict, Any
import logging
from .agent import Agent
from .types import Response

logger = logging.getLogger(__name__)

class Swarm:
    def __init__(self):
        pass

    def run(
        self,
        agent: Agent,
        messages: List[Dict[str, Any]],
        context_variables: Dict[str, Any]
    ) -> Response:
        logger.info(f"Running agent: {agent.name}")
        result = agent.execute(context_variables)
        messages.append({
            'agent': agent.name,
            'message': result.value
        })
        context_variables.update(result.context_variables or {})
        logger.debug(f"Agent '{agent.name}' result: {result.value}")
        logger.debug(f"Context variables updated: {context_variables}")
        return Response(
            messages=messages,
            agent=result.agent,
            context_variables=context_variables
        )
