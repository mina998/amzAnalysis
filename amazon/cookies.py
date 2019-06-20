import asyncio, json, random
from random import choice
from aiohttp import ClientSession
from fake_useragent import UserAgent
from amazon.tools.db import redis


class Cookies():



    def __init__(self, zip=10001, debug=False):
        """
        # 初始化
        :param debug:
        """
        self.__debug = debug
        self.__zip = zip



    async def run(self):
        """
        # 运行入口函数
        :return:
        """
        while True:

            if redis.table('cookies').count()> 50:
                if self.__debug: print('Cookies 池已满...')
                await asyncio.sleep(9)
                continue

            # 创建请求头 用户代理
            headers = {'User-Agent': UserAgent().chrome}
            # 设置回话
            async with ClientSession(headers=headers) as session:
                # 获取数据
                message = await self.__get_(session)
                if message and self.__debug: print(message)
            #
            await asyncio.sleep(random.randint(2,10))



    async def __get_(self, session):
        """
        #获取基本Cookies
        :param session: 会话
        :return:
        """
        urls = [
            'https://www.amazon.com/gp/goldbox?ref_=nav_cs_gb_azl',
            'https://www.amazon.com/b/ref=gc_surl_giftcards?node=2238192011',
            'https://www.amazon.com/ref=nav_logo',
            'https://www.amazon.com/gp/help/customer/display.html?nodeId=508510&ref_=nav_cs_help',
            'https://www.amazon.com/b/?_encoding=UTF8&ld=AZUSSOA-sell&node=12766669011&ref_=nav_cs_sell',
            'https://www.amazon.com/Outlet/b/?ie=UTF8&node=517808&ref_=sv_subnav_goldbox_3'
        ]
        try:
            async with session.get(choice(urls)) as index: cookies = index.cookies

        except Exception as e: return '请求失败: {}'.format(e)

        if not cookies.get('session-id'): return 'Session ID 获取失败.'

        await asyncio.sleep(1)

        return await self.__post_(session)



    async def __post_(self, session):
        """
        # 切换城市 获取必要Cookies
        :param session:
        :return:
        """
        link = 'https://www.amazon.com/gp/delivery/ajax/address-change.html'
        data = {
            'locationType': 'LOCATION_INPUT',
            'zipCode': self.__zip,
            'storeContext': 'generic',
            'deviceType': 'web', 'pageType': 'Gateway',
            'actionSource': 'glow'
        }

        try:
            async with session.post(link, data=data) as cidy: cookies = cidy.cookies

        except Exception as e: return 'POST失败: {}'.format(e)

        if not cookies.get('ubid-main'): return 'UBID 获取失败...'

        data = {cookie.key:cookie.value for cookie in cookies.values()}

        if self.__debug: print('Ubid:', data['ubid-main'])

        string  = json.dumps(data)

        redis.table('cookies').put(string)






if __name__ == '__main__':


    amz = Cookies(debug=True)

    loop = asyncio.get_event_loop()
    task = [amz.run() for i in range(5)]
    loop.run_until_complete(asyncio.wait(task))