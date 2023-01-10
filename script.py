from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import cv2
import numpy as np
import pyautogui
import wave
import pyaudio

def is_connected():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

# # display screen resolution, get it using pyautogui itself
# SCREEN_SIZE = tuple(pyautogui.size())
# # define the codec
# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# # frames per second
# fps = 30.0
# # create the video write object
# out = cv2.VideoWriter("output.avi", fourcc, fps, (SCREEN_SIZE))
# # the time you want to record in seconds
# record_seconds = 10

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(browser, 10)

if not is_connected():
    print("Error! No interner connection")
    raise SystemExit

browser.get('http://www.youtube.com')
browser.maximize_window()

time.sleep(1)

# current_time = now.strftime("%Y-%m-%d %H:%M:%S")
print("Accessed {} at {}".format(browser.title, current_time))

# get the accept cookies button and press it to continue
accept_btn_text = "Accept the use of cookies and other data for the purposes described"
wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-label='{}']".format(accept_btn_text))))
acc_cookies_btn = browser.find_elements(By.XPATH, "//button[@aria-label='{}']".format(accept_btn_text))

if len(acc_cookies_btn) == 0:
    print("Error! Did not found the accept cookies button")
    browser.quit()
    raise SystemExit
else:
    acc_cookies_btn = acc_cookies_btn[0]


browser.execute_script("arguments[0].click()", acc_cookies_btn)
# current_time = now.strftime("%Y-%m-%d %H:%M:%S")
print("Accepted cookies at {}".format(current_time))

# get all the videos by thumbnail and access a random one
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "yt-image")))
videos = browser.find_elements(By.TAG_NAME, "yt-image")

if len(videos) != 0:
    idx = random.randint(0, len(videos) - 1) 

    browser.execute_script("arguments[0].click()", videos[idx])
    # current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Accessed video {} at {}".format(browser.title, current_time))
else:
    print("Error: got no videos")
    browser.quit()
    raise SystemExit

play_btn = browser.find_elements(By.XPATH, "//button[@class='ytp-play-button ytp-button']")

shorts_play_btn = browser.find_elements(By.XPATH, "//button[@class='ytp-large-play-button ytp-button']")

if len(play_btn) == 0 and len(shorts_play_btn) == 0:
    print("Error: did not find the play button")
    browser.quit()
    raise SystemExit
elif len(play_btn) == 0:
    play_btn = shorts_play_btn[0]
else:
    play_btn = play_btn[0]
    

play_btn.click()
# browser.execute_script("arguments[0].click()", play_btn)
# current_time = now.strftime("%Y-%m-%d %H:%M:%S")
print("Pressed play at {}".format(current_time))

# class="ytp-ad-skip-button ytp-button"
try:
    # Wait for the ad to appear
    skip_ad_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-ad-skip-button ytp-button']")))

    # Click on the skip ad button
    skip_ad_button.click()
    print("Skipped ad at {}".format(current_time))
except:
    print("No ad to skip.")

# browser.quit()
# current_time = now.strftime("%Y-%m-%d %H:%M:%S")

print("Closed browser at {}".format(current_time))