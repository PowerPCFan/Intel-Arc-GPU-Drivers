"""
Scrape Intel's website for the latest Intel Arc GPU driver download link.
Exits with code 0 if the link was successfully updated, 1 if an error occurred, and 2 if no update is needed.
"""

import sys
from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.sync_api import sync_playwright
from typing import Final, Union
from pathlib import Path


buttons_selector: Final[str] = "div.dc-page-available-downloads-hero-button > button"
driver_page: Final[str] = "https://www.intel.com/content/www/us/en/download/785597/intel-arc-iris-xe-graphics-windows.html"  # noqa: E501
link_file: Final[Path] = Path("configs") / "link.txt"


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


def is_update_required(new_link: str) -> bool:
    with open(link_file, "r") as file:
        old_link = file.read().strip()

    return new_link != old_link


def update_link(new_link: str) -> bool:
    try:
        if link_file.is_file():
            link_file.unlink(missing_ok=True)

        with open(link_file, "w", encoding="utf-8") as file:
            file.write(new_link)

        return True
    except Exception:
        return False


try:
    if __name__ == "__main__":
        link = get_link()

        if link is None or link == "":
            raise Exception("No link found")

        update_required = is_update_required(link)

        if update_required:
            update_link(link)
            sys.exit(0)
        else:
            sys.exit(2)
    else:
        raise Exception("This is not intended to be run as a module.")
except Exception as e:
    print(f"An unexpected error occurred: {e}", flush=True)
    sys.exit(1)
