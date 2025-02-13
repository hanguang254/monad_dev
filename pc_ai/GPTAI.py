
from openai import OpenAI
client = OpenAI()
import matplotlib.pyplot as plt

def AI_image():
    # 设置中文字体（Windows: SimHei, Mac: Songti SC, Linux 需安装字体）
    plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 是 Windows 自带的黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    # 数据
    data = [10, 20, 4, 17, 18, 13]
    x_labels = range(1, len(data) + 1)

    # 创建折线图
    plt.figure(figsize=(6, 4))
    plt.plot(x_labels, data, marker='o', linestyle='-', color='b', label="数据趋势")

    # 添加数据标签（在每个点上显示数值）
    for i, txt in enumerate(data):
        plt.text(x_labels[i], data[i], str(txt), ha='right', va='bottom', fontsize=10, color='black')

    # 添加标题和标签
    plt.title("数据趋势折线图")
    plt.xlabel("索引")
    plt.ylabel("值")
    plt.legend()

    # 保存图片
    image_path = "trend_chart.png"
    plt.savefig(image_path)

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