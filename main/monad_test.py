import os

from dotenv import load_dotenv
from rpc_account import RpcConnect




# 创世nft已过期
def verse_mint(key):
    abi = [
        {
            "constant": False,
            "inputs": [],
            "name": "mint",
            "outputs": [],
            "payable": True,
            "stateMutability": "payable",
            "type": "function"
        }
    ]
    contract_address = "0xe25c57fF3EeA05d0F8bE9aaAE3F522DdC803cA4E"
    url = "https://testnet-rpc.monad.xyz"
    web3 = RpcConnect().connect_rpc(url)
    account = RpcConnect().account(web3, key=key)
    balance = web3.eth.get_balance(account.address)
    print(account.address,f"余额{web3.from_wei(balance,'ether')}")
    contract = web3.eth.contract(address=contract_address, abi=abi)

    transaction = contract.functions.mint().build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 100000,
        'gasPrice': web3.eth.gas_price,
        'value': web3.to_wei(0.3, 'ether'),
    })
    # 签名交易
    signed_transaction = web3.eth.account.sign_transaction(transaction, key)

    # 发送交易
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

    # 输出交易哈希
    print(f"交易发送成功，交易哈希: {web3.to_hex(tx_hash)}")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt["status"] == 1:
        print("mint成功")
    else:
        print("mint失败",tx_receipt)


# 铸造盒子
def MonAIbox(key):
    abi = [
        {
            "constant": False,
            "inputs": [
                {
                    "name": "amount",
                    "type": "uint256"
                },
                {
                    "name": "to",
                    "type": "address"
                }
            ],
            "name": "mint",
            "outputs": [],
            "payable": True,
            "stateMutability": "payable",
            "type": "function"
        }
    ]
    contract_address = "0x202F2025D638459b2Eab6EB68bFDa101c46DB972"
    url = "https://testnet-rpc.monad.xyz"
    web3 = RpcConnect().connect_rpc(url)
    account = RpcConnect().account(web3, key=key)
    balance = web3.eth.get_balance(account.address)
    print(account.address, f"余额{web3.from_wei(balance, 'ether')}")
    contract = web3.eth.contract(address=contract_address, abi=abi)

    transaction = contract.functions.mint(1,account.address).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 300000,
        'gasPrice': web3.eth.gas_price,
        'value': web3.to_wei(0.1, 'ether'),
    })
    # 签名交易
    signed_transaction = web3.eth.account.sign_transaction(transaction, key)

    # 发送交易
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

    # 输出交易哈希
    print(f"交易发送成功，交易哈希: {web3.to_hex(tx_hash)}")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt["status"] == 1:
        print("mint成功")
    else:
        print("mint失败", tx_receipt)
# 打开盒子
def openBox(key):
    abi = [
        {
            "constant": False,
            "inputs": [
                {
                    "name": "id",
                    "type": "uint256"
                }
            ],
            "name": "openBox",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    contract_address = "0x202F2025D638459b2Eab6EB68bFDa101c46DB972"
    url = "https://testnet-rpc.monad.xyz"
    web3 = RpcConnect().connect_rpc(url)
    account = RpcConnect().account(web3, key=key)
    balance = web3.eth.get_balance(account.address)
    print(account.address, f"余额{web3.from_wei(balance, 'ether')}")
    contract = web3.eth.contract(address=contract_address, abi=abi)

    transaction = contract.functions.openBox(1).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': web3.eth.gas_price,
        # 'value': web3.to_wei(0.1, 'ether'),
    })
    # 签名交易
    signed_transaction = web3.eth.account.sign_transaction(transaction, key)

    # 发送交易
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

    # 输出交易哈希
    print(f"交易发送成功，交易哈希: {web3.to_hex(tx_hash)}")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt["status"] == 1:
        print("打开成功")
    else:
        print("打开失败", tx_receipt)

if __name__ == '__main__':
    # 本地环境测试
    # load_dotenv()
    # key = os.getenv("KEY")
    # verse_mint(key)
    keys = RpcConnect().read_keys("monad_key.csv", "key")
    for i in keys:
        # MonAIbox(i)
        openBox(i)
