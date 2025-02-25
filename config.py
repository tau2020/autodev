import os
from dotenv import load_dotenv

load_dotenv()
# LLM Configuration
MODEL_TYPE = os.getenv("MODEL_TYPE", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
HUGGINGFACE_MODEL_NAME = os.getenv("HUGGINGFACE_MODEL_NAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
RENDER_API_KEY = os.environ.get("RENDER_API_KEY")
RENDER_FRONTEND_SERVICE_ID = os.environ.get("RENDER_FRONTEND_SERVICE_ID")
RENDER_SERVICE_ID = os.environ.get("RENDER_BACKEND_SERVICE_ID")
DOCKER_PASSWORD = os.environ.get("DOCKER_PASSWORD")
DOCKER_USERNAME = os.environ.get("DOCKER_USERNAME")
DOCKER_REGISTRY = os.environ.get("DOCKER_REGISTRY")
