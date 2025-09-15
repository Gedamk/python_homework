# Task 3 & 4: Scrape Durham Library books
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time

# Load the web page
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
time.sleep(3)  # Wait for page to load

# Find all search result entries (li elements)
li_elements = driver.find_elements(By.CSS_SELECTOR, "li.search-result-item")  # Update selector if needed
print(f"Found {len(li_elements)} books.")

# Collect results
results = []
for li in li_elements:
    try:
        title = li.find_element(By.CSS_SELECTOR, "span.title").text
    except:
        title = "N/A"
    try:
        authors = li.find_elements(By.CSS_SELECTOR, "a.author")
        author_text = "; ".join([a.text for a in authors])
    except:
        author_text = "N/A"
    try:
        format_year = li.find_element(By.CSS_SELECTOR, "div.format-year span").text
    except:
        format_year = "N/A"

    results.append({
        "Title": title,
        "Author": author_text,
        "Format-Year": format_year
    })

# Create DataFrame
df = pd.DataFrame(results)
print(df)

# Write CSV
df.to_csv("get_books.csv", index=False)

# Write JSON
with open("get_books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

driver.quit()
