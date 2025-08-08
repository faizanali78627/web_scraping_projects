import csv
from bs4 import BeautifulSoup

# Load the rendered HTML (e.g., saved from Selenium)
with open("psychologytoday_page1_rendered.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Find all therapist blocks
therapists = soup.select(".results-row")
data = []

for i, therapist in enumerate(therapists, start=1):
    # Extract name
    name_el = therapist.select_one(".profile-title")
    name = name_el.get_text(strip=True) if name_el else None

    # Extract phone
    phone_el = therapist.select_one("span.results-row-phone")
    phone = phone_el.get_text(strip=True) if phone_el else None

    # Extract area/postal from span.address
    address_el = therapist.select_one("span.address")
    area_postal = address_el.get_text(strip=True) if address_el else None

    # Extract bio from Vue-rendered span
    bio_el = therapist.find("span", attrs={"data-v-64dab710": True})
    bio = bio_el.get_text(strip=True) if bio_el else None

    # Store all extracted data
    data.append({
        "name": name,
        "phone": phone,
        "area_postal": area_postal,
        "bio": bio
    })

# Preview the extracted data
print(f"\n✅ Found {len(data)} therapists on Page 1\n")
for i, entry in enumerate(data, 1):
    print(f"Therapist {i}:")
    for k, v in entry.items():
        print(f"  {k}: {v}")
    print()

# Save to CSV
with open("therapists_page1.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "phone", "area_postal", "bio"])
    writer.writeheader()
    writer.writerows(data)

print("✅ All therapist data saved to therapists_page1.csv")
