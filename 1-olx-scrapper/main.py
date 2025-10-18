import time
from playwright.sync_api import sync_playwright, Playwright, expect
from tabulate import tabulate
import urllib.parse

# --- Configuration ---
BASE_URL = "https://www.olx.in/items/q-"
SEARCH_TERM = "car cover"


# --- Constants for Selectors ---
# selector -> an address for the html element
LIST_SELECTOR = "ul[data-aut-id='itemsList']"
ITEM_SELECTOR = "li[data-aut-id='itemBox']"
TITLE_SELECTOR = "span[data-aut-id='itemTitle']"
PRICE_SELECTOR = "span[data-aut-id='itemPrice']"
DESC_SELECTOR = "span[data-aut-id='itemDescription']"


def get_olx_results(search_query: str):
    # 1. Build the URL
    query_safe = urllib.parse.quote_plus(search_query)
    search_url = f"{BASE_URL}{query_safe}?isSearchCall=true"
    
    results = []
    
    # 2. Start Playwright
    with sync_playwright() as p:
        try:
            # 3. Launch the browser
            browser = p.chromium.launch(headless=False) 
            page = browser.new_page()
            
            # 4. Go to the page
            page.goto(search_url, wait_until="load", timeout=60000)

            # 5. WAIT for the content to load
            print("Waiting for search results to load...")
            # list_container = page.wait_for_selector(LIST_SELECTOR, timeout=10000)
            list_container = page.wait_for_selector(LIST_SELECTOR)

            # 6. Find all items
            items = list_container.query_selector_all(ITEM_SELECTOR)
            print(f"Found {len(items)} items.")

            # 7. Loop and extract data
            for item in items:
                title = item.query_selector(TITLE_SELECTOR)
                price = item.query_selector(PRICE_SELECTOR)
                desc = item.query_selector(DESC_SELECTOR) 

                # 8. Clean the data
                title_text = title.text_content().strip() if title else "N/A"
                price_text = price.text_content().strip() if price else "N/A"
                desc_text = desc.text_content().strip() if desc else "N/A (See item page)"

                results.append([title_text, price_text, desc_text])
                
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            # 9. Clean up
            if 'browser' in locals():
                browser.close()
                
    return results


def main():
    
   # Main function to run the scraping process and print the results.
    
    search_results = get_olx_results(SEARCH_TERM)
    
    if search_results:
        print("\n--- OLX Search Results ---")
        headers = ["Title", "Price", "Description"]
        print(tabulate(search_results, headers=headers, tablefmt="grid"))
    else:
        print("No results were returned.")

if __name__ == "__main__":
    main()