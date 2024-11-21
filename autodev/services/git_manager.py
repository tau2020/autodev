# autodev/services/git_manager.py

import os
import subprocess
import logging

logger = logging.getLogger(__name__)


class GitManagerService:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        os.makedirs(self.repo_path, exist_ok=True)
        if not self.is_git_repository():
            self.init_repo()

    def is_git_repository(self) -> bool:
        return os.path.isdir(os.path.join(self.repo_path, ".git"))

    def init_repo(self):
        logger.info(f"Initializing new Git repository at {self.repo_path}")
        self.run_git_command(["init"])

    def has_remote(self) -> bool:
        result = self.run_git_command(["remote"], capture_output=True)
        remotes = result.stdout.strip()
        return bool(remotes)

    def pull(self):
        if self.has_remote():
            logger.info("Pulling latest changes from remote.")
            self.run_git_command(["pull"], check=False)
        else:
            logger.info("No remote configured. Skipping git pull.")

    def add(self, file_pattern: str = "."):
        logger.info(f"Adding files to staging area: {file_pattern}")
        self.run_git_command(["add", file_pattern])

    def commit(self, message: str):
        logger.info(f"Committing changes with message: {message}")
        status = self.run_git_command(["status", "--porcelain"], capture_output=True)
        if status.stdout.strip():
            self.run_git_command(["commit", "-m", message], check=False)
        else:
            logger.info("Nothing to commit.")

    def push(self, remote_name: str = "origin", branch_name: str = "main"):
        if self.has_remote():
            logger.info(f"Pushing changes to {remote_name}/{branch_name}")
            self.run_git_command(["push", remote_name, branch_name], check=False)
        else:
            logger.info("No remote configured. Skipping git push.")

    def set_remote(self, remote_name: str, remote_url: str):
        logger.info(f"Setting remote '{remote_name}' to '{remote_url}'")
        self.run_git_command(["remote", "add", remote_name, remote_url])

    def run_git_command(self, command_list, capture_output=False, check=True):
        try:
            result = subprocess.run(
                ["git"] + command_list,
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                check=check,
            )
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command '{' '.join(command_list)}' failed: {e}")
            if capture_output:
                return e
            else:
                raise
