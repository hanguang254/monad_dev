import csv
from mnemonic import Mnemonic

def generate_mnemonics(count=10, strength=128):
    """
    批量生成助记词
    :param count: 生成的数量
    :param strength: 助记词的强度（128 生成 12 词，256 生成 24 词）
    :return: 助记词列表
    """
    mnemo = Mnemonic("english")
    mnemonics = [mnemo.generate(strength=strength) for _ in range(count)]
    return mnemonics

def save_mnemonics_to_csv(mnemonics, filename="mnemonics.csv"):
    """
    将助记词保存到CSV文件
    :param mnemonics: 助记词列表
    :param filename: 保存的文件名
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Mnemonic'])  # 写入表头
        for i, mnemonic in enumerate(mnemonics, 1):
            writer.writerow([i, mnemonic])  # 写入每一组助记词

# 生成 10 组 12 词助记词
mnemonics_list = generate_mnemonics(2)

# 将助记词保存到 CSV 文件
save_mnemonics_to_csv(mnemonics_list)

print("助记词已成功保存到 'mnemonics.csv' 文件中")
