import time
import re
import undetected_chromedriver as uc

def download_scribd(url, output, progress):
    m = re.search(r"document/(\d+)", url)
    if not m:
        raise Exception("Invalid Scribd URL")

    doc_id = m.group(1)
    embed_url = f"https://www.scribd.com/embeds/{doc_id}/content"

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get(embed_url)

    for i in range(1, 21):
        driver.execute_script("window.scrollBy(0,2000)")
        progress(i * 5)
        time.sleep(0.5)

    pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
    with open(output, "wb") as f:
        f.write(bytes.fromhex(pdf["data"]))

    driver.quit()
