import json
import time
import random
from playwright.sync_api import sync_playwright, TimeoutError

def extract_product_details(page, retries=3):
    for attempt in range(retries):
        try:
            return page.evaluate('''() => {
                const title = document.querySelector('.product-information_title__3jR8K')?.textContent.trim();
                const currentPrice = document.querySelector('.product-information_price__pEWjj div:first-child')?.textContent.trim();
                const originalPrice = document.querySelector('.product-information_compare-at-price__RZwtY')?.textContent.trim();
                const color = document.querySelector('.variants_colour__A3adN')?.textContent.trim();
                const description = document.querySelector('.accordion_content__Sk9kx')?.textContent.trim();
                const images = Array.from(document.querySelectorAll('img[sizes="100vw"]')).map(img => img.src);
                const sizes = Array.from(document.querySelectorAll('.size_size__saJiQ')).map(size => size.textContent.trim());
                
                const rating = document.querySelector('.action-bar_reviews__KMjaM span')?.textContent.trim();

                // Extract additional details from the description
                let fit = '';
                let materials = '';
                let sku = '';
                const descriptionParagraphs = document.querySelectorAll('.accordion_content__Sk9kx p');
                descriptionParagraphs.forEach(p => {
                    const text = p.textContent.trim();
                    if (text.startsWith('SIZE & FIT')) {
                        fit = text.split('SIZE & FIT')[1].trim();
                    } else if (text.startsWith('MATERIALS & CARE')) {
                        materials = text.split('MATERIALS & CARE')[1].trim();
                    } else if (text.startsWith('SKU:')) {
                        sku = text.split('SKU:')[1].trim();
                    }
                });

                return {
                    title,
                    currentPrice,
                    originalPrice,
                    color,
                    description,
                    images,
                    sizes,
                    rating,
                    fit,
                    materials,
                    sku
                };
            }''')
        except Exception as e:
            if attempt < retries - 1:
                print(f"Error extracting product details (attempt {attempt + 1}): {str(e)}. Retrying...")
                time.sleep(random.uniform(1, 3))
            else:
                print(f"Failed to extract product details after {retries} attempts: {str(e)}")
                return None

def save_progress(products, filename='progress_products.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)
    print(f"Progress saved: {len(products)} products")

def load_progress(filename='progress_products.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_all_products(page):
    last_height = 0
    while True:
        # Scroll down
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)  # Wait for content to load

        # Check if we've reached the bottom
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page.")
            break
        last_height = new_height

        try:
            load_more_button = page.query_selector("a.button_button__6GmNk.button_button--primary__bByrP:has-text('LOAD MORE')")
            if load_more_button:
                print("Clicking 'Load More' button...")
                load_more_button.click()
                page.wait_for_load_state("networkidle")
            else:
                print("No 'Load More' button found. Continuing to scroll...")
        except Exception as e:
            print(f"Error while trying to load more: {str(e)}")

    print("Finished loading all products.")

def run(playwright, url):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    all_products = load_progress()
    processed_urls = set(product['url'] for product in all_products)
    
    try:
        print(f"Loading the main page: {url}")
        page.goto(url, wait_until="domcontentloaded")
        
        print("Loading all products...")
        load_all_products(page)
        
        print("Extracting all product URLs...")
        product_urls = page.eval_on_selector_all(
            "a.product-card_product-title-link__jDI6f",
            "links => links.map(a => a.href)"
        )
        
        print(f"Total product URLs found: {len(product_urls)}")
        
        for index, product_url in enumerate(product_urls, 1):
            if product_url in processed_urls:
                print(f"Skipping already processed product: {product_url}")
                continue
            
            print(f"Processing product {index}/{len(product_urls)}: {product_url}")
            page.goto(product_url, wait_until="domcontentloaded")
            details = extract_product_details(page)
            if details:
                details['url'] = product_url
                all_products.append(details)
                processed_urls.add(product_url)
                print(f"Extracted details for: {details['title']}")
            else:
                print(f"Failed to extract details for: {product_url}")
            
            if len(all_products) % 10 == 0:
                save_progress(all_products)
            
            time.sleep(random.uniform(1, 3))
        
        return all_products
        
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return all_products
    finally:
        browser.close()

def main():
    url = 'https://ca.gymshark.com/collections/all-products'
    with sync_playwright() as playwright:
        products = run(playwright, url)
    
    if products:
        print(f"\nSuccessfully scraped {len(products)} products.")
        
        print("\nSample product data:")
        print(json.dumps(products[0], indent=2))
        
        with open('all_products.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2)
        print(f"\nDetailed data for {len(products)} products saved to all_products.json")
    else:
        print("No products were found or extracted.")

if __name__ == "__main__":
    main()
