import random


class Proxies:

    def load_proxies(self):
        '''

        :return:读取代理ip文件
        '''
        with open("../data/proxies.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    # 随机选择代理
    def get_random_proxy(self):
        '''

        :return: 随机选择ip
        '''
        proxies_list = Proxies().load_proxies()
        if proxies_list:
            proxy = random.choice(proxies_list)
            return {"http": proxy, "https": proxy}
        return None  # 没有代理则返回 None