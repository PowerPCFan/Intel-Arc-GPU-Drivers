"""
Scrape Intel's website for the latest Intel Arc GPU driver download link.
Exits with code 0 if successful, 1 otherwise.
"""

import sys
from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.sync_api import sync_playwright
from typing import Final, Union


buttons_selector: Final[str] = "div.dc-page-available-downloads-hero-button > button"
driver_page: Final[str] = "https://www.intel.com/content/www/us/en/download/785597/intel-arc-iris-xe-graphics-windows.html"  # noqa: E501


def get_link() -> Union[str, None]:
    download_link: Union[str, None] = None

    with sync_playwright() as playwright:
        with playwright.chromium.launch(headless=True) as chromium:
            with chromium.new_page() as page:
                page.goto(driver_page)
                page.wait_for_selector(
                    selector=buttons_selector,
                    state="attached",
                    timeout=15000
                )
                html: str = page.content()

    soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

    buttons: ResultSet[Tag] = soup.select(buttons_selector)

    if buttons:
        download_button: Tag = buttons[0]
        raw_download_link = download_button.get("data-href")
        download_link = raw_download_link if isinstance(raw_download_link, str) else None

        if download_link is not None:
            download_link = download_link.strip()

    return download_link


try:
    if __name__ == "__main__":
        link = get_link()

        if link is not None and link != "":
            print(link, flush=True)
            sys.exit(0)
        else:
            raise Exception("No link found")
    else:
        raise Exception("This is not intended to be run as a module.")
except Exception:
    sys.exit(1)
