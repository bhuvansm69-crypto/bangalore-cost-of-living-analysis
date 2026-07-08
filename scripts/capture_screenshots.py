from playwright.sync_api import sync_playwright
import os
import time

BASE_URL = "http://127.0.0.1:8050"

OUTPUT_DIR = "images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

pages = [
    ("dashboard-home.png", "/"),
    ("analytics.png", "/analytics"),
    ("locality-explorer.png", "/locality"),
    ("provider-comparison.png", "/providers"),
    ("map.png", "/map"),
    ("raw-data.png", "/data"),
    ("about.png", "/about"),
]

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
        viewport={"width": 1920, "height": 1080}
    )

    for filename, route in pages:

        print(f"Capturing {route}")

        page.goto(BASE_URL + route)

        page.wait_for_load_state("networkidle")

        time.sleep(2)

        page.screenshot(
            path=os.path.join(OUTPUT_DIR, filename),
            full_page=True
        )

    browser.close()

print("Done!")