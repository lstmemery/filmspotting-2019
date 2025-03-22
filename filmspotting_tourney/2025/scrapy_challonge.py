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
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=self.user_agents[0],
                viewport={'width': 1920, 'height': 1080}
            )

            page = await context.new_page()
            results = []

            for page_num in range(1, 4):
                print(f"\nProcessing page {page_num}")
                url = f"https://challonge.com/madness2025/predictions?page={page_num}"
                print(f"Navigating to: {url}")
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(uniform(1, 3))

                print("Looking for prediction links...")
                prediction_links = await page.eval_on_selector_all(
                    'a[href*="tournaments/14453024/predictions"]',
                    '''elements => elements
                        .map(el => el.href)
                        .filter(href => /\/predictions\/\d{7}$/.test(href))'''
                )
                print(f"Found {len(prediction_links)} prediction links")

                for i, link in enumerate(prediction_links, 1):
                    print(f"\nProcessing link {i}/{len(prediction_links)}: {link}")
                    await page.goto(link)

                    try:
                        print("Waiting for PredictionController...")
                        await page.wait_for_selector('[data-react-class="PredictionController"]')

                        print("Extracting predictions...")
                        predictions = await page.evaluate('''() => {
                            const el = document.querySelector('[data-react-class="PredictionController"]');
                            return el ? el.getAttribute('data-react-props') : null;
                        }''')

                        if predictions:
                            matches = re.findall(r'\d{9},\d,\d{9}', predictions)
                            print(f"Found {len(matches)} matches")
                            results.extend(matches)
                        else:
                            print("No predictions found in data-react-props")

                        # Debug page content if no matches found
                        if not matches:
                            print("Page HTML snippet:")
                            content = await page.content()
                            print(content[:500] + "...")

                    except TimeoutError:
                        print("Timeout waiting for PredictionController")
                        print("Current URL:", await page.url())
                        print("Page title:", await page.title())

                    await asyncio.sleep(uniform(1, 3))

            print(f"\nScraping complete. Found {len(results)} total matches")
            await browser.close()
            return results


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