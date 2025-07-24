import base64
import os
import secrets
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv
from main.rpc_account import RpcConnect
from eth_account.messages import encode_defunct

# 加载环境变量
load_dotenv()

# RPC 初始化
rpc_url = "https://56.rpc.thirdweb.com"
web3 = RpcConnect().connect_rpc(rpc_url)

# 读取所有私钥
keys = RpcConnect().read_keys("key.csv", "key")

# 生成 nonce
def generate_nonce(length=13):
    raw = secrets.token_bytes(length)
    nonce = base64.urlsafe_b64encode(raw).decode().rstrip("=")
    return nonce.replace("-", "").replace("_", "")

# 主函数：对单个私钥进行登录和查询余额
def login_and_check_balance(private_key):
    try:
        account = RpcConnect().account(web3, private_key)
        web3.eth.get_transaction_count(account.address)  # 激活地址连接

        # 时间生成
        now = datetime.now(timezone.utc)
        issued_at = now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        expiration_time = (now + timedelta(days=7)).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        nonce_str = generate_nonce()

        # 构造 SIWE 消息（保持原始格式，不改换行方式）
        message_str = (
            f"knowledgedrop.saharaai.com wants you to sign in with your Ethereum account:\n"
            f"{account.address}\n\n"
            f"Sign in with Ethereum to the app.\n\n"
            f"URI: https://knowledgedrop.saharaai.com\n"
            f"Version: 1\n"
            f"Chain ID: 56\n"
            f"Nonce: {nonce_str}\n"
            f"Issued At: {issued_at}\n"
            f"Expiration Time: {expiration_time}"
        )

        # 签名
        message = encode_defunct(text=message_str)
        signed_message = web3.eth.account.sign_message(message, private_key=private_key)

        # 请求登录
        sign_url = "https://earndrop.prd.galaxy.eco/sign_in"
        login_headers = {
            "Content-Type": "application/json",
            "Origin": "https://knowledgedrop.saharaai.com",
            "User-Agent": "Mozilla/5.0"
        }

        data = {
            "address": account.address,
            "message": message_str,
            "public_key": "",
            "signature": "0x" + signed_message.signature.hex()
        }

        res = requests.post(url=sign_url, headers=login_headers, json=data)

        if res.status_code != 200 or "token" not in res.json():
            print(f"[❌] 登录失败: {account.address} -> {res.status_code} {res.text}")
            return

        token = res.json()["token"]

        # 查询余额
        info_url = "https://earndrop.prd.galaxy.eco/sahara/info"
        info_headers = {
            "authorization": token,
            "Content-Type": "application/json",
            "Origin": "https://knowledgedrop.saharaai.com",
            "User-Agent": "Mozilla/5.0"
        }

        balance_res = requests.get(url=info_url, headers=info_headers)
        if balance_res.status_code != 200:
            print(f"[⚠️ ] 获取余额失败: {account.address}")
            return

        balance = balance_res.json().get("data", {}).get("total_amount", "未知")
        print(f"[✅] {account.address} 查询余额：{balance}")

    except Exception as e:
        print(f"[ERROR] {private_key[:10]}... 出错：{e}")

# ========== 主循环 ==========
for key in keys:
    login_and_check_balance(key)
