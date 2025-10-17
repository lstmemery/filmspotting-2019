import asyncio
from playwright.async_api import async_playwright, TimeoutError
import re
from random import uniform
from pathlib import Path


class ChallongeScraper:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ]

    async def scrape(self):
        print("Starting scraper...")
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(
                headless=False,  # Keep browser visible
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=IsolateOrigins,site-per-process',
                ]
            )
            context = await browser.new_context(
                user_agent=self.user_agents[0],
                viewport={'width': 1920, 'height': 1080},
                # Add browser fingerprinting evasion
                java_script_enabled=True,
                has_touch=True,
                locale='en-US',
                timezone_id='America/New_York',
                permissions=['geolocation']
            )

            # Modify JavaScript detection
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            page = await context.new_page()
            results = []

            for page_num in range(3, 4):
                print(f"\nProcessing page {page_num}")
                url = f"https://challonge.com/madness2025/predictions?page={page_num}"
                print(f"Navigating to: {url}")
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(uniform(1, 3))

                # Replace the prediction_links section with this:
                print("Looking for Final Four predictions...")
                final_four_predictions = await page.eval_on_selector_all(
                    '.final_four span',
                    '''elements => elements
                        .map(el => el.textContent.trim())
                        .filter(text => text.length > 0)'''
                )
                print(f"Found {len(final_four_predictions)} Final Four entries")
                results.extend(final_four_predictions)

                # Later, when writing results:
                output_path = Path.home() / 'Documents/filmspotting-2019/results/2025_final_four_3.txt'
                print(f"Writing results to {output_path}")
                with open(output_path, 'w') as f:
                    for prediction in results:
                        f.write(f"{prediction}\n")

            print(f"\nScraping complete. Found {len(results)} total matches")
            await browser.close()
            return results

async def navigate_with_retry(page, link, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"Navigation attempt {attempt + 1}/{max_retries}")
            await page.goto(link, timeout=60000)  # 60 second timeout
            await page.wait_for_load_state('load')  # Wait for initial load only
            return True
        except TimeoutError as e:
            print(f"Timeout on attempt {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print("Max retries reached, skipping link")
                return False
            await asyncio.sleep(5)  # Wait before retry


async def main():
    scraper = ChallongeScraper()
    results = await scraper.scrape()

    output_path = Path.home() / 'Documents/filmspotting-2019/results/2025_predictions.csv'
    print(f"Writing results to {output_path}")
    with open(output_path, 'w') as f:
        f.write('\n'.join(results))
    print("Done!")


if __name__ == '__main__':
    asyncio.run(main())