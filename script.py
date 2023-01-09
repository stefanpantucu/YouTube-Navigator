from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from datetime import datetime
import random

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

browser.get('http://www.youtube.com')

print("Accessed {} at {}".format(browser.title, current_time))

# get the accept cookies button and press it to continue
accept_btn_text = "Accept the use of cookies and other data for the purposes described"
acc_cookies_btn = browser.find_element(By.XPATH, "//button[@aria-label='{}']".format(accept_btn_text))

browser.execute_script("arguments[0].click()", acc_cookies_btn)
print("Accepted cookies at {}".format(current_time))

# get all the videos by thumbnail and access a random one
videos = browser.find_elements(By.TAG_NAME, "yt-image")

if len(videos) != 0:
    browser.execute_script("arguments[0].click()", videos[random.randint(0, len(videos))])
    print("Accessed video {} at {}".format(browser.title, current_time))

else:
    print("Error: got no videos")
    browser.quit()


# browser.quit()