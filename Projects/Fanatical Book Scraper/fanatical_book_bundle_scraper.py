import requests
import csv
import time
import os
from datetime import datetime

# navigates to each bundle and retrieves books
def get_books_from_bundle(slug, sale):
    
    if sale == "bundle":
        sale = "products-group"

    url = f"https://www.fanatical.com/api/{sale}/{slug}/en"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://www.fanatical.com/en/{sale}/{slug}",
        "Origin": "https://www.fanatical.com"
    }

    if sale == "pick-and-mix":
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                books = []
                authors = []
                for product in data.get("products", []):
                    title = product.get("name", "Unknown Title")
                    author = product.get("authors", [])
                    
                    books.append(title)
                    authors.append(author)

                return books, authors

        except Exception as e:
            print(f"❌ Error with {slug}: {e}")

    # If not Pick-and-Mix, try Bundle API
    else:
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                books = []
                authors = []
                bundles = data.get("bundles", [])

                for tier in bundles:
                    tier_items = tier.get("games", [])


                    for product in tier_items:
                        title = product.get("name", "Unknown Title")
                        author = product.get("authors", [])
                        
                        books.append(title)
                        authors.append(author)

                return books, authors

        except Exception as e:
            print(f"❌ Error with {slug}: {e}")

# Step 1: Retrieves bundles from fanatical and filters for book bundles returns slugs
url = "https://www.fanatical.com/api/algolia/bundles?altRank=false"
headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(url, headers=headers)
all_bundles = resp.json()

book_bundles = [b for b in all_bundles if b.get("display_type") == "book-bundle"]

book_slugs = []
bundle_titles = []
sale_types = []

for bundle in book_bundles:

    title = bundle.get("name", "N/A")
    sale_type = bundle.get("type", "")
    slug = bundle.get("slug", "")
    link = f"{url}/{slug}"

    bundle_titles.append(title)
    book_slugs.append(slug)
    sale_types.append(sale_type)

# Step 2: Retrieves all book titles and authors from each book slug

scraped_bundles = [[], [], []]

for slugs, sale_type in zip(book_slugs, sale_types):  
    result = get_books_from_bundle(slugs, sale_type)
    time.sleep(5)

    if not result:
        print(f"⚠️ Skipping {slugs} — no data returned.")
        continue

    books, authors = result
    slug_long_list = [slugs] * len(books)
    scraped_bundles[0].extend(slug_long_list)
    scraped_bundles[1].extend(books)
    scraped_bundles[2].extend(authors)

# Step 3: Convert column-wise to row-wise
rows = list(zip(*scraped_bundles)) # zips slug, title, author into rows

# Step 4: Export to CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "csv_exports")
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"fanatical_book_bundles_{timestamp}.csv"
output_path = os.path.join(output_dir, output_filename)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["bundle", "title", "author"])  # Header row
    writer.writerows(rows)

print(f"\n✅ Exported {len(rows) - 1} book entries to {output_path}")