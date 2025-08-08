import os
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

city_slug = "ca/san-francisco"
folder = f"html_pages/{city_slug.replace('/', '_')}"
os.makedirs(folder, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

# Store hashes to detect duplicate pages
page_hashes = {}

def download_and_save(page):
    url = f"https://www.psychologytoday.com/us/therapists/{city_slug}?page={page}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        html = res.text

        # Hash check to detect duplicates
        page_hash = hashlib.md5(html.encode()).hexdigest()
        if page_hash in page_hashes.values():
            print(f"🛑 Page {page} is a duplicate. Skipping.")
            return "duplicate"

        page_hashes[page] = page_hash
        file_path = f"{folder}/page_{page}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Saved: {file_path}")
        return "ok"

    except Exception as e:
        print(f"❌ Error on page {page}: {e}")
        return "error"

# Download pages in parallel batches, stopping on repeated pages
def threaded_downloader(max_pages=500, max_workers=10):
    stop_at = None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for batch_start in range(1, max_pages + 1, max_workers):
            futures = {
                executor.submit(download_and_save, page): page
                for page in range(batch_start, batch_start + max_workers)
            }
            for future in as_completed(futures):
                status = future.result()
                if status == "duplicate":
                    stop_at = futures[future]
                    break
            if stop_at:
                print(f"✅ Stopping after page {stop_at} due to duplicate content.")
                break

if __name__ == "__main__":
    threaded_downloader(max_pages=500, max_workers=10)
# This script downloads therapist listings from Psychology Today's Austin, TX page in parallel batches, saving each page as an HTML file. It detects duplicate pages using MD5 hashes and stops downloading when a duplicate is found. Adjust the `max_pages` and `max_workers` parameters as needed for your use case.
# It uses the requests library for efficient HTTP requests and concurrent.futures for parallel processing, making