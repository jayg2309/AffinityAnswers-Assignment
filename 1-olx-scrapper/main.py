import time
from playwright.sync_api import sync_playwright
from tabulate import tabulate
import urllib.parse

# Configuration
BASE_URL = "https://www.olx.in/items/q-"
SEARCH_TERM = "car cover"

def get_olx_results(search_query: str):
    query_safe = urllib.parse.quote_plus(search_query)
    search_url = f"{BASE_URL}{query_safe}"
    results = []
    
    with sync_playwright() as p:
        # Launch browser with a timeout
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Set navigation timeout (60 seconds)
            page.set_default_navigation_timeout(60000)
            
            # Navigate to the page
            print(f"Loading: {search_url}")
            page.goto(search_url, wait_until="domcontentloaded")
            
            # Wait for the items to load
            print("Waiting for items to load...")
            page.wait_for_selector('div[data-aut-id="itemBox"]', timeout=10000)
            
            # Get all items
            items = page.query_selector_all('div[data-aut-id="itemBox"]')
            print(f"Found {len(items)} items")
            
            # Extract data from each item
            for item in items:
                title_elem = item.query_selector('div[data-aut-id="itemTitle"]')
                price_elem = item.query_selector('span[data-autoid="price"]')
                desc_elem = item.query_selector('span[data-autoid="description"]')
                
                title = title_elem.text_content().strip() if title_elem else "N/A"
                price = price_elem.text_content().strip() if price_elem else "N/A"
                desc = desc_elem.text_content().strip() if desc_elem else "N/A"
                
                results.append([title, price, desc])
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            
        finally:
            # Clean up
            context.close()
            browser.close()
    
    return results

def main():
    search_results = get_olx_results(SEARCH_TERM)
    
    if search_results:
        print("\n--- OLX Car Covers ---")
        headers = ["Title", "Price", "Description"]
        print(tabulate(search_results, headers=headers, tablefmt="grid"))
    else:
        print("No results found or there was an error fetching data.")

if __name__ == "__main__":
    main()