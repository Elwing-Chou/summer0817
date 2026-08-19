import glob
import pandas as pd
import os

if not os.path.exists("巴哈id"):
    os.makedirs("巴哈id")

alldf = []
fn = glob.glob("baha/*.csv")
for f in fn:
    df = pd.read_csv(f)
    alldf.append(df)
# 把所有的表格合成一個大表格
table = pd.concat(alldf)

for u in table["userid"].unique():
    # 篩選: 把跟你資料筆數依樣多的True/False帶進去, 就完成篩選 False(刪除)
    fil = table["userid"] == u
    table[fil].to_csv(f"巴哈id/{u}.csv")