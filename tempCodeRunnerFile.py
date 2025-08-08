from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = "https://www.psychologytoday.com/us/therapists/ny/new-york?page=1"

options = Options()
options.add_argument("--headless")  # runs without opening a window
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(8)  # ⏳ give JavaScript time to render content

# Save the fully loaded page
with open("psychologytoday_page1_rendered.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print("✅ Page fully loaded and saved.")
# This script uses Selenium to load a page and save the fully rendered HTML content.
# It waits for the JavaScript to execute before saving the page source. 