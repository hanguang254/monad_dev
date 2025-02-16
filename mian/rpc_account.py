
from web3 import Web3
import os
from dotenv import load_dotenv
from eth_account import Account


class RpcConnect():

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

    def create_account(self):
        w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
        acc = w3.eth.account.create()
        print(f'private key={w3.to_hex(acc.key)}, account={acc.address}')

    def account(self,web3,key):
        """
        :param web3: 实例
        :param key: 私钥
        :return:
        """
        try:
            account = web3.eth.account.from_key(key)
            print(f"地址：{account.address}")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    load_dotenv()
    key = os.getenv("KEY")
    print("私钥：",key)
