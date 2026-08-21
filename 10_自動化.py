# no module named distutils: pip install --upgrade setuptools
import undetected_chromedriver as uc
import time
import re
import os
import urllib.request as req
import urllib.parse as parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":

    name = "google"
    if not os.path.exists(name):
        os.makedirs(name)

    driver = uc.Chrome(version_main=151, use_subprocess=False)
    driver.get('https://www.google.com/')
    driver.maximize_window()

    # find_element, find_elements
    e = driver.find_element(By.TAG_NAME, "textarea")
    e.send_keys("chiikawa")
    e.send_keys(Keys.ENTER)
    time.sleep(3)
    # 找到上面的圖片那個選擇
    e = driver.find_elements(By.CLASS_NAME, "C6AK7c")[2]
    e.click()
    time.sleep(5)