import asyncio, json
from base64 import b64decode
from random import shuffle, sample
from proxies.base import Http
from proxies.tool import tool

class Spider(Http):


    #1
    async def cc_free01(self):

        html = await self.download('https://api.getproxylist.com/proxy')
        if not html: return False
        data = json.loads(html)
        proxy= '{}:{}'.format(data.get('ip'), data.get('port'))
        await self.check(proxy)

    #2
    async def cc_free02(self):

        link = 'http://www.gatherproxy.com/proxylist/anonymity/?t=Elite'
        data = dict(Type='elite', PageIdx=1)
        html = await self.download(link, method='POST', data=data)
        patn = r'<script>document\.write\(\'(\d+\.\d+\.\d+\.\d+)\'\)</script></td>[\s\S]*?<td><script>document\.write\(gp\.dep\(\'(.*?)\'\)\)</script>'
        urls = tool.xpath(html, '//div[@class="pagenavi"]/a/text()')
        shuffle(urls)
        for num in urls:
            data['PageIdx'] = num
            resp = await self.download(link+'#'+num, method='POST', data=data)
            if not resp: continue
            ipv4 = tool.findall(patn, resp+html)
            ipv4 = ['%s:%s' %(ip[0], int(ip[1], 16)) for ip in ipv4]
            html = ''
            for ip in ipv4[0:5]: await self.check(ip)

    #3
    async def cc_free03(self):

        link = 'http://www.gatherproxy.com/proxylist/anonymity/?t=Anonymous'
        data = dict(Type='anonymous', PageIdx=1)
        html = await self.download(link, method='POST', data=data)
        patn = r'<script>document\.write\(\'(\d+\.\d+\.\d+\.\d+)\'\)</script></td>[\s\S]*?<td><script>document\.write\(gp\.dep\(\'(.*?)\'\)\)</script>'
        urls = tool.xpath(html, '//div[@class="pagenavi"]/a/text()')
        shuffle(urls)
        for num in urls:
            data['anonymous'] = num
            resp = await self.download(link+'#'+num, method='POST', data=data)
            if not resp: continue
            ipv4 = tool.findall(patn, resp+html)
            ipv4 = ['%s:%s' %(ip[0], int(ip[1], 16)) for ip in ipv4]
            html = ''
            for ip in ipv4: await self.check(ip)

    #4
    async def cc_free04(self):

        for url in ['https://free-proxy-list.net/', 'https://www.us-proxy.org/']:
            res = await self.download(url)
            ptn = r'<td>(\d+\.\d+\.\d+\.\d+?)</td><td>(\d+?)</td>'
            ips = tool.findall(ptn, res)
            for ip in ips: await self.check('{}:{}'.format(ip[0], ip[1]))

    #5
    async def cc_free05(self):

        link = 'https://www.proxynova.com/proxy-server-list/'
        html = await self.download(link)
        urls = tool.xpath(html, '//div[@class="dropdown"]/div[@class="col3 clearfix"]/ul/li/div/a/@href')
        shuffle(urls)
        for uri in urls:
            url = 'https://www.proxynova.com'+uri
            res = await self.download(url)
            ptn = "write\('12345678([\d\.]+?)'\.substr\(8\)\s\+\s'([\d\.]+?)'\);</script>\s</abbr>[\s\S]*?</td>[\s\S]*?<td align=\"left\">([\s\S]+?)</td>"
            ips = tool.findall(ptn, res+html)
            ips = ['{}{}:{}'.format(ip[0], ip[1], tool.compile(r'<[^>]+>', ip[2])) for ip in ips]
            for ip in ips: await self.check(ip)
            html=''
            await asyncio.sleep(1)

    #6
    async def cc_free06(self):

        link = 'https://www.xroxy.com/proxy-country/'
        html = await self.download(link)
        urls = tool.xpath(html, '//div[@class="wpb_wrapper"]//ul/li/a/@href')
        shuffle(urls)
        for url in urls:
            res = await self.download(url)
            ptn = '<td tabindex="0" class="sorting_1">(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?<td>(\d+?)</td>'
            ips = tool.findall(ptn, res)
            for ip in ips: await self.check('{}:{}'.format(ip[0], ip[1]))

    #7
    async def cc_free07(self):

        data = locals()
        for n in range(1, 999):
            html = await self.download('https://sockslist.net/proxy/server-socks-hide-ip-address/%s'%n)
            elem = tool.findall(r'<\!\[CDATA\[([^\]]+?)\/', html)
            if not tool.xpath(html, '//*[@id="pages"]/a[last()-1]/text()'): break
            if len(elem) < 1: continue
            rows = tool.findall(r'(\w+) = ([\w\d\^]+);', elem[0])
            # # # # 动态定义变量
            for i in rows: data[i[0]] = eval(i[1] * 1)
            ptrn = r't_ip">(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?write\((.*?)\);'  # 匹配全部
            ipv4 = tool.findall(ptrn, html)
            rows = []
            for ip in ipv4: await self.check('{}:{}'.format(ip[0], eval(ip[1] * 1)))

    #8
    async def cc_free08(self, url='https://www.cool-proxy.net/proxies/http_proxy_list/page'):

        html = await self.download(url)
        ptn = r'str_rot13\("(.*?)"\)\)\)</script></td>[\s\S]*?<td>(\d+?)</td>'
        ips = tool.findall(ptn, html)
        ips = ['{}:{}'.format(b64decode(tool.rot13(ip[0])).decode('utf-8'), ip[1]) for ip in ips if ip[0] and ip[1]]
        for ip in ips[0:4]: await self.check(ip)
        url = tool.xpath(html, '//th[@class="pagination"]/span[@class="next"]/a/@href')
        await asyncio.sleep(1)
        if len(url) > 0: await self.cc_free08('https://www.cool-proxy.net'+url[0])

    #9
    async def cc_free09(self):

        data = {'xpp': 5, 'xf1': 0, 'xf2': 0, 'xf4': 0, 'xf5': 1}
        html = await self.download('http://spys.one/en/http-proxy-list/', method='POST', data=data)
        elem = tool.findall(r'</table><script type="text/javascript">(.*?)</script>', html)
        if len(elem) < 1: return False
        rows = tool.findall(r'(\w+)=([\w\d\^]+);', elem[0])
        # # # 动态定义变量
        data = locals()
        for i in rows: data[i[0]] = eval(i[1] * 1)
        ptn = r'<font class=spy14>(\d+\.\d+\.\d+\.\d+)<script type="text/javascript">document.write\("<font class=spy2>:<\\/font>"\+(.*?)\)</script></font>'  # 匹配全部
        ips = tool.findall(ptn, html)
        for ip in ips:
            rows = ip[1].replace('(', '').replace(')', '').split('+')
            port = ''  # 拼接端口
            for i in rows: port += str(eval(i) * 1)
            await self.check('{}:{}'.format(ip[0], port))

    #0
    async def cc_free10(self):

        data = {'xpp': 5, 'xf1': 0, 'xf2': 0, 'xf4': 0, 'xf5': 1}
        html = await self.download('http://spys.one/en/free-proxy-list/', method='POST', data=data)
        elem = tool.findall(r'</table><script type="text/javascript">(.*?)</script>', html)
        if len(elem) < 1: return False
        rows = tool.findall(r'(\w+)=([\w\d\^]+);', elem[0])
        # # # 动态定义变量
        data = locals()
        for i in rows: data[i[0]] = eval(i[1] * 1)
        ptn = r'<font class=spy14>(\d+\.\d+\.\d+\.\d+)<script type="text/javascript">document.write\("<font class=spy2>:<\\/font>"\+(.*?)\)</script></font>'  # 匹配全部
        ips = tool.findall(ptn, html)
        for ip in ips:
            rows = ip[1].replace('(', '').replace(')', '').split('+')
            port = ''  # 拼接端口
            for i in rows: port += str(eval(i) * 1)
            await self.check('{}:{}'.format(ip[0], port))


#######################################################################
#####################        国内代理         ###########################
#######################################################################

    #1cn
    async def cc_kuaidaili(self, page=26):

        pages = sample(range(1, page+1), page)  # random.sample()生成不相同的随机数
        for n in pages:
            html = await self.download('https://www.kuaidaili.com/free/inha/%s/' % n)
            ptn = r'data-title="IP">(.*?)</td>[\s\S]*?<td data-title="PORT">(.*?)<'
            ips = tool.findall(ptn, html)
            for ip in ips: await self.check('{}:{}'.format(ip[0], ip[1]))
            await asyncio.sleep(5)

    #2cn
    async def cc_xicidaili(self, page=30):
        page = sample(range(1, page + 1), page)  # random.sample()生成不相同的随机数
        for n in page:
            html = await self.download('https://www.xicidaili.com/nt/%s'%n)
            ptn = r'<td>(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?<td>(\d+?)</td>[\s\S]*?<a'
            ips = tool.findall(ptn, html)
            for ip in ips: await self.check('{}:{}'.format(ip[0], ip[1]))
            await asyncio.sleep(3)

        # url = self.xpath(html, '//div[@class="pagination"]/a[@class="next_page"]/@href')
        # if url: await self.cc_xicidaili('https://www.xicidaili.com'+url[0])

    #3cn
    async def cc_89ip(self):

        link = 'http://www.89ip.cn/tqdl.html?api=1&num=500&port=&address=&isp='
        html = await self.download(link)
        ptn = r'(\d+\.\d+\.\d+\.\d+:\d+)'
        ips = tool.findall(ptn, html)
        for ip in ips: await self.check(ip)

    #4cn
    async def cc_free(self):

        res = await self.download('http://lab.crossincode.com/proxy/')
        ptn = r'<td>(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?<td>(\d+?)</td>'
        ips = tool.findall(ptn, res)
        for ip in ips: await self.check('{}:{}'.format(ip[0], ip[1]))




if __name__ == '__main__':
    s = Spider()

    loop = asyncio.get_event_loop()
    task = [s.cc_free()]
    loop.run_until_complete(asyncio.wait(task))














