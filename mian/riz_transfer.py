from rpc_account import RpcConnect





url = "https://base.llamarpc.com"

web3 = RpcConnect().connect_rpc(url)
# 读取私钥
keys = RpcConnect().read_keys("riz_key.csv","key")

ABI = []

to_account = ""
riz_address = ""
amount = 10*10**18

print(keys)

