import os
import time

import requests
from dotenv import load_dotenv
from eth_account.messages import encode_defunct

from mian.rpc_account import RpcConnect


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

    account = RpcConnect().account(web3, key=key)
    # print(account.address)
    message_url = "https://api-kiteai.bonusblock.io/api/auth/get-auth-ticket"
    timestamp = int(time.time())
    message_data ={"nonce":f"timestamp_{timestamp}"}
    # print(message_data)
    message_res = requests.post(message_url,json=message_data).json()
    msg = message_res["payload"]

    # print("消息签名:",msg)
    message = encode_defunct(text=msg)
    signed_message = web3.eth.account.sign_message(message, private_key=key)
    # print(signed_message.signature.hex())
    sign_url = "https://api-kiteai.bonusblock.io/api/auth/eth"
    sign_data ={
        "blockchainName":"ethereum",
        "signedMessage":f"0x{signed_message.signature.hex()}",
        "nonce":f"timestamp_{timestamp}",
        "referralId":"optionalReferral"
    }
    # print(sign_data)
    sign_res = requests.post(url=sign_url,json=sign_data).json()
    # print(sign_res)
    token = find_value(sign_res,"token")
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "x-auth-token":f"{token}"
    }
    url = "https://api-kiteai.bonusblock.io/api/kite-ai/get-status"

    user_res = requests.get(url, headers=headers).json()
    # print(user_res)
    print(f"{account.address} 积分：{find_value(user_res,'userXp')}")

if __name__ == '__main__':
    load_dotenv()
    key = os.getenv("KEY")
    rpc_url = "https://api.avax.network/ext/bc/C/rpc"
    web3 = RpcConnect().connect_rpc(rpc_url)
    get_score(key)