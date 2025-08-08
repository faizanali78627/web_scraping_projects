import os
import csv
from bs4 import BeautifulSoup

# -----------------------------
# Scrape all saved HTML files
# -----------------------------

def scrape_saved_city(city_slug):
    folder = f"html_pages/{city_slug.replace('/', '_')}"
    data = []

    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".html"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                therapists = soup.select(".results-row")

                for therapist in therapists:
                    name_el = therapist.select_one(".profile-title")
                    name = name_el.get_text(strip=True) if name_el else None

                    phone_el = therapist.select_one("span.results-row-phone")
                    phone = phone_el.get_text(strip=True) if phone_el else None

                    address_el = therapist.select_one("span.address")
                    area_postal = address_el.get_text(strip=True) if address_el else None

                    bio_el = therapist.find("span", attrs={"data-v-64dab710": True})
                    bio = bio_el.get_text(strip=True) if bio_el else None

                    data.append({
                        "name": name,
                        "phone": phone,
                        "area_postal": area_postal,
                        "bio": bio,
                        "source_page": filename
                    })

    return data

# -----------------------------
# Save scraped data to CSV
# -----------------------------

def save_to_csv(data, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "phone", "area_postal", "bio", "source_page"])
        writer.writeheader()
        writer.writerows(data)

# -----------------------------
# Run Example
# -----------------------------

if __name__ == "__main__":
    city_slug = "ca/san-francisco"

# Change to your target city slug
    # Ensure the folder exists 
# example, update as needed
    data = scrape_saved_city(city_slug)

    print(f"\n✅ Extracted {len(data)} therapists from saved HTML files for {city_slug}\n")
    save_to_csv(data, f"therapists_{city_slug.replace('/', '_')}.csv")
    print("✅ Data saved to CSV.")