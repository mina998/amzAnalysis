import asyncio
from multiprocessing import Process
from amazon.cookies import Cookies
from amazon.product import Product


def cookies():

    exe  = Cookies(debug=True)

    loop = asyncio.get_event_loop()
    task = [exe.run() for i in range(5)]
    loop.run_until_complete(asyncio.wait(task))




def prodeut():

    exe = Product(debug=True)
    exe.main()







if __name__ == '__main__':


    task1 = Process(target=cookies)
    task1.start()

    task2 = Process(target=prodeut)
    task2.start()