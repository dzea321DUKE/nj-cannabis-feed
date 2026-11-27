import json
from datetime import datetime
from playwright.sync_api import sync_playwright

# Target dispensaries (e.g., Central NJ menus near Carteret / Woodbridge / Cranbury)
DISPENSARY_URLS = [
    {"name": "Breakwater Cranbury", "url": "https://breakwateratc.com"},
    # Add your preferred local dispensary menu URLs here
]

TARGET_BRANDS = [
    "Breakwater", "Clade9", "Garden Greens", "Full Tilt Labs", "Hamilton Farms",
    "Brighterside Farms", "EV Cultivation", "Bass River Buds", "Daily Muse", "Illicit",
    "710 Labs", "Hillview Farms", "Test Kitchen", "Niche", "Grown Rogue",
    "RYTHM", "Kind Tree", "Good Green", "Cookies", "Grassroots"
]

def collect_prices():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()

        for store in DISPENSARY_URLS:
            try:
                page.goto(store["url"], wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(3000)  # Wait for menu items to render
                body_text = page.inner_text("body")

                # Match target brands found on the rendered page
                for brand in TARGET_BRANDS:
                    if brand.lower() in body_text.lower():
                        results.append({
                            "brand": brand,
                            "tier": "Craft / Small-Batch",
                            "size": "3.5g Flower",
                            "dispensary": store["name"],
                            "regPrice": 55.00,   # Replace with CSS selector price extraction
                            "salePrice": 44.00,  # Replace with CSS selector sale extraction
                            "dealNote": f"Detected on {store['name']} ({datetime.now().strftime('%m/%d %H:%M')})"
                        })
            except Exception as e:
                print(f"Error reading {store['name']}: {e}")

        browser.close()

    # Save to prices.json
    with open("prices.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    collect_prices()
