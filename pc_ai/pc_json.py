from collections import Counter
from datetime import datetime
import requests



# 查询最新数据
def request_data():
  url = 'https://api.8828355.com/test?token=67FBE9D81D36A55D&t=jnd28&rows=50&p=json&date=20250211'
  res =requests.get(url)
  print(res.json())
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
    print("\n".join([str(item) for item in list_data]))
    return list_data



if __name__ == '__main__':
    res = request_data()
    # print(res)
    res_data = kai_data(res)