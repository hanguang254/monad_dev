from datetime import datetime, timedelta
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

import requests
import schedule
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
from rpc_account import RpcConnect
from proxies import Proxies


def transfer_test(index, key, amount, max_retries=5):
    account = RpcConnect().account(web3, key=key)
    retry_count = 0  # 失败重试计数

    while retry_count < max_retries:
        try:
            random_amount = amount + random.uniform(0.001, 0.005)
            amount_in_wei = web3.to_wei(random_amount, "ether")
            print(f"[{index}]|开始执行任务 (尝试 {retry_count + 1}/{max_retries})")

            gas_price = web3.eth.gas_price
            balance = web3.eth.get_balance(account.address)

            if web3.from_wei(balance, 'ether') > 0.001:
                print(f"[{index}][{account.address}] 余额：{web3.from_wei(balance, 'ether')} SAHARA")

                transaction = {
                    'to': account.address,
                    'value': int(amount_in_wei),
                    'gas': 25000,
                    'gasPrice': gas_price,
                    'nonce': web3.eth.get_transaction_count(account.address),
                    'chainId': 313313
                }

                signed_transaction = web3.eth.account.sign_transaction(transaction, key)
                tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                if tx_receipt["status"] == 1:
                    print(f"[{index}][{account.address}] | ✅ | 转账成功 | hash: {tx_hash.hex()}")
                    return  # 成功后退出函数，不再重试
                else:
                    print(f"[{index}][{account.address}] | ❌ | 交易失败 : {tx_receipt}")

            else:
                print(f"[{index}][{account.address}] | ❌ | 余额不足 | 余额：{web3.from_wei(balance, 'ether')}")
                return  # 余额不足时直接退出，不重试

        except Exception as e:
            print(f"[{index}][{account.address}] | ❌ | 转账失败: {str(e)}")

        retry_count += 1
        if retry_count < max_retries:
            print(f"[{index}][{account.address}] | 🔄 | {retry_count} 次尝试失败，等待 5 秒后重试...")
            sleep(5)  # 失败后等待 5 秒再试
        else:
            print(f"[{index}][{account.address}] | ❌ | 转账失败，已达到最大重试次数")


def claim(key):
    account = RpcConnect().account(web3, key=key)
    try:
        # 获取本地环境参数
        proxy = Proxies().get_random_proxy()


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
        uid_res = requests.post(url=uid_url,headers=login_headers,json=uid_data,proxies=proxy,timeout=10)
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
        login_res = requests.post(url=login_url,headers=login_headers,json=login_data,proxies=proxy,timeout=10)

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
        fresh_res = requests.post(url=fresh_url,headers=headers,json=data,proxies=proxy,timeout=10).json()
        # print("刷新任务",fresh_res)
        db_data = {"taskIDs":["1004"],"timestamp":f"{time.time()}"}
        data_betch = "https://legends.saharalabs.ai/api/v1/task/dataBatch"

        db_res = requests.post(url=data_betch,headers=headers,json=db_data,proxies=proxy,timeout=10).json()
        # print(f"任务状态：{db_res}")

        if int(fresh_res) == 2 or int(fresh_res) == 3:
            sleep(2)
            url = "https://legends.saharalabs.ai/api/v1/task/claim"

            res = requests.post(url=url,headers=headers,json=data,proxies=proxy,timeout=10)
            if res.status_code == 200:
                rescive = res.json()[0]["amount"]
                print(f"[{account.address}]|✅|领取碎片[{rescive}]成功")
            else:
                print(f"[{account.address}]|❌|领取失败 :{res.json()}")
        else:
            print(f"[{account.address}]|✅|已领取")

    except Exception as e:
        print(f"[{account.address}]|❌|领取失败: {str(e)}")


def main():
    keys = RpcConnect().read_keys("key.csv", "key")
    rpc_url = "https://testnet.saharalabs.ai"
    workers = 5  # 并发任务数
    amount = 0.001  # 转账金额

    global web3  # 声明全局变量
    max_rpc_retries = 5  # 最大 RPC 连接重试次数
    rpc_retry_count = 0

    while rpc_retry_count < max_rpc_retries:
        web3 = RpcConnect().connect_rpc(rpc_url)
        if web3 and web3.is_connected():
            break
        else:
            print(f"⚠️  RPC 连接失败，重试 {rpc_retry_count + 1}/{max_rpc_retries}...")
            rpc_retry_count += 1
            sleep(5)
    else:
        print("❌ 无法连接到 RPC 服务器，退出程序")
        return

    for i in range(0, len(keys), workers):
        batch_keys = keys[i:i + workers]

        # **执行 transfer_test 任务，失败会自动重试**
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(transfer_test, index + i, key, amount): index for index, key in
                       enumerate(batch_keys)}
            for future in as_completed(futures):
                future.result()  # 确保每个任务都执行完毕

        print(f"⏳ {workers} 个任务执行完毕，等待 2 秒后继续...")
        sleep(2)

    print("✅ 所有 transfer_test 任务完成，开始 claim 任务")

    # **执行 claim 任务**
    with ThreadPoolExecutor(max_workers=workers) as executor:
        proxy = Proxies().get_random_proxy()
        web3 = RpcConnect().connect_rpc(rpc_url, proxy)

        futures = {executor.submit(claim, key): key for key in keys}
        for future in as_completed(futures):
            future.result()
    print("✅ 任务执行成功！")
    # # 获取并打印下次执行时间
    next_run_time = schedule.next_run()
    print(f"任务下次执行时间：{next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

    
if __name__ == '__main__':
    # 安排任务，每天 UTC 时间 12:00 运行一次
    schedule.every().day.at("12:00").do(main)

    print("✅ 任务已安排，每天 UTC 12:00 运行")

    while True:
        schedule.run_pending()
        time.sleep(60)
