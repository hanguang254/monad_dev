import csv
import time
from eth_account import Account
from concurrent.futures import ThreadPoolExecutor



def create_wallet_with_prefix(prefix: str) -> tuple:
    """
    生成符合指定前缀的钱包地址（排除 '0x' 比较）
    :param prefix: 钱包地址需要符合的前缀（不包含 '0x'）
    :return: 地址、私钥和助记词
    """
    while True:
        Account.enable_unaudited_hdwallet_features()  # 启用助记词功能
        account, mnemonic = Account.create_with_mnemonic()  # 创建钱包和助记词
        address = account.address[2:].lower()  # 去掉 '0x' 并转为小写
        if address.startswith(prefix.lower()):  # 检查前缀
            return account.address, account.key.hex(), mnemonic


def save_wallet_to_csv(file_name: str, wallet_data: list):
    """
    将钱包数据保存到 CSV 文件中
    :param file_name: CSV 文件名
    :param wallet_data: 包含地址、私钥和助记词的列表
    """
    with open(file_name, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for data in wallet_data:
            writer.writerow(data)


def generate_wallets(prefix: str, num_wallets: int, thread_count: int, file_name: str):
    """
    使用多线程生成符合指定前缀的钱包地址
    :param prefix: 钱包地址的前缀
    :param num_wallets: 需要生成的钱包数量
    :param thread_count: 线程数
    :param file_name: CSV 文件名
    """
    wallet_list = []  # 存储生成的钱包数据
    start_time = time.time()  # 记录开始时间

    def task():
        """单个线程的任务"""
        address, private_key, mnemonic = create_wallet_with_prefix(prefix)
        print(f"生成钱包：{address}")  # 实时打印生成的地址
        return address, private_key, mnemonic

    # 使用线程池生成钱包
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for result in executor.map(lambda _: task(), range(num_wallets)):
            wallet_list.append(result)

    # 保存生成的钱包数据到 CSV
    save_wallet_to_csv(file_name, wallet_list)

    # 打印统计信息
    end_time = time.time()
    print(f"\n生成完成！总共生成 {num_wallets} 个钱包，耗时 {end_time - start_time:.2f} 秒。")
    print(f"钱包信息已保存到文件：{file_name}")


if __name__ == "__main__":
    # prefix = input("请输入钱包地址需要的前缀：")
    prefix = "00"
    # num_wallets = int(input("请输入需要生成的钱包数量："))
    num_wallets = 20
    # thread_count = int(input("请输入线程数量："))
    thread_count = 28

    file_name = "wallet_info_with_prefix_multithread3.csv"  # 保存文件名
    print(f"开始生成 {num_wallets} 个以 '{prefix}' 为前缀的钱包地址，使用 {thread_count} 个线程...")

    generate_wallets(prefix, num_wallets, thread_count, file_name)

