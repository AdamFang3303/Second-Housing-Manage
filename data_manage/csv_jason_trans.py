import pandas as pd
import json

# 读取 CSV 文件
file_path = r"./data/杭州小区数据_带坐标.csv"
df = pd.read_csv(file_path, encoding='utf-8')

# 提取经纬度和均价数据
data = df[['经度', '纬度', '均价']].dropna().to_dict(orient='records')

# 保存为 JSON 文件
json_path = r"./data/杭州小区数据_带坐标.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"数据已保存到 {json_path}")