import os
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

# Top 50 cities EXCLUDING NY, LA, Austin, SF
top_cities = [
   
    "ca/san-diego", "tx/dallas", "ca/san-jose", "fl/jacksonville", "in/indianapolis",
    "oh/columbus", "nc/charlotte", "tx/fort-worth", "mi/detroit", "tn/memphis",
    "ma/boston", "wa/seattle", "co/denver", "dc/washington", "tn/nashville",
    "ok/oklahoma-city", "ky/louisville", "nv/las-vegas", "or/portland", "md/baltimore",
    "wi/milwaukee", "nm/albuquerque", "az/tucson", "ca/fresno", "ca/sacramento",
    "ks/wichita", "tx/el-paso", "nc/raleigh", "mo/kansas-city", "co/colorado-springs",
    "fl/miami", "ga/atlanta", "oh/cleveland", "fl/tampa", "pa/pittsburgh",
    "mn/minneapolis", "tx/arlington", "hi/honolulu", "la/new-orleans", "ct/bridgeport",
    "ca/long-beach", "ca/oakland", "fl/orlando", "va/virginia-beach", "mo/st-louis"
]

headers = {"User-Agent": "Mozilla/5.0"}

def download_and_save(city_slug, page, page_hashes):
    url = f"https://www.psychologytoday.com/us/therapists/{city_slug}?page={page}"
    folder = f"html_pages/{city_slug.replace('/', '_')}"
    os.makedirs(folder, exist_ok=True)

    try:
        res = requests.get(url, headers=headers, timeout=20)
        html = res.text

        page_hash = hashlib.md5(html.encode()).hexdigest()
        if page_hash in page_hashes:
            print(f"🛑 Duplicate for {city_slug} page {page}. Skipping.")
            return "duplicate"

        page_hashes.add(page_hash)
        file_path = f"{folder}/page_{page}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ {city_slug} → Page {page} saved.")
        return "ok"

    except Exception as e:
        print(f"❌ {city_slug} page {page} failed: {e}")
        return "error"

def threaded_downloader(city_slug, max_pages=500, max_workers=10):
    print(f"\n📍 Starting: {city_slug}")
    page_hashes = set()
    stop_at = None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for batch_start in range(439, max_pages + 1, max_workers):
            futures = {
                executor.submit(download_and_save, city_slug, page, page_hashes): page
                for page in range(batch_start, batch_start + max_workers)
            }
            for future in as_completed(futures):
                if future.result() == "duplicate":
                    stop_at = futures[future]
                    break
            if stop_at:
                print(f"✅ Done with {city_slug} at page {stop_at} (duplicate).")
                break

if __name__ == "__main__":
    for city in top_cities:
        threaded_downloader(city, max_pages=500, max_workers=20)