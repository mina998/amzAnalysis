import asyncio
from multiprocessing import Process
from random import shuffle

from amazon.cookies import Cookies
from amazon.product import Product
from proxies.main import Proxy
from web.app import app


debug = True


def service():

    app.debug = 1
    app.run(host='127.0.0.1',port=1082)



proxy = Proxy()
def proxies():

    while True:
        crawls = list(filter(lambda m: m.startswith("cc_"), dir(proxy)))
        shuffle(crawls)
        task = [getattr(proxy, func)() for func in crawls]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task))


def verify():

    while True:
        ips  = proxy.redis.get(cut=5)
        loop = asyncio.get_event_loop()
        task = [proxy.check(row.decode('utf-8'), num=3, verify=True) for row in ips]
        loop.run_until_complete(asyncio.wait(task))



def cookies():

    exe  = Cookies(debug=debug)

    loop = asyncio.get_event_loop()
    task = [exe.run() for i in range(5)]
    loop.run_until_complete(asyncio.wait(task))




def prodeut():

    exe = Product(debug=debug)
    exe.main()





if __name__ == '__main__':


#运行WEB服务器
    task0 = Process(target=service)
    task0.start()


#抓取代理
    task1 = Process(target=proxies)
    task1.start()

    # 验证过多无效代理
    task2 = Process(target=verify)
    task2.start()

    # 代理提取API
    task3 = Process(target=proxy.http)
    task3.start()


#获取COOKIES
    task4 = Process(target=cookies)
    task4.start()

    # 抓取数据
    task5 = Process(target=prodeut)
    task5.start()




