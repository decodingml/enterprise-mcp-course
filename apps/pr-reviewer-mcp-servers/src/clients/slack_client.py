import httpx
from config import settings
from loguru import logger

SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
SLACK_CHANNEL_HISTORY_URL = "https://slack.com/api/conversations.history"

class SlackClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {settings.SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            }
        )

    async def send_message(self, channel: str, text: str) -> dict:
        logger.info(f"Sending message to Slack channel '{channel}': {text}")
        payload = {
            "channel": channel,
            "text": text
        }
        resp = await self.client.post(
            SLACK_POST_MESSAGE_URL,
            json=payload
        )
        resp.raise_for_status()
        result = resp.json()
        if not result.get("ok"):
            logger.error(f"Failed to send message: {result}")
        else:
            logger.info(f"Message sent: {result}")
        return result

    async def get_last_messages(self, channel: str, limit: int = 10) -> list:
        logger.info(f"Fetching last {limit} messages from Slack channel '{channel}'")
        params = {
            "channel": channel,
            "limit": limit
        }
        resp = await self.client.get(
            SLACK_CHANNEL_HISTORY_URL,
            params=params
        )
        resp.raise_for_status()
        result = resp.json()
        if not result.get("ok"):
            logger.error(f"Failed to fetch messages: {result}")
            return []
        print(result)
        messages = result.get("messages", [])
        logger.info(f"Fetched {len(messages)} messages from channel '{channel}'")
        return messages
