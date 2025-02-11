
from openai import OpenAI
client = OpenAI()




def AI_Analysis():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            # system设定角色，知识范围英文最佳
            {
                "role": "system",
                "content": "You are a lottery analyst and a mathematician with a rich knowledge of probability."
            },
            # 输入参数内容
            {
                "role": "user",
                "content": "你好！"
            }
        ]
    )


    print(completion.choices[0].message)