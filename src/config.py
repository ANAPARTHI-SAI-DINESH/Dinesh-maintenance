"""Configuration for the maintenance agent.

Reads settings from a .env file (see .env.example). Keeping the API key in .env
and out of the code is how you avoid leaking it into git.
"""
import os

from dotenv import load_dotenv

# Load variables from .env (in the project root) into the process environment.
load_dotenv()

# Which Claude model the agent talks to. Override in .env with MAINTENANCE_MODEL.
#   claude-haiku-4-5 -> cheap + fast, ideal while learning/iterating
#   claude-opus-4-8  -> strongest reasoning, for the polished version
MODEL = os.getenv("MAINTENANCE_MODEL", "claude-haiku-4-5")


def require_api_key() -> None:
    """Fail fast with a friendly message if the API key is missing."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "ANTHROPIC_API_KEY is not set.\n"
            "Fix: `cp .env.example .env` then paste your key from console.anthropic.com."
        )
