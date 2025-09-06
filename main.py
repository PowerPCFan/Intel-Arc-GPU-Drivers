"""
Scrape Intel's website for the latest Intel Arc GPU driver download link.
Exits with code 0 if successful, 1 otherwise.
"""

import sys
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def _print(message: str) -> None:
    print(message, flush=True)


def get_link() -> str:
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch(headless=True)
        page = chromium.new_page()
        page.goto(
            "https://www.intel.com/content/www/us/en/download/785597/"
            "intel-arc-iris-xe-graphics-windows.html"
        )
        html = page.content()
        chromium.close()

    soup = BeautifulSoup(html, 'html.parser')

    download_link = soup.select(
        'div.dc-page-available-downloads-hero-button > button'
    )[0]['data-href']

    return str(download_link)


if __name__ == "__main__":
    try:
        link = get_link()

        if link:
            _print(link)
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception:
        sys.exit(1)
else:
    sys.exit(1)
