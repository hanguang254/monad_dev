import os
from collections import Counter
from datetime import datetime
import requests
from dotenv import load_dotenv


# 查询最新数据
def request_data():
    load_dotenv()
    url = os.getenv("PCAPI")
    res =requests.get(url)
    # print(res.json())
    # 查询数据
    return res.json()



def kai_data(data):
    res = data['data']
    list_data =[]
    for i in res:

        x =""
        # print(i)
        qishu = i['drawIssue']
        opentime =datetime.fromtimestamp(float(i['opentime'])).strftime('%Y-%m-%d %H:%M:%S')
        opencode=i['opencode']
        # 拆分字符串并转换为整数列表
        opencode_list = list(map(int, opencode.split(',')))
        # 计算和值
        opencode_sum = sum(opencode_list)
        # 使用 Counter 来计算每个数字出现的次数
        counter = Counter(opencode_list)

        # 判断是否有任何数字的出现次数 >= 3
        if any(count >= 3 for count in counter.values()):
            has_three_equal = True  # 有三位相等的数字
            x="豹子"
        # 判断是否有重复的数字
        elif len(opencode_list) != len(set(opencode_list)):
            has_duplicate = True  # 有重复数字
            x = "对子"
        else:
            has_duplicate = False  # 没有重复数字
            x = "杂六"
        # 将结果添加到列表
        list_data.append([opentime, f"期数：{qishu}", f"开奖：{opencode}",f"和值：{opencode_sum}",x])
    # print("\n".join([str(item) for item in list_data]))
    print(list_data)
    return list_data

def find_first_two_zaliu(data):
    # 存储符合条件的记录
    result = []

    # 遍历处理后的数据列表
    for i in range(len(data) - 1):
        # 获取前两个数组的最后一个元素（类型）
        if data[i][-1] == "杂六" and data[i + 1][-1] == "杂六":
            result.append([data[i], data[i + 1]])

    return result


if __name__ == '__main__':
    try:
        res = request_data()
        # print(res)
        res_data = kai_data(res)
        # 查找前两个数组的最后一个元素都是"杂六"的记录
        result = find_first_two_zaliu(res_data)
        print("\n".join([str(item) for item in result]))
        if len(result)>=2:
            # AI分析
            pass
    except Exception as e:
        print(e)