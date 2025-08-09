import os
import time
import requests
from typing import Any, Dict, Iterable, List, Optional, Union

# Prefer absolute import to avoid relative import issues
from codebots.bots._bot import BaseBot

__all__ = ["ClickUpBot"]


class ClickUpBot(BaseBot):
    """Bot to interact with ClickUp API v2 using a personal API token.

    Token handling:
    - Uses environment variable CLICKUPBOT_BOT_TOKEN if set (recommended for CI/CD).
    - Falls back to ~/.tokens/clickup.json with {"bot_token": "..."} for local dev.

    Parameters
    ----------
    config_file : str, optional
        Path to a JSON token file. Defaults to ~/.tokens/clickup.json
    base_url : str, optional
        Override ClickUp API base URL. Defaults to https://api.clickup.com/api/v2
    timeout : float, optional
        HTTP request timeout in seconds (default 30.0)
    """

    def __init__(
        self,
        config_file: Optional[str] = None,
        base_url: str = "https://api.clickup.com/api/v2",
        timeout: float = 30.0,
    ) -> None:
        if not config_file:
            from .. import TOKENS
            config_file = os.path.join(TOKENS, "clickup.json")
        super().__init__(config_file)

        token = getattr(self, "bot_token", None)
        if not token:
            raise ValueError(
                "ClickUp token not found. Set CLICKUPBOT_BOT_TOKEN or provide a token file."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        # ClickUp expects the token directly in the Authorization header (no 'Bearer' prefix)
        self._session.headers.update(
            {
                "Authorization": token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    @property
    def session(self) -> requests.Session:
        return self._session

    # ---------------------------
    # Low-level HTTP helper
    # ---------------------------
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """Issue an HTTP request with basic retry for 429/5xx."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        attempt = 0
        while True:
            attempt += 1
            resp = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                timeout=self.timeout,
            )

            # Handle rate limits and transient errors
            if resp.status_code in (429, 500, 502, 503, 504) and attempt <= max_retries:
                retry_after = resp.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else min(2 ** attempt, 10)
                time.sleep(delay)
                continue

            # Raise for other non-success responses
            if not (200 <= resp.status_code < 300):
                try:
                    detail = resp.json()
                except Exception:
                    detail = resp.text
                raise RuntimeError(
                    f"ClickUp API error {resp.status_code} {resp.reason} at {url}: {detail}"
                )

            # Return JSON payload
            try:
                return resp.json()
            except ValueError:
                return {}

    # ---------------------------
    # Team / Space / Folder / List
    # ---------------------------
    def get_teams(self) -> List[Dict[str, Any]]:
        """Return all teams the token has access to."""
        data = self._request("GET", "/team")
        return data.get("teams", [])

    def find_team_id(self, name: str) -> Optional[str]:
        """Find a team id by its name."""
        for team in self.get_teams():
            if team.get("name") == name:
                return str(team.get("id"))
        return None

    def get_spaces(self, team_id: Union[int, str], archived: bool = False) -> List[Dict[str, Any]]:
        data = self._request("GET", f"/team/{team_id}/space", params={"archived": str(archived).lower()})
        return data.get("spaces", [])

    def get_folders(self, space_id: Union[int, str], archived: bool = False) -> List[Dict[str, Any]]:
        data = self._request("GET", f"/space/{space_id}/folder", params={"archived": str(archived).lower()})
        return data.get("folders", [])

    def get_lists(self, folder_id: Union[int, str], archived: bool = False) -> List[Dict[str, Any]]:
        data = self._request("GET", f"/folder/{folder_id}/list", params={"archived": str(archived).lower()})
        return data.get("lists", [])

    # ---------------------------
    # Tasks
    # ---------------------------
    def list_tasks(
        self,
        list_id: Union[int, str],
        page: Optional[int] = None,
        archived: bool = False,
        include_subtasks: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"archived": str(archived).lower()}
        if page is not None:
            params["page"] = page
        if include_subtasks is not None:
            params["subtasks"] = str(include_subtasks).lower()
        data = self._request("GET", f"/list/{list_id}/task", params=params)
        return data.get("tasks", [])

    def get_task(self, task_id: Union[int, str]) -> Dict[str, Any]:
        return self._request("GET", f"/task/{task_id}")

    def create_task(
        self,
        list_id: Union[int, str],
        name: str,
        description: Optional[str] = None,
        status: Optional[str] = None,
        assignees: Optional[Iterable[Union[int, str]]] = None,
        tags: Optional[Iterable[str]] = None,
        priority: Optional[int] = None,
        due_date: Optional[int] = None,  # Unix ms
        due_date_time: Optional[bool] = None,
        start_date: Optional[int] = None,  # Unix ms
        start_date_time: Optional[bool] = None,
        notify_all: Optional[bool] = None,
        parent: Optional[str] = None,
        time_estimate: Optional[int] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a task in a list. Supply additional API fields via `extra` if needed."""
        payload: Dict[str, Any] = {"name": name}
        if description is not None:
            payload["description"] = description
        if status is not None:
            payload["status"] = status
        if assignees is not None:
            payload["assignees"] = [int(a) for a in assignees]
        if tags is not None:
            payload["tags"] = list(tags)
        if priority is not None:
            payload["priority"] = int(priority)
        if due_date is not None:
            payload["due_date"] = int(due_date)
        if due_date_time is not None:
            payload["due_date_time"] = bool(due_date_time)
        if start_date is not None:
            payload["start_date"] = int(start_date)
        if start_date_time is not None:
            payload["start_date_time"] = bool(start_date_time)
        if notify_all is not None:
            payload["notify_all"] = bool(notify_all)
        if parent is not None:
            payload["parent"] = str(parent)
        if time_estimate is not None:
            payload["time_estimate"] = int(time_estimate)
        if custom_fields is not None:
            payload["custom_fields"] = custom_fields
        if extra:
            payload.update(extra)

        return self._request("POST", f"/list/{list_id}/task", json=payload)

    def update_task(
        self,
        task_id: Union[int, str],
        fields: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update a task. Provide API fields in `fields` (e.g., {'status': 'in progress'})."""
        return self._request("PUT", f"/task/{task_id}", json=fields)

    def add_comment(
        self,
        task_id: Union[int, str],
        comment_text: str,
        assignee_id: Optional[Union[int, str]] = None,
        notify_all: bool = False,
    ) -> Dict[str, Any]:
        """Add a comment to a task."""
        payload: Dict[str, Any] = {"comment_text": comment_text, "notify_all": bool(notify_all)}
        if assignee_id is not None:
            payload["assignee"] = int(assignee_id)
        return self._request("POST", f"/task/{task_id}/comment", json=payload)


# Debug
if __name__ == "__main__":
    # Example usage:
    # export CLICKUPBOT_BOT_TOKEN="your-token"
    bot = ClickUpBot()
    teams = bot.get_teams()
    print(f"Teams: {[t.get('name') for t in teams]}")