import pandas as pd
import json
from urllib.parse import quote
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
# 定义获取经纬度的函数
def get_location(address, ak):
    base_url = "http://api.map.baidu.com/geocoding/v3/"
    params = {
        "address": address,
        "output": "json",
        "ak": ak
    }
    # 使用 urlencode 方法生成查询字符串
    query_string = urlencode(params, quote_via=quote_plus)
    url = f"{base_url}?{query_string}"  # 拼接完整的 URL
    try:
        response = urlopen(url)
        data = json.loads(response.read().decode())
        if data["status"] == 0:
            location = data["result"]["location"]
            return location["lng"], location["lat"]
        else:
            print(f"Error: {data['message']} for address {address}")
            return None, None
    except Exception as e:
        print(f"Error: {e} for address {address}")
        return None, None

# 读取CSV文件
file_path = r"./data/杭州小区数据.csv"
df = pd.read_csv(file_path, encoding='utf-8')

# 设置百度地图API Key
ak = "i57ftT5e9ZCta3Wu0ij4ZkrqKe8w61lE"  # 替换为你的百度地图API Key

# 新增两列：经度和纬度
df['经度'] = None
df['纬度'] = None

# 遍历每一行数据，获取经纬度
for index, row in df.iterrows():
    address = f"杭州市{row['所在区']}{row['所在街道']}{row['小区名称']}"
    lng, lat = get_location(address, ak)
    df.at[index, '经度'] = lng
    df.at[index, '纬度'] = lat

# 保存到新的CSV文件
output_path = r"./data/杭州小区数据_带坐标.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"处理完成，结果已保存到 {output_path}")