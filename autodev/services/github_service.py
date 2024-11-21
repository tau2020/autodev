# autodev/services/github_service.py

import os
import logging
from github import Github, GithubException

logger = logging.getLogger(__name__)


class GitHubService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            logger.error("GITHUB_TOKEN environment variable not set.")
            raise ValueError("GITHUB_TOKEN environment variable not set.")
        self.github = Github(self.token)
        try:
            self.user = self.github.get_user()
            logger.info(f"Authenticated with GitHub as {self.user.login}")
        except GithubException as e:
            logger.error(f"Failed to authenticate with GitHub: {e}")
            raise

    def create_repository(self, repo_name: str, private: bool = True) -> None:
        if self.repository_exists(repo_name):
            logger.warning(f"Repository '{repo_name}' already exists.")
            return
        try:
            repo = self.user.create_repo(name=repo_name, private=private)
            logger.info(f"Repository '{repo_name}' created.")
        except GithubException as e:
            logger.error(f"Failed to create repository '{repo_name}': {e}")

    def commit_code(
        self,
        repo_name: str,
        file_path: str,
        content: str,
        commit_message: str = "Initial commit",
    ) -> None:
        try:
            repo = self.github.get_repo(f"{self.user.login}/{repo_name}")
            if self.file_exists(repo, file_path):
                logger.info(f"Updating existing file '{file_path}' in repository '{repo_name}'.")
                file = repo.get_contents(file_path)
                repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=file.sha,
                )
            else:
                repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                )
            logger.info(f"Committed code to {repo_name}/{file_path}")
        except GithubException as e:
            logger.error(f"Failed to commit code to {repo_name}/{file_path}: {e}")

    def repository_exists(self, repo_name: str) -> bool:
        try:
            self.github.get_repo(f"{self.user.login}/{repo_name}")
            logger.debug(f"Repository '{repo_name}' exists.")
            return True
        except GithubException:
            logger.debug(f"Repository '{repo_name}' does not exist.")
            return False

    def file_exists(self, repo, file_path: str) -> bool:
        try:
            repo.get_contents(file_path)
            logger.debug(f"File '{file_path}' exists in repository '{repo.name}'.")
            return True
        except GithubException:
            logger.debug(f"File '{file_path}' does not exist in repository '{repo.name}'.")
            return False
