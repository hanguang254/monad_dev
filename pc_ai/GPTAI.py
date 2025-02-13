
from openai import OpenAI
client = OpenAI()
import matplotlib.pyplot as plt

def AI_image():
    # 设置中文字体（Windows: SimHei, Mac: Songti SC, Linux 需安装字体）
    plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 是 Windows 自带的黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 三组数据
    data1 = [10, 20, 4, 17, 18, 13]  # 第一组数据
    data2 = [15, 25, 10, 22, 16, 19]  # 第二组数据
    data3 = [5, 12, 8, 14, 20, 15]  # 第三组数据
    data4= [4,9,2,10,23,24]
    x_labels = range(1, len(data1) + 1)  # X 轴索引（1, 2, 3, ...）

    # 创建折线图
    plt.figure(figsize=(8, 5))

    # 绘制三条折线
    plt.plot(x_labels, data1, marker='o', linestyle='-', color='b', label="数据组 1")
    plt.plot(x_labels, data2, marker='o', linestyle='--', color='r', label="数据组 2")
    plt.plot(x_labels, data3, marker='o', linestyle='-.', color='g', label="数据组 3")
    plt.plot(x_labels, data4, marker='o', linestyle='-.', color='k', label="数据组 4")

    # 在每个数据点上显示数值
    for i in range(len(data1)):
        plt.text(x_labels[i], data1[i], str(data1[i]), ha='right', va='bottom', fontsize=10, color='blue')
        plt.text(x_labels[i], data2[i], str(data2[i]), ha='center', va='bottom', fontsize=10, color='red')
        plt.text(x_labels[i], data3[i], str(data3[i]), ha='right', va='bottom', fontsize=10, color='green')
        plt.text(x_labels[i], data4[i], str(data4[i]), ha='right', va='top', fontsize=15, color='k')

    # 添加标题和标签
    plt.title("三组数据趋势折线图")
    plt.xlabel("索引")
    plt.ylabel("值")
    plt.legend()  # 显示图例

    # 保存图片
    image_path = "multi_trend_chart.png"
    plt.savefig(image_path)
    plt.show()

    print(f"图片已保存: {image_path}")


def AI_Analysis(text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # system设定角色，知识范围英文最佳
            {
                "role": "system",
                "content": "你是一个资深的彩票分析师，掌握着诸多彩票分析方法，如走势图分析法，折线图走势分析法，非常熟悉加拿大28"
            },
            # 输入参数内容
            {
                "role": "user",
                "content": f"{text}"
            }
        ]
    )

    print(completion.choices[0].message.content)

if __name__ == '__main__':
    # text=""
    # AI_Analysis(text)
    AI_image()