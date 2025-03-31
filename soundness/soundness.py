import random
import time

import pandas as pd
import requests

# 读取 CSV 数据
df = pd.read_csv("data.csv")

# 遍历每一行数据（如果你有多条要发）
for index, row in df.iterrows():
    authorization = row['Authorization']
    content = row['content']
    # print("发送内容：",content)

    url = "https://discord.com:443/api/v9/channels/1349309778693718036/messages"
    headers = {
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Authorization": authorization,
        "X-Discord-Timezone": "Asia/Shanghai",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/channels/1341336526713257984/1349309778693718036",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Priority": "u=1, i"
    }

    json_data = {
        "content": "!access " + content,
        "flags": 0,
        "mobile_network_type": "unknown",
        "nonce": str(random.randint(10**18, 10**19 - 1)),
        "tts": False
    }

    response = requests.post(url, headers=headers, json=json_data)
    print(content)
    print(f"第 {index + 1} 条消息响应：{response.status_code} - {response.text}")
    time.sleep(5)
