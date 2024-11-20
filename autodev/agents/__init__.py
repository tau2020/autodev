# autodev/agents/__init__.py

from .user_interface import user_interface_agent
from .project_manager import project_manager_agent
from .task_decomposer import task_decomposer_agent
from .solution_architect import solution_architect_agent  # New agent
from .developer import developer_agent
from .testing import testing_agent
from .integration import integration_agent
from .deployment import deployment_agent

__all__ = [
    'user_interface_agent',
    'project_manager_agent',
    'task_decomposer_agent',
    'solution_architect_agent',  # Include in __all__
    'developer_agent',
    'testing_agent',
    'integration_agent',
    'deployment_agent'
]
