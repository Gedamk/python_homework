# Task 6: Scrape OWASP Top 10
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

url = "https://owasp.org/www-project-top-ten/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
time.sleep(3)  # Wait for page to load

# Find top 10 vulnerabilities
vulns = driver.find_elements(By.XPATH, "//div[contains(@class,'top-ten')]//li")
top_10_list = []

for v in vulns[:10]:
    try:
        title = v.find_element(By.TAG_NAME, "a").text
        link = v.find_element(By.TAG_NAME, "a").get_attribute("href")
        top_10_list.append({"Vulnerability": title, "Link": link})
    except:
        continue

print(top_10_list)

# Write CSV
df = pd.DataFrame(top_10_list)
df.to_csv("owasp_top_10.csv", index=False)

driver.quit()
