from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = "https://www.wired.com/search/?q=AI&page="
data = []

page = 1

while len(data) < 60:
    print(f"\nScraping halaman {page}...")

    driver.get(base_url + str(page))
    time.sleep(5)

    articles = driver.find_elements(By.CSS_SELECTOR, "a.summary-item__hed-link")

    for article in articles:
        try:
            title = article.text
            link = article.get_attribute("href")

            # buka halaman detail
            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)

            # ambil author
            author = "ByUnknown"

            try:
                author_elem = driver.find_element(By.CSS_SELECTOR, '[rel="author"]')
                author = author_elem.text
            except:
                try:
                    author_elem = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="Byline-name"]')
                    author = "By " + author_elem.text
                except:
                    try:
                        author_elem = driver.find_element(By.CSS_SELECTOR, '.byline__name')
                        author = author_elem.text
                    except:
                        author = "ByUnknown"

            # ambil description
            try:
                desc_elem = driver.find_element(By.CSS_SELECTOR, 'meta[name="description"]')
                description = desc_elem.get_attribute("content")
            except:
                description = ""

            data.append({
                "title": title,
                "url": link,
                "description": description,
                "author": author,
                "scraped_at": datetime.now().isoformat(),
                "source": "Wired.com"
            })

            print(f"✔ {title} - {author}")

            # tutup tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            continue

    print(f"Total sementara: {len(data)}")
    page += 1

driver.quit()

# hapus duplikat
unique_data = {item["url"]: item for item in data}.values()
data = list(unique_data)

print(f"\nTOTAL AKHIR: {len(data)} artikel")

with open("../data/articles.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)