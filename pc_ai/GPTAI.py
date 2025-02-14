
from openai import OpenAI
client = OpenAI()




def AI_Analysis(text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # system设定角色，知识范围英文最佳
            {
                "role": "system",
                "content": "你是一个资深的彩票分析师，掌握着诸多彩票分析方法，如走势图分析法，折线图走势分析法，非常熟悉加拿大28的开奖规则"
            },
            # 输入的文本内容
            {
                "role": "user",
                "content": f"{text}"
            },
        ]
    )

    print(completion.choices[0].message.content)

if __name__ == '__main__':
    text="我把本地图片转化位base64编码给你 你能查看图片内容吗？"
    # AI_Analysis(text)

