
import httpx
from config import settings
from loguru import logger

ASANA_PROJECT_TASKS_URL = f"https://app.asana.com/api/1.0/projects/{settings.ASANA_PROJECT_GID}/tasks"
ASANA_TASKS_URL = "https://app.asana.com/api/1.0/tasks"

class AsanaClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {settings.ASANA_TOKEN}"}
        )

    async def find_task(self, query: str) -> dict | None:
        logger.info(f"Searching for Asana task with query: '{query}' in project {settings.ASANA_PROJECT_GID}")
        list_resp = await self.client.get(
            ASANA_PROJECT_TASKS_URL,
        )
        list_resp.raise_for_status()
        task_refs = list_resp.json()["data"]

        for ref in task_refs:
            logger.debug(f"Checking task: {ref['name']} (gid: {ref['gid']})")
            if query.lower() in ref["name"].lower():
                logger.info(f"Found matching task: {ref['name']} (gid: {ref['gid']})")
                detail_resp = await self.client.get(f"{ASANA_TASKS_URL}/{ref['gid']}")
                detail_resp.raise_for_status()
                return detail_resp.json()["data"]

        logger.warning(f"No matching Asana task found for query: '{query}'")
        return None

    async def create_task(self, name: str, description: str = "") -> dict:
        logger.info(f"Creating Asana task: '{name}' in project {settings.ASANA_PROJECT_GID}")
        payload = {
            "data": {
                "name": name,
                "notes": description,
                "projects": [settings.ASANA_PROJECT_GID],
            }
        }
        resp = await self.client.post(
            ASANA_TASKS_URL,
            json=payload
        )
        resp.raise_for_status()
        logger.info(f"Created Asana task: '{name}' (response: {resp.json()})")
        return resp.json()["data"]