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
    list_data = []
    for i in res:
        qishu = i['drawIssue']
        opentime = datetime.fromtimestamp(float(i['opentime'])).strftime('%Y-%m-%d %H:%M:%S')
        opencode = i['opencode']

        # 拆分字符串并转换为整数列表
        opencode_list = list(map(int, opencode.split(',')))
        # 计算和值
        opencode_sum = sum(opencode_list)
        # 使用 Counter 计算数字出现次数
        counter = Counter(opencode_list)

        x = ""  # 初始化开奖类型

        # 判断豹子（三个数字相同）
        if any(count == 3 for count in counter.values()):
            x = "豹子"

        # 判断对子（有两个相同数字）
        elif any(count == 2 for count in counter.values()):
            x = "对子"

        else:
            # 处理顺子（考虑 0 既可以是 0 也可以当作 10）
            sorted_nums = sorted(opencode_list)

            # **核心逻辑：判断顺子的两种情况**
            # 1. **正常顺子判断**（如 1,2,3 或 7,8,9）
            is_shunzi = sorted_nums[2] - sorted_nums[0] == 2 and sorted_nums[1] - sorted_nums[0] == 1

            # 2. **包含 0 的特殊顺子判断**
            # - "0,1,2" 视为顺子
            # - "8,9,0" 视为 "8,9,10" 也是顺子
            if 0 in sorted_nums:
                temp_nums = [10 if num == 0 else num for num in sorted_nums]  # 把 0 变成 10
                temp_nums.sort()
                is_shunzi = is_shunzi or (temp_nums[2] - temp_nums[0] == 2 and temp_nums[1] - temp_nums[0] == 1)

            if is_shunzi:
                x = "顺子"
            else:
                x = "杂六"

        # 将结果添加到列表
        list_data.append([opentime, f"期数：{qishu}", f"开奖：{opencode}", f"和值：{opencode_sum}", x])

    print(f"返回数据：{list_data}")
    return list_data

def find_first_two_zaliu(data):
    # 存储符合条件的记录
    result = []
    # 检查前两个元素的最后一个类型是否都是 "杂六"
    if len(data) > 1 and data[0][-1] == "杂六" and data[1][-1] == "杂六":
        result.append(data[0])
        result.append(data[1])

    # print(result)
    return result



if __name__ == '__main__':
    try:
        res = request_data()
        # print(res)
        res_data = kai_data(res)
        print("--------------------------------处理后的数据-------------------------------------------")
        print("\n".join([str(item) for item in res_data]))
        print("--------------------------------分割线-------------------------------------------")
        # 查找前两个数组的最后一个元素都是"杂六"的记录
        result = find_first_two_zaliu(res_data)
        print("捕捉数据",result)
        if len(result)>0:
            print("--------------------------------出现连续机会-------------------------------------------")
            print("\n".join([str(item) for item in result]))
            print("--------------------------------进行AI分析-------------------------------------------")
            # AI分析
        else:
            print("--------------------------------不满足条件等待机会-------------------------------------------")
    except EOFError as e:
        print(e)