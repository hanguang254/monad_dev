import json


# 定义读取文件并提取ethereum_address的函数
def extract_ethereum_addresses(input_file, output_file):
    ethereum_addresses = []

    with open(input_file, 'r') as file:
        # 使用一个变量暂存有效JSON内容
        current_json = ""
        for line in file:
            # 如果行包含分隔符，表示下一个钱包数据的开始
            if "---------------------------------------------------" in line:
                # 如果当前暂存的JSON有数据且是有效的，解析并提取ethereum_address
                if current_json.strip():
                    try:
                        data = json.loads(current_json.strip())
                        ethereum_address = data.get('ethereum_address')
                        if ethereum_address:
                            ethereum_addresses.append(ethereum_address)
                    except json.JSONDecodeError as e:
                        print(f"解析JSON错误：{e}")

                # 重置当前的JSON数据为新一段钱包数据
                current_json = ""
            else:
                # 累积每行数据到current_json
                current_json += line

        # 处理文件结尾的最后一个钱包数据
        if current_json.strip():
            try:
                data = json.loads(current_json.strip())
                ethereum_address = data.get('ethereum_address')
                if ethereum_address:
                    ethereum_addresses.append(ethereum_address)
            except json.JSONDecodeError as e:
                print(f"解析JSON错误：{e}")

    # 将提取的ethereum_address写入到输出文件
    with open(output_file, 'w') as output:
        for address in ethereum_addresses:
            output.write(f"{address}\n")

    print(f"提取的ethereum_address已保存到 {output_file}")


# 设置输入和输出文件路径
input_file = '../data/hemi_key.txt'  # 输入文件名（包含200个类似的JSON对象）
output_file = 'ethereum_addresses.txt'  # 输出文件名

# 调用函数提取ethereum_address
extract_ethereum_addresses(input_file, output_file)
