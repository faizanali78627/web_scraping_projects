from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import csv

# Setup headless Chrome with random User-Agent
ua = UserAgent()
options = Options()
options.add_argument("--headless")
options.add_argument(f"user-agent={ua.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Output CSV setup
with open('therapists.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Profile URL', 'Phone', 'Bio'])

    page = 1
    city_url = 'https://www.psychologytoday.com/us/therapists/ny/new-york'

    while True:
        url = f"{city_url}?page={page}"
        print(f"[INFO] Loading page {page}: {url}")
        driver.get(url)

        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card")))
            cards_on_page = driver.find_elements(By.CSS_SELECTOR, "div.card")
            print(f"[DEBUG] Found {len(cards_on_page)} card divs using Selenium directly.")
        except Exception as e:
            print(f"[INFO] No content on page {page} or took too long: {e}")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cards = soup.select('div.card')

        if not cards:
            print("[INFO] No therapist profiles found.")
            break

        print(f"[INFO] Found {len(cards)} profiles on page {page}")
        for card in cards:
            try:
                name = card.select_one('h2').get_text(strip=True) if card.select_one('h2') else 'N/A'
                link_tag = card.select_one('a')
                link = 'https://www.psychologytoday.com' + link_tag['href'] if link_tag and link_tag.has_attr('href') else 'N/A'
                phone = card.select_one('.profile-phone').get_text(strip=True) if card.select_one('.profile-phone') else 'N/A'
                bio = card.select_one('p').get_text(strip=True) if card.select_one('p') else 'N/A'

                writer.writerow([name, link, phone, bio])
                print(f"  • {name}")
            except Exception as e:
                print(f"[WARN] Skipped a card due to: {e}")

        page += 1
        time.sleep(2)

# Clean up
driver.quit()
print("[DONE] therapists.csv created.")
