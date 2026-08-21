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
    input("故意卡住")
    print("繼續往下!!!")
    time.sleep(3)
    # 找到上面的圖片那個選擇
    e = driver.find_elements(By.CLASS_NAME, "C6AK7c")[2]
    e.click()
    time.sleep(5)
    # 找到所有小圖
    es = driver.find_elements(By.CLASS_NAME, "ImUqSb")
    for e in es:
        # 點小圖讓他旁邊出現大圖
        e.find_element(By.TAG_NAME, "a").click()
        # 如果你想省->1改少
        time.sleep(1)
        # 找到大圖
        e = driver.find_element(By.CLASS_NAME, "sFlh5c")
        # 找到圖片來源
        src = e.get_attribute("src")
        # 存圖片
        h = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
        }
        r = req.Request(src, headers=h)
        resp = req.urlopen(r)
        print(src)
        # 打開一個新的檔案, 把內容寫到新的檔案裡 w:寫入 b:不是純文字
        fname = f"google/{time.time()}.jpg"
        f = open(fname, "wb")
        f.write(resp.read())
        # 檔案關閉=儲存
        f.close()

    time.sleep(5)