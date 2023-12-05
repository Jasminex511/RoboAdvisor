import pandas as pd
import json

# 加载excel文件
# 【注意】这里需要改写为自己的格式文件地址
df = pd.read_excel('C:\\Users\\11834\\Desktop\\test_optimization_result.xlsx')

# 处理结果
results = {}
for i, row in df.iterrows():
    etf = row[0]  # 第一列为ETF名称
    weights = row[1:].to_dict()  # 第二列开始为比重

    results[etf] = weights

import os

desktop_path = os.path.join("C:", os.sep, "Users", "11834", "Desktop")

# 【注意】这里需要改写写入json文件
with open(os.path.join(desktop_path, 'results.json'), 'w') as f:
    json.dump(results, f)