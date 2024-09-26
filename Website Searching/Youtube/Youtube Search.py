from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

search_term = input("What do you want to search today?\n").strip()

while True:
    try:
        n = int(input("Number of videos:\n").strip())  # Strip spaces and ensure it's a valid integer
        break  # Exit loop if input is valid
    except ValueError:
        print("Please enter a valid number.")  # Prompt again if input is not a valid number

input("Press Enter to Start...")

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless") 

dv = webdriver.Chrome(options=chrome_options)
dv.get("https://www.youtube.com/")

wait = WebDriverWait(dv, 30)

# you have to press "Accept all".
time.sleep(5)

search_box = wait.until(EC.presence_of_element_located((By.NAME, 'search_query')))
search_box.send_keys(search_term)
time.sleep(1)
search_box.send_keys(Keys.RETURN)

# Waiting for the page to load, adjust as necessary
time.sleep(3)

videos = dv.find_elements(By.XPATH, '//ytd-video-renderer')
results = []

for video in videos[:n]:
    try:
        title = video.find_element(By.ID, 'video-title').text
        link = video.find_element(By.ID, 'video-title').get_attribute('href')
        thumbnail = video.find_element(By.XPATH, './/img').get_attribute('src')
        views = video.find_element(By.XPATH, './/span[contains(text(), "views")]').text  

        results.append({
            "title": title,
            "views": views,
            "link": link,
            "thumbnail": thumbnail
        })

        print(f"Title: {title}\nViews: {views}\nLink: {link}\nThumbnail: {thumbnail}\n")
    except Exception as e:
        print(f"Error processing video: {e}")
        continue

if results:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    filename = f"{search_term}_search_results.txt"
    filepath = os.path.join(script_dir, filename)  

    with open(filepath, "w", encoding="utf-8") as f:
        for result in results:
            f.write(f"Title: {result['title']}\nLink: {result['link']}\nThumbnail: {result['thumbnail']}\nViews: {result['views']}\n\n")

    print(f"Results saved in {filepath}")
else:
    print("No videos found or the list is empty.")

dv.quit()
