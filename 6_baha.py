import urllib.request as req
import json
import pandas as pd

url = "https://api.gamer.com.tw/anime/v1/danmu.php?videoSn=36632&geo=TW%2CHK"
f = req.urlopen(url)
s = f.read()
# [] {} -> JSON格式
s = json.loads(s)
danmus = s["data"]["danmu"]
df = pd.DataFrame(danmus)
df.to_csv("danmu.csv", index=False)
print(df)