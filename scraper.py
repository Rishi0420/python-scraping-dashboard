# scraper.py (Corrected selectors as of today)

import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_amazon_laptops():
    url = "https://www.amazon.in/s?k=laptops"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive'
    }

    print("Fetching page from Amazon...")
    # Using a timeout is a good practice
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(
            f"Error: Failed to retrieve the page. Status code: {response.status_code}")
        return None

    print("Page fetched successfully! Parsing HTML...")
    soup = BeautifulSoup(response.content, "html.parser")

    laptop_names = []
    laptop_prices = []
    laptop_ratings = []

    # Using a more general selector for the product container
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    if not results:
        print("Could not find any product containers.")
        return None

    print(f"Found {len(results)} potential products on the page.")

    for item in results:
        name = "N/A"
        price = "N/A"
        rating = "N/A"

        # --- Corrected Name Selector ---
        name_tag = item.find(
            'h2', class_='a-size-small a-spacing-none a-color-base s-line-clamp-3 a-text-normal')
        if name_tag:
            name = name_tag.get_text(strip=True)

        # --- Corrected Price Selector ---
        price_tag = item.find('span', class_='a-price-whole')
        if price_tag:
            price = price_tag.get_text(strip=True)

        # --- Corrected Rating Selector ---
        rating_tag = item.find('span', class_='a-icon-alt')
        if rating_tag:
            rating_text = rating_tag.get_text(strip=True)
            # Ensure it's a valid rating format like "4.1 out of 5 stars"
            if 'out of 5' in rating_text:
                rating = rating_text.split()[0]

        # We only add the product if it has a name AND a price
        if name != "N/A" and price != "N/A":
            laptop_names.append(name)
            laptop_prices.append(price)
            laptop_ratings.append(rating)

    # Create a pandas DataFrame
    if not laptop_names:
        print("Warning: No products with both Name and Price were found.")
        return None

    df = pd.DataFrame({
        'Name': laptop_names,
        'Price': laptop_prices,
        'Rating': laptop_ratings
    })

    return df


if __name__ == "__main__":
    # First, delete old files to ensure a fresh start
    import os
    if os.path.exists('laptops_data.csv'):
        os.remove('laptops_data.csv')
    if os.path.exists('laptops.db'):
        os.remove('laptops.db')

    laptops_df = scrape_amazon_laptops()

    if laptops_df is not None and not laptops_df.empty:
        print("\n--- Scraped Data Sample ---")
        print(laptops_df.head())

        laptops_df.to_csv('laptops_data.csv', index=False)
        print("\nData successfully saved to 'laptops_data.csv'.")
    else:
        print("\nNo valid data was scraped. Please check scraper selectors or network connection.")
