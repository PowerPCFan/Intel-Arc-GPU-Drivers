from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url = "https://www.intel.com/content/www/us/en/download/785597/intel-arc-iris-xe-graphics-windows.html"

def get_link():
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch(headless=True)
        page = chromium.new_page()
        page.goto(url)
        html = page.content()
        chromium.close()

    soup = BeautifulSoup(html, 'html.parser')
    download_link = soup.select('div.dc-page-available-downloads-hero-button > button')
    
    return download_link[0]['data-href']

try:
    link = get_link()

    if link:
        print(link)
    else:
        print("Error")
except:
    print("Error")