import urllib.request as req
import json
import pandas as pd
import bs4 as bs
import os

if not os.path.exists("baha"):
    os.makedirs("baha")

url = "https://ani.gamer.com.tw/animeVideo.php?sn=36632"
r = req.Request(url, headers={"User-Agent": "Mozilla/5.0"})
f = req.urlopen(r)
s = f.read()
html = bs.BeautifulSoup(s)
links = html.find_all("a")
for l in links:
    href = l["href"]
    if href.startswith("?sn"):
        sn = href.split("=")[1]
        # 拿到sn -> 下載每一集的蛋木
        url = f"https://api.gamer.com.tw/anime/v1/danmu.php?videoSn={sn}&geo=TW%2CHK"
        print(url)
        f = req.urlopen(url)
        s = f.read()
        # [] {} -> JSON格式
        s = json.loads(s)
        danmus = s["data"]["danmu"]
        df = pd.DataFrame(danmus)
        df.to_csv(f"baha/{sn}.csv", index=False)
