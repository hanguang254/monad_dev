import base64

from openai import OpenAI
client = OpenAI()




def AI_Analysis(text,imgname):
    # 本地图片转base64字符串
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(imgname)

    completion = client.chat.completions.create(
        model="gpt-4.5-preview",
        messages=[
            # system设定角色，知识范围英文最佳
            {
                "role": "system",
                "content": "你是一个资深的彩票分析师，掌握着诸多彩票分析方法，如走势图分析法，折线图走势分析法，非常熟悉加拿大28的开奖规则"
            },
            # 输入的文本内容
            # {
            #     "role": "user",
            #     "content": f"{text}"
            # },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{text}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        },
                    },
                ]
            }
        ]
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


if __name__ == '__main__':
    # text="我应该怎么上传图片给openapi的sdk调用接口对图片进行分析呢"
    text = "请分析图片上的彩票走势图，预测加拿大28下一期的可能结果"
    AI_Analysis(text,'image.png')
    # upload_img("image.png")
