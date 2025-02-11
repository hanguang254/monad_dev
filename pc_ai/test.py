import requests
import hashlib
import time


def generate_sign(params, secret_key):
    """
    根据参数和密钥生成签名
    :param params: 请求参数的字典
    :param secret_key: 密钥
    :return: 生成的签名
    """
    # 1. 过滤空值参数，并按字典序排序
    sorted_params = sorted((k + str(v) for k, v in params.items() if v), key=lambda x: x[0])

    # 2. 拼接排序后的参数
    sign_str = ''.join(sorted_params) + secret_key

    # 3. 计算 MD5 哈希值
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    return sign


def main():
    appid = "41442"  # 您的应用ID
    secret_key = "eea95ab82ec186ad4eb1a0d0d01bb6a9"  # 您的密钥
    format_type = "json"  # 返回数据格式
    current_time = str(int(time.time()))  # 当前时间戳

    # 请求参数
    params = {
        "appid": appid,
        "format": format_type,
        "time": current_time
    }

    # 生成签名
    sign = generate_sign(params, secret_key)
    params["sign"] = sign

    # 发送 GET 请求
    url = "https://qayz.api.storeapi.net/api/119/259"
    response = requests.get(url, params=params)

    # 输出返回结果
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"请求失败，状态码：{response.status_code}")


if __name__ == "__main__":
    main()
