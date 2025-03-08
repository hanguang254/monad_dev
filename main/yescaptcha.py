import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class YesCaptcha:

    def TurnstileTask(self):
        load_dotenv()
        CLIENT_KEY = os.getenv("CLIENT_KEY")
        if not CLIENT_KEY:
            print("错误: CLIENT_KEY 未正确加载！请检查 .env 文件")
            return

        website_url = 'https://testnet.monad.xyz/'
        site_key = '0x4AAAAAAA-3X4Nd7hf3mNGx'
        url = "https://api.yescaptcha.com/createTask"
        headers = {
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "content-type": "application/json"
        }
        data = {
                "clientKey":f"{CLIENT_KEY}",
                "task":
                {
                    "type":"TurnstileTaskProxylessM1",
                    "websiteURL":f"{website_url}",
                    "websiteKey":f"{site_key}"
                }
            }

        try:
            response = requests.post(url, json=data, headers=headers)
            print(f"请求状态码: {response.status_code}")
            print(response.text)

            if response.status_code != 200:
                print("请求失败，返回内容:", response.text)
                return

            result = response.json()
            print("API 返回数据:", result)

            taskId = result.get('taskId')
            if taskId:
                return taskId
            else:
                print("未找到 taskId，API 可能返回错误:", result)
        except requests.exceptions.RequestException as e:
            print("请求异常:", str(e))


if __name__ == '__main__':
    YesCaptcha().TurnstileTask()
