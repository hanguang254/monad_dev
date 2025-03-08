import os
import time
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import requests
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
from rpc_account import RpcConnect



def transfer_test(index,key,amount):

    # 设置转账金额（单位：ETH），并将其转换为 wei（1 ETH = 10^18 wei）
    # amount_in_ether = 0.001  # 转账金额（单位：ETH）
    amount_in_wei = int(float(amount) * (10 ** 18))
    print(f"[{index}]|开始执行任务")

    # 获取当前的 gas price
    gas_price = web3.eth.gas_price

    # 获取本地环境参数
    # load_dotenv()
    # key = os.getenv("KEY")
    # print("私钥：", key)

    # print(keys)
    account = RpcConnect().account(web3,key=key)
    print(f"[{index}][{account.address}]余额：{web3.from_wei(web3.eth.get_balance(account.address),'ether')}")
    transaction = {
        'to': account.address,
        'value': amount_in_wei,
        'gas': 25000,  # 设置 gas 限额（可以根据实际情况调整）
        'gasPrice': web3.to_wei(1.2,"gwei"),
        'nonce': web3.eth.get_transaction_count(account.address),  # 获取当前账户的 nonce
        'chainId': 313313  # 1 为主网，若是测试网，需要调整
    }

    # 使用私钥签名交易
    signed_transaction = web3.eth.account.sign_transaction(transaction, key)

    # 发送已签名的交易
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    # 输出交易哈希
    # print(f"交易已发送，交易哈希: {tx_hash.hex()}")

    # 监听交易确认
    # print("等待交易确认...")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt["status"] == 1:
        print(f"[{index}][{account.address}]|✅|转账成功|hash:{tx_hash.hex()}")
    else:
        print(f"[{index}][{account.address}]|❌|交易失败 :{tx_receipt}")


def claim(key):
    # 获取本地环境参数

    # load_dotenv()
    # key = os.getenv("KEY")
    # print("私钥：", key)
    account = RpcConnect().account(web3, key=key)

    # 获取签名uuid
    login_headers = {
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "content-type": "application/json"
    }
    uid_url = "https://legends.saharalabs.ai/api/v1/user/challenge"

    uid_data = {
        "address": account.address,
        "timestamp":time.time()
    }
    # print(uid_data)
    uid_res = requests.post(url=uid_url,headers=login_headers,json=uid_data)
    # print(uid_res)
    uid = uid_res.json()['challenge']
    # 消息签名
    msg = (f"Sign in to Sahara!\nChallenge:{uid}")
    # print("消息签名")
    message = encode_defunct(text=msg)
    signed_message = web3.eth.account.sign_message(message, private_key=key)
    # print(signed_message.signature.hex())

    a = web3.eth.account.recover_message(message, signature=signed_message.signature)
    # print(f"本地验证签名地址：{a}")


    login_url = "https://legends.saharalabs.ai/api/v1/login/wallet"


    login_data = {
        "address":account.address,
        "sig":f"0x{signed_message.signature.hex()}",
        "timestamp":time.time()
        # "walletName":"MetaMask",
        # "walletUUID":"87a503ae-d129-464a-8237-f05b3afe1f1b"
    }
    # print(login_data)
    login_res = requests.post(url=login_url,headers=login_headers,json=login_data)

    # print(login_res.json())
    token = login_res.json()['accessToken']
    # 刷新任务
    fresh_url = "https://legends.saharalabs.ai/api/v1/task/flush"

    data = {
        "taskID": "1004",
        "timestamp":time.time()
    }

    headers = {
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "authorization": f"Bearer {token}"
    }
    fresh_res = requests.post(url=fresh_url,headers=headers,json=data).json()
    # print("刷新任务",fresh_res)
    db_data = {"taskIDs":["1004"],"timestamp":f"{time.time()}"}
    data_betch = "https://legends.saharalabs.ai/api/v1/task/dataBatch"

    db_res = requests.post(url=data_betch,headers=headers,json=db_data).json()
    # print(f"任务状态：{db_res}")

    if int(fresh_res) == 2 or int(fresh_res) == 3:
        sleep(2)
        url = "https://legends.saharalabs.ai/api/v1/task/claim"

        res = requests.post(url=url,headers=headers,json=data)
        if res.status_code == 200:
            print(f"[{account.address}]|✅|领取碎片[{res.json()[0]["amount"]}]成功")
        else:
            print(f"[{account.address}]|❌|领取失败 :{res.json()}")
    else:
        print(f"[{account.address}]|✅|已领取")


def main():

    keys = RpcConnect().read_keys("key.csv","key")

    rpc_url = "https://testnet.saharalabs.ai"
    global web3
    web3 = RpcConnect().connect_rpc(rpc_url)

    if web3.is_connected():
        # 使用线程池加速查询
        workers = 5 # 线程数
        amount = 0.001 #转账金额
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # 提交 transfer_test 任务，并保存 Future 对象
            futures = [executor.submit(transfer_test, index, key,amount) for index, key in enumerate(keys)]

            # 等待所有 transfer_test 任务执行完毕
            for future in futures:
                future.result()  # 这里会阻塞，直到所有任务完成

            print("✅ 所有 transfer_test 任务完成，开始 claim 任务")

            # 线程池执行 claim
            executor.map(claim, keys)

if __name__ == '__main__':
    # load_dotenv()
    # key = os.getenv("KEY")
    # print("私钥：", key)
    # claim(key)
    main()
