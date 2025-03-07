import os
import time
import random
import requests
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
from concurrent.futures import ThreadPoolExecutor
from mian.rpc_account import RpcConnect


# 读取代理池
def load_proxies():
    with open("../data/proxies.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


# 随机选择代理
def get_random_proxy():
    proxies_list = load_proxies()
    if proxies_list:
        proxy = random.choice(proxies_list)
        return {"http": proxy, "https": proxy}
    return None  # 没有代理则返回 None


def find_value(data, target_key):
    """递归查找字典或字典列表中的目标键"""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = find_value(value, target_key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_value(item, target_key)
            if result is not None:
                return result
    return None


def get_score(key):
    """查询单个账户积分"""
    account = RpcConnect().account(web3, key=key)
    timestamp = int(time.time())

    proxy = get_random_proxy()  # 选择一个随机代理

    # 获取签名消息
    message_url = "https://api-kiteai.bonusblock.io/api/auth/get-auth-ticket"
    message_data = {"nonce": f"timestamp_{timestamp}"}

    try:
        message_res = requests.post(message_url, json=message_data, proxies=proxy, timeout=10).json()
    except requests.RequestException as e:
        print(f"[{account.address}] ❌ 代理 {proxy} 连接失败: {e}")
        return

    msg = message_res["payload"]

    # 进行签名
    message = encode_defunct(text=msg)
    signed_message = web3.eth.account.sign_message(message, private_key=key)

    # 提交签名
    sign_url = "https://api-kiteai.bonusblock.io/api/auth/eth"
    sign_data = {
        "blockchainName": "ethereum",
        "signedMessage": f"0x{signed_message.signature.hex()}",
        "nonce": f"timestamp_{timestamp}",
        "referralId": "optionalReferral"
    }

    try:
        sign_res = requests.post(url=sign_url, json=sign_data, proxies=proxy, timeout=10).json()
    except requests.RequestException as e:
        print(f"[{account.address}] ❌ 代理 {proxy} 连接失败: {e}")
        return

    # 获取 token
    token = find_value(sign_res, "token")
    if not token:
        print(f"[{account.address}] ❌ 获取 token 失败！")
        return

    # 请求用户数据
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "x-auth-token": f"{token}"
    }
    url = "https://api-kiteai.bonusblock.io/api/kite-ai/get-status"

    try:
        user_res = requests.get(url, headers=headers, proxies=proxy, timeout=10).json()
    except requests.RequestException as e:
        print(f"[{account.address}] ❌ 代理 {proxy} 连接失败: {e}")
        return

    # 获取积分
    score = find_value(user_res, "userXp")
    if score is not None:
        print(f"[{account.address}] ✅ 积分：{score}")
    else:
        print(f"[{account.address}] ❌ 获取积分失败！")


def main():
    """多线程执行 get_score"""
    load_dotenv()
    keys = RpcConnect().read_keys("GoKiteAI_key.csv", "key")  # 读取多个密钥
    rpc_url = "https://api.avax.network/ext/bc/C/rpc"

    global web3
    web3 = RpcConnect().connect_rpc(rpc_url)

    # 使用线程池加速查询
    # 线程数
    workers = 1
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(get_score, keys)


if __name__ == '__main__':
    main()
