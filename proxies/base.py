import asyncio, time
from random import sample
from aiohttp import ClientSession, web
from fake_useragent import UserAgent
from proxies.db import RedisClient


class Http():
    redis = RedisClient()


    async def __proxy(self, request):
        """
        # WEB API 查询一条数据
        :param request:
        :return:
        """
        if request.query.get('m') == 'mina998':
            proxy = self.redis.pop()
        else: proxy = None

        return web.json_response({'http':proxy, 'https': proxy})



    async def __count(self, request):
        """
        # WEB API 统计获取数量
        :param request:
        :return:
        """
        count = self.redis.count()
        return web.Response(text='%s'%count)



    def http(self):

        routes = [
            web.get('/', self.__proxy),
            web.get('/count', self.__count)
        ]

        app = web.Application()
        app.add_routes(routes)
        web.run_app(app, host='0.0.0.0', port=88)



    async def download(self, url, method='GET', data=None):
        """
        #网页下载器
        :param url: 网页链接 字符串
        :param method: 请求方法 字符串
        :param data: POST请求发送数据 字典
        :return: 字符串
        """
        headers = {'User-Agent': UserAgent().chrome}
        async with ClientSession(headers=headers) as session:
            proxy = self.__proxy_get()
            print(url)
            for i in range(5):
                try:
                    async with session.request(method, url, data=data, proxy=proxy, verify_ssl=False) as response:
                        if response.status in [200, 201]: return await response.text()
                except Exception as e: print('Request Failed:', e)

                if i > 1: proxy = None
        return ''


    async def check(self, proxy, num=1, verify=False):
        """
        # 验证代理有效性 并保存
        :param proxy: 代理IP 字符串
        :param num: 验证时所请求的页数, 最大
        :return:
        """

        # 检测代理池是已满
        while True:

            if self.redis.count() > 200:
                print('代理池已满.....')
                time.sleep(60)
                continue
            else: break

        # 检测所获代理数量是否达标, 如达标就验证
        while verify:

            if self.redis.count() < 100:
                print('等侍验证.....')
                time.sleep(3600)
                continue
            else: break



        headers = {'User-Agent': UserAgent().chrome}

        async with ClientSession(headers=headers) as session:
            status = 0
            for url in self.__verify_page_url(num):
                try:
                    async with session.get(url, proxy='http://'+proxy, verify_ssl=False, timeout=3) as response:
                        if response.status in [200,201]: status += 1
                except Exception as e: status -= 1
        if status > 0:

            print('有效:', proxy)
            self.redis.put(proxy, left=False)

        else: print('无效:', proxy)


    def __verify_page_url(self, num):
        """
        # 生成代理验证请求链接列表
        :param num: 生成链接数
        :return: 链接列表
        """
        urls = [
            'https://www.amazon.com', 'https://www.etsy.com', 'https://www.ebay.com',
            'https://www.amazon.com/gp/goldbox', 'https://www.amazon.com/amazonprime',
            'https://www.amazon.com/gp/browse.html?node=16115931011',
            'https://www.amazon.com/gp/help/customer/display.html',
        ]
        if num > len(urls) or num < 0: return urls
        return sample(urls, num)


    def __proxy_get(self):
        """
        # 获取代理IP
        :return:
        """
        proxy = self.redis.get()
        proxy = 'http://' + proxy if proxy else proxy
        return proxy