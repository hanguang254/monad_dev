import os

from dotenv import load_dotenv

from rpc_account import RpcConnect





url = "https://mainnet.base.org"

web3 = RpcConnect().connect_rpc(url)
# 读取私钥
keys = RpcConnect().read_keys("monad_key.csv","key")

ABI = [
{
  "constant": "false",
  "inputs": [
    {
      "name": "recipient",
      "type": "address"
    },
    {
      "name": "amount",
      "type": "uint256"
    }
  ],
  "name": "transfer",
  "outputs": [
    {
      "name": "success",
      "type": "bool"
    }
  ],
  "payable": "false",
  "stateMutability": "nonpayable",
  "type": "function"
},
{
  "constant": "true",
  "inputs": [
    {
      "name": "account",
      "type": "address"
    }
  ],
  "name": "balanceOf",
  "outputs": [
    {
      "name": "balance",
      "type": "uint256"
    }
  ],
  "payable": "false",
  "stateMutability": "view",
  "type": "function"
}


]


load_dotenv()
key = os.getenv("KEY")
print("私钥：", key)

to_account = ""
riz_address = "0xd722E55C1d9D9fA0021A5215Cbb904b92B3dC5d4"
amount = 10*10**18

print(keys)
account = RpcConnect().account(web3,key)
print(account.address)
token_contract = web3.eth.contract(address=riz_address,abi=ABI)
gas = web3.eth.gas_price

# 获取交易的预估 gas
# gas_estimate = token_contract.functions.transfer(account.address, amount).estimate_gas({
#     'from': account.address,
# })
# print(gas_estimate)

balance = token_contract.functions.balanceOf(account.address).call()
print(balance)

# 构建交易
transaction = token_contract.functions.transfer(account.address, 0).build_transaction({
    'chainId': 8453,  # 主网链ID
    'gas': 30000,  # gas 限制
    'gasPrice': web3.to_wei('5', 'gwei'),  # gas价格
    'nonce': web3.eth.get_transaction_count(account.address),  # 获取 nonce
})
# 签名交易
signed_transaction = web3.eth.account.sign_transaction(transaction, key)

# 发送交易
tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

# 输出交易哈希
print(f"交易发送成功，交易哈希: {web3.toHex(tx_hash)}")