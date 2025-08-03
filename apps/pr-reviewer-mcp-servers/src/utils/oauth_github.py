import webbrowser
import requests
from urllib.parse import urlencode
from loguru import logger
from config import settings


GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
REDIRECT_URI = "http://localhost:8000/callback"


def generate_authorization_url():
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "scope": "repo read:org",
        "redirect_uri": REDIRECT_URI,
    }
    return f"{GITHUB_AUTHORIZE_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> str:
    headers = {"Accept": "application/json"}
    data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(GITHUB_TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]


def run_cli_oauth_flow():
    logger.info("🔑 Starting OAuth2 CLI flow for GitHub")
    auth_url = generate_authorization_url()
    logger.info(f"👉 Open the following URL in your browser to authorize access:\n{auth_url}")
    webbrowser.open(auth_url)

    code = input("Paste the code you received here: ").strip()
    if not code:
        logger.error("❌ No code provided. Aborting.")
        return

    try:
        token = exchange_code_for_token(code)
        logger.success("✅ Access token retrieved successfully.")
        print(f"\n➡️  Your GitHub Access Token (put this in your .env as GITHUB_ACCESS_TOKEN):\n{token}\n")
    except Exception as e:
        logger.error(f"❌ Failed to exchange code for token: {e}")


if __name__ == "__main__":
    run_cli_oauth_flow()
