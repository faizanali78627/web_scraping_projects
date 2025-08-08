import requests
from bs4 import BeautifulSoup
import csv
import time
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor

# Define list of cities
cities = [
 
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
import hashlib  

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_city(city_slug):
    base_url = f"https://www.psychologytoday.com/us/therapists/{city_slug}?page={{}}"
    page = 1
    last_page_hash = None
    city_key = city_slug.replace("/", "_")
    os.makedirs("html_pages", exist_ok=True)
    
    while True:
        url = base_url.format(page)
        print(f"🌐 Fetching {url}")
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"❌ Failed to load {url}")
            break

        html = res.text
        # Save each page as it's downloaded
        with open(f"html_pages/{city_key}_page_{page}.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Hash comparison to detect duplicates
        current_hash = hashlib.md5(html.encode()).hexdigest()
        if current_hash == last_page_hash:
            print(f"🛑 Page {page} is duplicate. Ending.")
            break
        last_page_hash = current_hash

        soup = BeautifulSoup(html, "html.parser")
        listings = soup.select(".results-row")
        if not listings:
            print(f"❌ No listings on page {page}")
            break

        # Extract and save data incrementally
        csv_path = f"therapists_{city_key}.csv"
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["city", "name", "phone", "area_postal", "bio"])
            if page == 1 and not os.path.exists(csv_path):
                writer.writeheader()
            for row in listings:
                name = row.select_one(".profile-title")
                phone = row.select_one(".results-row-phone")
                area = row.select_one("span.address")
                bio = row.find("span", attrs={"data-v-64dab710": True})
                writer.writerow({
                    "city": city_slug,
                    "name": name.get_text(strip=True) if name else None,
                    "phone": phone.get_text(strip=True) if phone else None,
                    "area_postal": area.get_text(strip=True) if area else None,
                    "bio": bio.get_text(strip=True) if bio else None
                })

        page += 1
        time.sleep(0.5)  # Polite pause

# Run multiple cities in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(scrape_city, cities)

print("✅ All cities scraped.")
