import os
import hashlib
import requests
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# === CONFIG ===
city_slug = "ca/san-francisco"  # Change as needed
folder = f"html_pages/{city_slug.replace('/', '_')}"
os.makedirs(folder, exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}

# === OXYLABS AUTHENTICATED PROXIES ===
username = "faizi_CUbRu"
password = "123456789Ali_"
proxy_host = "dc.oxylabs.io"
proxy_ports = ["8001", "8002", "8003", "8004", "8005"]

# Build authenticated proxy list
proxies_list = [
    f"http://{username}:{password}@{proxy_host}:{port}" for port in proxy_ports
]

# For tracking duplicates
page_hashes = {}

def download_and_save(page):
    url = f"https://www.psychologytoday.com/us/therapists/{city_slug}?page={page}"
    print(f"🌐 Fetching page {page}: {url}" )
    for attempt in range(3):
        proxy = random.choice(proxies_list)
        proxies = {"http": proxy, "https": proxy}
        try:
            res = requests.get(url, headers=headers, proxies=proxies, timeout=15)
            html = res.text

            # Check for duplicate
            page_hash = hashlib.md5(html.encode()).hexdigest()
            if page_hash in page_hashes.values():
                print(f"🛑 Page {page} is a duplicate. Skipping.")
                return "duplicate"
            page_hashes[page] = page_hash

            # Save the file
            path = f"{folder}/page_{page}.html"
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"✅ Page {page} saved via {proxy}")
            return "ok"

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed for page {page} with {proxy}: {e}")
            sleep(2)
    print(f"❌ Page {page} failed after retries.")
    return "error"

def threaded_downloader(max_pages=100, max_workers=10):
    stop_at = None
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for batch_start in range(1, max_pages + 1, max_workers):
            futures = {
                executor.submit(download_and_save, page): page
                for page in range(batch_start, batch_start + max_workers)
            }
            for future in as_completed(futures):
                result = future.result()
                if result == "duplicate":
                    stop_at = futures[future]
                    break
            if stop_at:
                print(f"🛑 Duplicate page reached at page {stop_at}. Stopping.")
                break

if __name__ == "__main__":
    threaded_downloader(max_pages=100, max_workers=10)
