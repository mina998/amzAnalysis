import asyncio
from random import shuffle
from proxies.spider import Spider
from multiprocessing import Process

class Proxy(Spider):

    def crawl(self):

        while True:

            crawls = list(filter(lambda m: m.startswith("cc_"), dir(self)))
            shuffle(crawls)

            task = [getattr(self, func)() for func in crawls]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(task))




    def verify(self):

        while True:
            ips  = self.redis.get(cut=5)
            loop = asyncio.get_event_loop()
            task = [self.check(row.decode('utf-8'), num=3, verify=True) for row in ips]
            loop.run_until_complete(asyncio.wait(task))




    def run(self):

        webapi = Process(target=self.http)
        webapi.start()

        crawls = Process(target=self.crawl)
        crawls.start()

        # verify = Process(target=self.verify)
        # verify.start()







if __name__ == '__main__':

    Proxy().run()
