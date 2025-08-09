import os
import json


class BaseBot():
    """BaseBot class for the other bots.
    Modern token handling: supports environment variables for CI/CD and falls back to token files."""

    def __init__(self, config_file) -> None:
        self._credentials = self._get_token(config_file)
        for k, v in self._credentials.items():
            self.__setattr__(k, v)

    def _get_token(self, config_file):
        """Read the access token from environment variable or json file.

        Priority:
        1. Environment variable (recommended for CI/CD)
        2. Token file (for local development)
        """
        env_var = f'{self.__class__.__name__.upper()}_BOT_TOKEN'
        env_token = os.getenv(env_var)
        if env_token:
            # If only token is needed, return as dict
            return {'bot_token': env_token}
        # Fallback to file
        try:
            with open(config_file, "r") as f:
                token = json.load(f)
            return token
        except FileNotFoundError:
            raise FileNotFoundError(f"No token found for {self.__class__.__name__}.\nSet the environment variable {env_var} or run the CLI set-token command.")
