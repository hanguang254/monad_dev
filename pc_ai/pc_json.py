import os
import time
from collections import Counter
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from GPTAI import AI_Analysis


# 查询最新数据
def request_data():
    load_dotenv()
    token = os.getenv("PCAPI")
    # 获取当前时间并格式化为 'yyyy-mm-dd'
    current_time = datetime.now().strftime("%Y-%m-%d")
    # 去掉连字符
    date = current_time.replace("-", "")
    url = f"https://api.8828355.com/api?token={token}&t=jnd28&rows=100&p=json&date={date}"
    # print(url)
    res =requests.get(url)
    # print(res.json())
    # 查询数据
    return res.json()


def kai_data(data):
    res = data['data']
    list_data = []
    for i in res:
        qishu = i['drawIssue']
        opentime = i["opentime"]
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
    cishu = 0
    old_res = []

    while True:
        cishu += 1
        try:
            # 获取当前时间
            now = datetime.now()
            print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")

            # 请求最新数据
            res = request_data()
            # 处理数据
            res_data = kai_data(res)
            print("--------------------------------已处理后的数据-------------------------------------------")
            # print("\n".join([str(item) for item in res_data]))

            print(f"--------------------------------第{cishu}次获取数据-------------------------------------------")

            # 查找前两个数组的最后一个元素都是"杂六"的记录
            new_res = find_first_two_zaliu(res_data)
            print("捕捉数据", new_res)

            # 如果发现连续相同的"杂六"机会
            if len(new_res) > 0:
                if new_res != old_res:
                    # print(new_res)
                    # print(old_res)
                    print("--------------------------------出现连续机会-------------------------------------------")
                    print("\n".join([str(item) for item in new_res]))
                    print("--------------------------------进行AI分析-------------------------------------------")
                    # AI分析
                    send_text = (f'{res_data}这是jnd28最新100期数开奖，'
                                 f'请根据个位十位百位号码走势图，利用走势分析法、或者每位的折线图进行预测下一期开杂六的概率有多大（杂六为三位数字都不同也不是顺数）'
                                 f'并且结合和值开奖走势分析，综合评断下期杂六的概率有多大')
                    AI_Analysis(send_text)
                else:
                    print(
                        "--------------------------------新老数据一样不符合分析条件-------------------------------------------")
            else:
                print(
                    "--------------------------------未捕捉到数据-------------------------------------------")
            # 更新 old_res，只有在新数据符合条件时才更新
            old_res = new_res

        except EOFError as e:
            print(e)

        # 计算下一次执行的时间（当前时间加1分钟）
        next_run_time = now + timedelta(minutes=1)
        print(f"下次执行时间: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"--------------------------------第{cishu}次执行-------------------------------------------")

        # 计算当前时间和下次执行时间的差值（秒数）
        time_to_wait = (next_run_time - datetime.now()).total_seconds()

        # 等待直到下次执行时间
        time.sleep(time_to_wait)