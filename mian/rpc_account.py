import csv
import json

from web3 import Web3
import os
from dotenv import load_dotenv


class RpcConnect:

    def connect_rpc(self,url):
        try:
            # # 读取rpc变量
            # load_dotenv()
            # rpc = os.getenv("RPC")
            # 链接rpc
            w3 = Web3(Web3.HTTPProvider(url))
            res = w3.is_connected()
            if res:
                print("链接rpc成功")
            else:
                print("链接rpc失败")
            # print(f"链接结果：{res}")
            return w3
        except Exception as e:
            print("错误提示:",e)

    def create_account(self,web3,num_accounts):
        private_keys = []
        addresses = []

        # 批量创建账户
        for _ in range(num_accounts):
            acc = web3.eth.account.create()
            private_keys.append(web3.to_hex(acc.key))
            addresses.append(acc.address)

        # 打印所有的私钥和地址
        print("Private Keys:")
        for key in private_keys:
            print(key)

        print("\nAddresses:")
        for address in addresses:
            print(address)

    def account(self,web3,key):
        """
        :param web3: 实例
        :param key: 私钥
        :return:
        """
        try:
            account = web3.eth.account.from_key(key)
            # print(f"地址：{account.address}")
            return account
        except Exception as e:
            print(e)

    def read_csv(self,csv_path,column_name):
        keys = []
        # 打开 CSV 文件
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            # 创建 CSV 阅读器
            reader = csv.DictReader(file)
            # 读取 'key' 列的所有数据
            for row in reader:
                key_value = row.get(column_name)  # 使用 .get() 来安全获取值
                if key_value:  # 仅当 key 有值时才添加
                    keys.append(key_value)
                else:
                    print(f"警告: 找到一个空值或缺失的 'key' 数据：{row}")
        return keys

    def read_keys(self,dataname,rows):
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建 CSV 文件的完整路径
        csv_path = os.path.join(current_dir,"..","data", dataname)
        # 读取 CSV 文件，跳过标题行，获取第一个密钥
        keys = RpcConnect().read_csv(csv_path, rows)
        return keys

    def get_balance(self,web3,key):
        account = RpcConnect().account(web3, key=key)
        balance = web3.eth.get_balance(account.address)
        print(account.address, f"余额{web3.from_wei(balance, 'ether')}")
        return web3.from_wei(balance, 'ether')

if __name__ == '__main__':
    load_dotenv()
    key = os.getenv("KEY")
    # print("私钥：",key)

    url = "https://testnet-rpc.monad.xyz"
    web3 = RpcConnect().connect_rpc(url)

    # 查询monad余额
    # keys = RpcConnect().read_keys('../data/fat_key.csv','key')
    # for i in keys:
    #     RpcConnect().get_balance(web3,i)



    # 生成wallets.json
    address_list = RpcConnect().read_keys('../data/GoKiteAI_key.csv','address')
    keys = RpcConnect().read_keys('../data/GoKiteAI_key.csv','key')
    print(address_list)
    print(keys)

    # 创建一个字典列表
    address_key_pairs = []

    # 将地址和密钥配对并添加到列表中
    for address, key in zip(address_list, keys):
        address_key_pairs.append({
            "address": address,
            "privateKey": key
        })

    # 将字典列表写入到 JSON 文件
    output_file = 'wallets.json'
    with open(output_file, 'w') as json_file:
        json.dump(address_key_pairs, json_file, indent=2)

    print(f"JSON 文件已生成：{output_file}")