import asyncio, json, time, random

from aiohttp import TCPConnector, ClientSession
from fake_useragent import UserAgent
from amazon.tools.db import sqlite, redis
from amazon.tools.utils import Rule, Xpath, Tools


class Product():


    def __init__(self, debug=False):
        """
        #初始化
        :param debug:
        """
        self.__debug = debug



    async def __run_(self, task, proxy):
        """
        # 运行查询
        :param task: 每次任务查询所需参数 元组
        :param proxy:代理
        :return:
        """

        # 生成HTTP头 USER AGENT
        headers = {'User-Agent': UserAgent().chrome}
        # 获取COOKIES
        cookies = await self.__cookies_get()
        # 设置异步参数
        connect = TCPConnector(ssl=False, limit=30)
        # 创建会话
        async with ClientSession(connector=connect, headers=headers, cookies=cookies) as session:
            # 获取数据
            message = await self.__fetch_(session, task, proxy)

            if self.__debug and message: print(message)

        # 异步等待
        await asyncio.sleep(random.randint(1,10))



    async def __fetch_(self, session, task, proxy):
        """
        # 获取数据
        :param session:
        :param task:
        :param proxy:
        :return:
        """
        id, asin, seller = task
        #主机
        host = 'https://www.amazon.com'
        #URI
        link = host+'/dp/{}?m={}'.format(asin, seller) if seller else host+'/dp/'+asin
        #发送请求
        try:
            async with session.get(link, proxy=proxy, timeout=10) as resp:

                code = resp.status

                if code not in [200, 201]: return '{}, [{}]HTTP请求失败. 代理:{}'.format(asin, code, proxy)


                html = await resp.text()
                if 'Enter the characters you see below' in html: return '{}, 出现验证码, 代理:{}'.format(asin, proxy)

        except Exception as e: return '{}, {}, 代理:{}'.format(asin, self.__err_handler(e), proxy)

        return await self.__parse(html, session, asin, proxy, id)



    async def __parse(self, html, session, asin, proxy, id):
        """
        # 解析代码
        :param html:
        :param session:
        :param asin:
        :param proxy:
        :param id:
        :return:
        """
        rank = Rule(r"#([\d,]+?) in\s.*?See Top 100 in .*?</a>\)", html).first(default='0').replace(',', '')
        imge = Rule(r'colorImages\'.*?(https.*?)"', html).first()

        ssid = Xpath('//input[@id="session-id"][@name="session-id"]/@value', html).first()
        if not ssid: return '{}, SSID获取失败, 代理:{}'.format(asin, proxy)


        price = Rule(r'id=\"priceblock_ourprice.*?>\$([\d.]+)<', html).first()
        if not price: return '{}, 价格获取失败, 代理:{}'.format(asin, proxy)


        stock = Rule(r'Only (\d+?) left in stock - order soon.', html).first()

        if not stock: stock =await self.__stock_(session, asin, ssid, proxy=proxy)

        #
        if not stock.isdigit(): return stock


        self.__save_(price=price, stock=stock, rank=rank, imge=imge, asin=asin, id=id)



    async def __stock_(self, session, asin, ssid, proxy):
        """
        # 另一种方式查询库存
        :param session:
        :param asin:
        :param ssid:
        :param proxy:
        :return:
        """
        #Post需要提交数据
        data = {'ASIN': asin, 'verificationSessionID': ssid, 'quantity': '99999'}
        #Post地址
        link = 'https://www.amazon.com/gp/add-to-cart/json/ref=dp_start-bbf_1_glance'
        #开始发送
        try:
            async with session.post(link, data=data, proxy=proxy, timeout=8) as resp: html=await resp.text()

            code = resp.status

            if code not in [200,201]: return '{}, HTTP[{}], 代理:{}'.format(link, code, proxy)

            stock= json.loads(html.strip())
            if stock.get('isOK'): return stock.get('cartQuantity')

            return '{}, {}, 代理:{}'.format(asin, stock.get('exception').get('reason'), proxy)

        except Exception as e: return '{}, {}, 代理:{}'.format(link, self.__err_handler(e), proxy)



    async def __cookies_get(self):
        """
        # 查询Cookies
        :return:
        """

        while True:

            try:

                cookies = redis.table('cookies').pop()

            except Exception as e: print(e)



            if cookies: return json.loads(cookies)

            if self.__debug: print('等侍Cookies....')

            await asyncio.sleep(3)

            continue



    def __save_(self, price, stock, rank, imge, asin, id):
        """
        # 保存并更新数据
        :param price:
        :param stock:
        :param rank:
        :param imge:
        :param asin:
        :param id:
        :return:
        """
        sql = 'insert into marks (price,stock,bsr,uptime,asin_id) values ({},{},{},datetime("now"),{})'.format(price,stock,rank,id)
        sqlite.execute(sql)

        sql = 'update listing set status =1, img="{}" where id={}'.format(imge, id)
        sqlite.execute(sql)

        sqlite.commit()

        print('{}, 库存:{}, 价格:{}, 排名:{}'.format(asin, stock, price, rank))



    def __proxy_get(self, condition):
        """
        #查询一条代理
        :return:
        """
        if not condition: return None

        proxy = redis.table('proxies').pop()

        if proxy: return 'http://{}'.format(proxy)

        return None



    def __err_handler(self,e):

        if not e: return '未知错误.'
        return e



    def main(self):
        """
        #入口函数
        :return:
        """

        if sqlite.execute('select count(*) from listing').fetchone()[0] ==0: time.sleep(300)

        loop = asyncio.get_event_loop()

        i = 0
        #下次执行时间戳

        while True:

            i +=1
            # 下次执行剩余
            exe = Tools.next_time_stamp()- Tools.time_stamp_now(t=True)
            #每次查询几香槟酒
            num = random.randint(1,5)

            sql = 'select id,asin,seller from listing where status =0 order by random() limit {}'.format(num)

            res = sqlite.execute(sql).fetchall()

            if not res:

                if exe > 1:

                    print('倒计时: {}秒'.format(exe))
                    time.sleep(10)
                    continue

                sqlite.execute('update listing set status=0')
                sqlite.commit()


            task = [self.__run_(row, self.__proxy_get(i%5)) for row in res]
            loop.run_until_complete(asyncio.wait(task))

            if i > 10000: i = 0






if __name__ == '__main__':



    m = Product(debug=True)

    m.main()




