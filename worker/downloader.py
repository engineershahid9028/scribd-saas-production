import re
from playwright.sync_api import sync_playwright

def download_scribd(url, output, progress):
    m = re.search(r"document/(\d+)", url)
    if not m:
        raise Exception("Invalid Scribd URL")

    doc_id = m.group(1)
    embed_url = f"https://www.scribd.com/embeds/{doc_id}/content"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(embed_url)

        for i in range(1, 21):
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            progress(i * 5)
            page.wait_for_timeout(400)

        pdf = page.pdf()
        with open(output, "wb") as f:
            f.write(pdf)

        browser.close()
