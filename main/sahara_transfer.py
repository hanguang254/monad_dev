import os

from dotenv import load_dotenv

from rpc_account import RpcConnect


abi = [
	{
		"anonymous": "false",
		"inputs": [
			{
				"indexed": "true",
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": "true",
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"anonymous": "false",
		"inputs": [
			{
				"indexed": "false",
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"indexed": "false",
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "Withdraw",
		"type": "event"
	},
	{
		"stateMutability": "payable",
		"type": "fallback"
	},
	{
		"inputs": [],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "deposit",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "depositquota",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address[]",
				"name": "recipients",
				"type": "address[]"
			},
			{
				"internalType": "uint256[]",
				"name": "amounts",
				"type": "uint256[]"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"stateMutability": "payable",
		"type": "receive"
	}
]


def deposit(amount , gaslimit=1000000):
    # amount_in_ether = 49  # 转账金额（单位：ETH）
    amount_in_wei = web3.to_wei(amount, 'ether')

    # 获取当前的 gas price
    gas_price = web3.eth.gas_price
    transaction = {
        'to': "0xf1F7B7E3b9bD45e83C06f5B18B029DF69a7c5b61",
        'value': amount_in_wei,
        'gas': gaslimit,  # 设置 gas 限额（可以根据实际情况调整）
        'gasPrice': web3.to_wei(2, 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),  # 获取当前账户的 nonce
        'chainId': 313313  # 1 为主网，若是测试网，需要调整
    }

    # 使用私钥签名交易
    signed_transaction = web3.eth.account.sign_transaction(transaction, key)

    # 发送已签名的交易
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    # 输出交易哈希
    print(f"交易已发送，交易哈希: {tx_hash.hex()}")

    # 监听交易确认
    print("等待交易确认...")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt["status"] == 1:
        print("存款成功")
    else:
        print(tx_receipt)


def transfer(address,amount, gaslimit=1000000):
    token_contract = web3.eth.contract(address="0xf1F7B7E3b9bD45e83C06f5B18B029DF69a7c5b61",abi=abi)
    tranfer_transaction = token_contract.functions.transfer(address,amount).build_transaction({
        'from': account.address,
        'gas': gaslimit,  # 可以根据实际情况调整
        'gasPrice': web3.to_wei(2, 'gwei'),  # 获取当前 gas price
        'nonce': web3.eth.get_transaction_count(account.address),  # 获取当前账户的 nonce
        'chainId': 313313  # 1 为主网，若是测试网，需要调整
    })

    # 签名交易
    signed_transaction = web3.eth.account.sign_transaction(tranfer_transaction, key)

    # 发送交易
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

    # 输出交易哈希
    print(f"交易发送成功，交易哈希: {web3.to_hex(tx_hash)}")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt["status"] == 1:
        print("发送交易成功")
    else:
        print(tx_receipt)


def withdraw(key,gaslimit=1000000):
    token_contract = web3.eth.contract(address="0xf1F7B7E3b9bD45e83C06f5B18B029DF69a7c5b61", abi=abi)
    balance = token_contract.functions.balanceOf().call()
    print(balance)
    withdraw_transaction = token_contract.functions.withdraw(balance).build_transaction({
        'from': account.address,
        'gas': gaslimit,  # 可以根据实际情况调整
        'gasPrice': web3.to_wei(2, 'gwei'),  # 获取当前 gas price
        'nonce': web3.eth.get_transaction_count(account.address),  # 获取当前账户的 nonce
        'chainId': 313313  # 1 为主网，若是测试网，需要调整
    })
    # 签名交易
    signed_transaction = web3.eth.account.sign_transaction(withdraw_transaction, key)

    # 发送交易
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    # 输出交易哈希
    print(f"交易发送成功，交易哈希: {web3.to_hex(tx_hash)}")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if tx_receipt["status"] == 1:
        print("提款成功")
    else:
        print(tx_receipt)

if __name__ == '__main__':
        # 本地环境测试
        load_dotenv()
        key = os.getenv("KEY")
        # print("私钥：", key)

        url = "https://testnet.saharalabs.ai"
        web3 = RpcConnect().connect_rpc(url)
        account = RpcConnect().account(web3,key)
        # print("地址：", account.address)

        # 合约存款
        deposit(2.7,gaslimit=200000)

        address_list = RpcConnect().read_csv("../data/address.csv","address")

        # print(address_list)
        # 根据 address_list 的长度生成对应的 amount 数组
        amount_in_wei = web3.to_wei(0.1, 'ether')
        amount = [amount_in_wei] * len(address_list)
        # print(amount)
        # 分发方法
        transfer(address_list,amount,gaslimit=2000000)

        #提款
        # withdraw(key)