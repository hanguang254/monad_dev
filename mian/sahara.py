
import os

import requests
from dotenv import load_dotenv
from eth_account.messages import encode_defunct

from rpc_account import RpcConnect


def transfer_test():
    rpc_url = "https://testnet.saharalabs.ai"
    web3 = RpcConnect().connect_rpc(rpc_url)

    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 CSV 文件的完整路径
    csv_path = os.path.join(current_dir, 'key.csv')
     # 读取 CSV 文件，跳过标题行，获取第一个密钥
    keys = RpcConnect().read_key(csv_path,"key")

    # 设置转账金额（单位：ETH），并将其转换为 wei（1 ETH = 10^18 wei）
    amount_in_ether = 0.001  # 转账金额（单位：ETH）
    amount_in_wei = web3.to_wei(amount_in_ether, 'ether')

    # 获取当前的 gas price
    gas_price = web3.eth.gas_price

    # 获取本地环境参数
    # load_dotenv()
    # key = os.getenv("KEY")
    # print("私钥：", key)

    # print(keys)
    for i in keys:
        account = RpcConnect().account(web3,key=i)
        print("地址：",account.address)
        transaction = {
            'to': account.address,
            'value': amount_in_wei,
            'gas': 25000,  # 设置 gas 限额（可以根据实际情况调整）
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),  # 获取当前账户的 nonce
            'chainId': 313313  # 1 为主网，若是测试网，需要调整
        }

        # 使用私钥签名交易
        signed_transaction = web3.eth.account.sign_transaction(transaction, i)

        # 发送已签名的交易
        tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        # 输出交易哈希
        print(f"交易已发送，交易哈希: {tx_hash.hex()}")

        # 监听交易确认
        print("等待交易确认...")
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt["status"] == 1:
            print("发送交易成功")
        else:
            print(tx_receipt)


def claim():
    # 获取本地环境参数

    load_dotenv()
    key = os.getenv("KEY")
    # print("私钥：", key)

    rpc_url = "https://testnet.saharalabs.ai"
    web3 = RpcConnect().connect_rpc(rpc_url)
    account = RpcConnect().account(web3, key=key)

    # 获取签名uuid
    login_headers = {
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "Bearer null",
        "content-type": "application/json"
    }
    uid_url = "https://legends.saharalabs.ai/api/v1/user/challenge"

    uid_data = {
        "address": account.address,
    }
    uid_res = requests.post(url=uid_url,headers=login_headers,json=uid_data)
    # print(uid_res.json())
    uid = uid_res.json()['challenge']
    # 消息签名
    msg = (f"Sign in to Sahara! Challenge:{uid}")
    print(msg)
    message = encode_defunct(text=msg)
    signed_message = web3.eth.account.sign_message(message, private_key=key)
    print(signed_message.signature.hex())

    a = web3.eth.account.recover_message(message, signature=signed_message.signature)
    print(a)


    login_url = "https://legends.saharalabs.ai/api/v1/login/wallet"


    login_data = {
        "address":account.address,
        "sig":f"0x{signed_message.signature.hex()}",
        # "walletName":"MetaMask",
        # "walletUUID":"87a503ae-d129-464a-8237-f05b3afe1f1b"
    }
    print(login_data)
    login_res = requests.post(url=login_url,headers=login_headers,json=login_data)

    print(login_res.json())


    # token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ3YWxsZXQiLCJzdWIiOiIweDMyYjVkYjc4OTU0NDUxODk3YTNjMD"
    #          "g5YTViMGNlNTUzZGUwYTQ1OTciLCJhdWQiOlsiYWNjZXNzIl0sImV4cCI6MTczOTc0MTI0OSwianRpIjoiZDd0dzYybjEyNm"
    #          "F4WkNhTS0yMDQ3ODgwIn0.4LkfIoVcclB-9ZXoiylc8Jde3nsBpruu1PzXLYfNu88")
    #
    # url = "https://legends.saharalabs.ai/api/v1/task/claim"
    # headers = {
    #     "accept-encoding":"gzip, deflate, br, zstd",
    #     "accept-language":"zh-CN,zh;q=0.9",
    #     "authorization": f"Bearer {token}"
    # }
    # data = {
    #      "taskID":"1004"
    #  }
    # res = requests.post(url=url,headers=headers,json=data)
    # print(res.json())


if __name__ == '__main__':
    transfer_test()
    # claim()