
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import time


URL = "https://coa.gov.in/search_arch.php?lang=1&level=1&linkid=&lid=289&lang=1"

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)


def main():

    requests_found = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        # Capture requests
        def capture_request(request):

            requests_found.append({
                "method": request.method,
                "url": request.url,
                "resource_type": request.resource_type,
                "post_data": request.post_data
            })

            print("\n--- REQUEST ---")
            print("Method:", request.method)
            print("Type:", request.resource_type)
            print("URL:", request.url)

            if request.post_data:
                print("POST DATA:", request.post_data)

        page.on("request", capture_request)

        print("Opening CoA directory...")

        try:

            page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

        except Exception as e:

            print("\nNavigation warning:")
            print(e)

        # Give the page time to load
        time.sleep(5)

        print("\nFinal URL:")
        print(page.url)

        print("\nPage title:")
        print(page.title())

        print("\nThe browser is now open.")
        print("Perform ONE architect search.")
        print("If CAPTCHA appears, complete it normally.")

        input("\nPress ENTER after the search results appear...")

        # Give the RESULT page time to finish loading
        time.sleep(5)

        print("\nCurrent result URL:")
        print(page.url)

        print("\nCurrent page title:")
        print(page.title())

        # --------------------------------------------------
        # SAVE RESULT PAGE HTML
        # --------------------------------------------------

        try:

            html = page.content()

            Path(
                "data/coa_search_results.html"
            ).write_text(
                html,
                encoding="utf-8"
            )

            print("\nSaved RESULT page HTML.")

        except Exception as e:

            print("\nCould not save RESULT page HTML:")
            print(e)

        # --------------------------------------------------
        # SAVE NETWORK REQUESTS
        # --------------------------------------------------

        Path(
            "data/network_requests.json"
        ).write_text(
            json.dumps(
                requests_found,
                indent=2
            ),
            encoding="utf-8"
        )

        print("\nSaved network requests.")

        print(
            f"\nTotal requests captured: {len(requests_found)}"
        )

        print("\nResult page should now be saved.")

        input("\nPress ENTER to close the browser...")

        browser.close()


if __name__ == "__main__":
    main()
