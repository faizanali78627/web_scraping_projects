import requests
from bs4 import BeautifulSoup
import csv
import time

# ✅ Target one city: Austin, TX
city_slug = "tx/austin"
base_url = f"https://www.psychologytoday.com/us/therapists/{city_slug}?page={{}}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_data = []
page = 1

while True:
    url = base_url.format(page)
    print(f"🌐 Fetching {url}")
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"❌ Failed to load page {page}")
        break

    soup = BeautifulSoup(res.text, "html.parser")
    listings = soup.select(".results-row")

    if not listings:
        print(f"🛑 No listings found on page {page}. Ending.")
        break

    for row in listings:
        name = row.select_one(".profile-title")
        phone = row.select_one(".results-row-phone")
        area = row.select_one("span.address")
        bio = row.find("span", attrs={"data-v-64dab710": True})

        all_data.append({
            "city": "Austin, TX",
            "name": name.get_text(strip=True) if name else None,
            "phone": phone.get_text(strip=True) if phone else None,
            "area_postal": area.get_text(strip=True) if area else None,
            "bio": bio.get_text(strip=True) if bio else None
        })

    page += 1
    time.sleep(0.5)  # polite pause

# Save to CSV
with open("therapists_austin.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["city", "name", "phone", "area_postal", "bio"])
    writer.writeheader()
    writer.writerows(all_data)

print(f"✅ Done. {len(all_data)} therapists saved for Austin, TX.")
# This script fetches therapist listings from Psychology Today's Austin, TX page, extracts relevant data, and saves it to a CSV file. It handles pagination and ensures polite scraping with a delay between requests. Adjust the `city_slug` variable to target different cities as needed.
# The script uses requests and BeautifulSoup for efficient scraping without the overhead of Selenium, making it