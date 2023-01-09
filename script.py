from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

browser.get('http://www.youtube.com')

print(browser.title)

# browser.quit()