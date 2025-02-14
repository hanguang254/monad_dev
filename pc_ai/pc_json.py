import os
import time
from collections import Counter
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
from GPTAI import AI_Analysis
import matplotlib.pyplot as plt


# 查询最新数据
def request_data(rows):
    load_dotenv()
    token = os.getenv("PCAPI")
    # 获取当前时间并格式化为 'yyyy-mm-dd'
    current_time = datetime.now().strftime("%Y-%m-%d")
    # 去掉连字符
    date = current_time.replace("-", "")
    url = f"https://api.8828355.com/api?token={token}&t=jnd28&rows={rows}&p=json&date={date}"
    # print(url)
    res =requests.get(url)
    # print(res.json())
    # 查询数据
    return res.json()

def create_image():
    '''

    :return: 折线图方法
    '''
    # 设置中文字体（Windows: SimHei, Mac: Songti SC, Linux 需安装字体）
    plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 是 Windows 自带的黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 获取期数个位十位百位
    issue, units, tens, hundreds, sums = image_data()

    # 三组数据
    data1 = units  # 第一组数据
    data2 = tens  # 第二组数据
    data3 = hundreds  # 第三组数据
    data4 = sums
    x_labels = issue

    # 创建折线图
    plt.figure(figsize=(10, 5))

    # 绘制三条折线
    plt.plot(x_labels, data1, marker='o', linestyle='-', color='b', label="个位")
    plt.plot(x_labels, data2, marker='o', linestyle='--', color='r', label="十位")
    plt.plot(x_labels, data3, marker='o', linestyle='-.', color='g', label="百位")
    plt.plot(x_labels, data4, marker='o', linestyle='-.', color='k', label="和值")

    # 在每个数据点上显示数值
    for i in range(len(data1)):
        plt.text(x_labels[i], data1[i], str(data1[i]), ha='right', va='bottom', fontsize=10, color='blue')
        plt.text(x_labels[i], data2[i], str(data2[i]), ha='center', va='bottom', fontsize=10, color='red')
        plt.text(x_labels[i], data3[i], str(data3[i]), ha='right', va='bottom', fontsize=10, color='green')
        plt.text(x_labels[i], data4[i], str(data4[i]), ha='right', va='top', fontsize=15, color='k')

    # 限制 X 轴标签的显示间隔
    plt.xticks(x_labels[::3])  # 每隔两个显示一个标签（你可以调整间隔数字）

    # 添加标题和标签
    plt.title("最新的30期走势图")
    plt.xlabel("期数")
    plt.ylabel("值")
    plt.legend()  # 显示图例

    # 保存图片
    image_path = "image.png"
    plt.savefig(image_path)
    # plt.show()

    print(f"图片已保存: {image_path}")
    # 文字描述部分
    description = generate_description(x_labels, data1, data2, data3, data4)
    print(description)
    return description


def generate_description(x_labels, data1, data2, data3, data4):
    '''生成图表的文字描述'''
    description = "图表描述：\n"
    description += "本图展示了最新30期的数据趋势，分别为个位、十位、百位和和值四组数据。（从左往右读）\n"

    # 描述各组数据的走势
    description += "1. 个位数据趋势：\n"
    description += f"   {data1}，从期数 {x_labels[0]} 到 {x_labels[-1]}，出现了{get_trend(data1)}的变化。\n"

    description += "2. 十位数据趋势：\n"
    description += f"   {data2}，十位数据从期数 {x_labels[0]} 到 {x_labels[-1]}，表现出{get_trend(data2)}的趋势。\n"

    description += "3. 百位数据趋势：\n"
    description += f"   {data3}，百位数据在这30期内，展示了{get_trend(data3)}的变化。\n"

    description += "4. 和值数据趋势：\n"
    description += f"   {data4}，和值数据呈现出{get_trend(data4)}的走势。\n"

    return description


def get_trend(data):
    '''分析数据的趋势（升、降、波动）'''
    if data[0] < data[-1]:
        return "上升"
    elif data[0] > data[-1]:
        return "下降"
    else:
        return "波动"

def image_data():
    res = request_data(30)
    # print(res)
    data = res["data"]
    Issue=[]
    Units=[]
    Tens=[]
    Hundreds=[]
    Sums =[]
    for i in data:
        qishu = i['drawIssue']
        # 拆分字符串并转换为整数列表
        opencode_list = list(map(int, i['opencode'].split(',')))
        # 计算和值
        opencode_sum = sum(opencode_list)
        unit = list(map(int, i['opencode'].split(',')))[2]
        ten = list(map(int, i['opencode'].split(',')))[1]
        hund =list(map(int, i['opencode'].split(',')))[0]
        # print(unit)
        Issue.append(qishu)
        Units.append(unit)
        Tens.append(ten)
        Hundreds.append(hund)
        Sums.append(opencode_sum)
    Issue.reverse()
    Units.reverse()
    Tens.reverse()
    Hundreds.reverse()
    Sums.reverse()
    # print(Issue,Units,Tens,Hundreds,hezhi)
    return Issue, Units, Tens, Hundreds, Sums


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

    # print(f"返回数据：{list_data}")
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


def main():
    cishu = 0
    old_res = []

    while True:
        cishu += 1
        try:
            # 获取当前时间
            now = datetime.now()
            print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")

            # 请求最新数据
            res = request_data(50)
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
                    # 生成走势图
                    description = create_image()
                    # AI分析
                    send_text = (f'{res_data}这是jnd28最新50期数开奖，规则（每位数的范围是0到9，杂六就是三位数字不一样，且不是顺子，和值大于13就是大小于14就是小）'
                                 f'这是最新20期的折现走势图的文字描述【{description}】冷静理想的分析预测下一期'
                                 f'给出预测杂六与与和值是大是小的概率百分比！并且用中文回答')
                    AI_Analysis(send_text)
                else:
                    print(
                        "--------------------------------新老数据一样不符合分析条件-------------------------------------------")
            else:
                print("最新", request_data(1)["data"])
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

if __name__ == '__main__':
    main()
    # create_image()
    # image_data()