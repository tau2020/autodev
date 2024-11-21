# autodev/core/swarm.py

from typing import Dict, Any
import logging
from .agent import Agent
from .types import Response

logger = logging.getLogger(__name__)

class Swarm:
    def __init__(self, agents: Dict[str, Agent]):
        self.agents = agents

    def run(
        self,
        agent_name: str,
        context_variables: Dict[str, Any],
    ) -> Response:
        agent = self.agents.get(agent_name)
        if not agent:
            logger.error(f"Agent '{agent_name}' not found.")
            return Response(
                messages=[],
                agent=None,
                context_variables=context_variables,
            )
        logger.info(f"Running agent: {agent.name}")
        try:
            result = agent.execute(context_variables)
            messages = [{"agent": agent.name, "message": result.value}]
            context_variables.update(result.context_variables or {})
            logger.debug(f"Agent '{agent.name}' result: {result.value}")
            logger.debug(f"Context variables updated: {context_variables}")
            return Response(
                messages=messages,
                agent=result.agent,
                context_variables=context_variables,
            )
        except Exception as e:
            logger.error(f"Error executing agent '{agent.name}': {e}")
            return Response(
                messages=[],
                agent=None,
                context_variables=context_variables,
            )
