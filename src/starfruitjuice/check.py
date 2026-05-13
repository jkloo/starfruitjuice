import os
import sys

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()


TARGET_URL = os.environ["TARGET_URL"]

NOT_FOUND_TEXT = os.getenv(
    "NOT_FOUND_TEXT",
    "404 Error - Page not found",
)


def fetch_page(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=15)

        print(f"HTTP {response.status_code}")

        response.raise_for_status()

        return response.text

    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return None


def page_is_live(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()

    return NOT_FOUND_TEXT.lower() not in text.lower()


def main():
    print(f"Checking: {TARGET_URL}")

    html = fetch_page(TARGET_URL)

    if html is None:
        sys.exit(0)

    if page_is_live(html):
        print("PAGE IS LIVE")

        # Non-zero exit code can trigger
        # GitHub Actions notifications
        sys.exit(1)

    print("Page still unavailable")
    sys.exit(0)


if __name__ == "__main__":
    main()