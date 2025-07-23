import webbrowser
import requests
from urllib.parse import urlencode
from loguru import logger
from config import settings  

SLACK_AUTHORIZE_URL = "https://slack.com/oauth/v2/authorize"
SLACK_TOKEN_URL = "https://slack.com/api/oauth.v2.access"
REDIRECT_URI = "https://localhost:8000/callback"  


def generate_authorization_url():
    params = {
        "client_id": settings.SLACK_CLIENT_ID,
        "scope": "chat:write,channels:read,users:read",  # adjust scopes for your app
        "redirect_uri": REDIRECT_URI,
    }
    return f"{SLACK_AUTHORIZE_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    data = {
        "client_id": settings.SLACK_CLIENT_ID,
        "client_secret": settings.SLACK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(SLACK_TOKEN_URL, data=data)
    response.raise_for_status()
    token_data = response.json()

    if not token_data.get("ok"):
        raise Exception(f"Slack OAuth error: {token_data.get('error')}")
    return token_data  # contains access_token, team info, bot info


def run_cli_oauth_flow():
    logger.info("🔑 Starting OAuth2 CLI flow for Slack")
    auth_url = generate_authorization_url()
    logger.info(f"👉 Open the following URL in your browser to authorize access:\n{auth_url}")
    webbrowser.open(auth_url)

    code = input("Paste the code you received here: ").strip()
    if not code:
        logger.error("❌ No code provided. Aborting.")
        return

    try:
        token_data = exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        logger.success("✅ Access token retrieved successfully.")
        print(f"\n➡️  Your Slack Bot Access Token (put this in your .env as SLACK_BOT_TOKEN):\n{access_token}\n")
    except Exception as e:
        logger.error(f"❌ Failed to exchange code for token: {e}")


if __name__ == "__main__":
    run_cli_oauth_flow()
