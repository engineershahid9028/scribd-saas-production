import os
import re
from playwright.sync_api import sync_playwright

# Force Playwright to use Railway-installed browser
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/root/.cache/ms-playwright"

def download_scribd(url, output, progress):
    m = re.search(r"document/(\d+)", url)
    if not m:
        raise Exception("Invalid URL")

    doc_id = m.group(1)
    embed_url = f"https://www.scribd.com/embeds/{doc_id}/content"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(embed_url, wait_until="networkidle")

        for i in range(1, 21):
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            progress(i * 5)
            page.wait_for_timeout(400)

        pdf = page.pdf()
        with open(output, "wb") as f:
            f.write(pdf)

        browser.close()
