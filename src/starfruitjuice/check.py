import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()


BASE_URL = os.environ["BASE_URL"]
TARGET_SLUG = os.environ["TARGET_SLUG"]
TARGET_URL = f"{BASE_URL.rstrip("/")}/{TARGET_SLUG}/"

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


def main() -> int:
    print(f"Checking: {TARGET_URL}")

    html = fetch_page(TARGET_URL)

    if html is None:
        return 1

    if page_is_live(html):
        print("PAGE IS LIVE")
        return 0

    print("Page still unavailable")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
