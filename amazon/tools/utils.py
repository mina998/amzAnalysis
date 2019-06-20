import datetime, re, time
from lxml import etree
from redis import Redis


class Tools():

    @staticmethod
    def current_time(str='%Y-%m-%d %H:%M:%S'):
        """
        获取当日期时间
        :param str: 日期时间格式
        :return: 日期时间
        """
        return datetime.datetime.now().strftime(str)

    @staticmethod
    def time_stamp_now(t=False):
        """
        获取当前时间戳
        :return:
        """
        if t: return int(time.time())
        return time.time()

    @staticmethod
    def next_time_stamp():
        """
        明天时间戳
        :return:
        """
        # 当天日期
        today    = datetime.date.today()
        # 明天日期
        tomorrow = today + datetime.timedelta(days=1)
        # 转为时间数组
        timeArray = time.strptime(str(tomorrow), "%Y-%m-%d")
        # 转为时间戳
        return int(time.mktime(timeArray))

    @staticmethod
    def sleep(s=1):
        time.sleep(s)


    @staticmethod
    def proxy():
        http =   Redis().rpop('proxies')
        if http: return 'http://'+http.decode('utf-8')
        return http

    @staticmethod
    def log_trace(out, msg):
        if out: print(msg)



class Xpath():

    def __new__(cls, xpath, docment):
        """
        #
        :param xpath:
        :param docment:
        :return:
        """
        if docment:
            tree = etree.HTML(docment)
            cls.result = tree.xpath(xpath)
        else: cls.result = []
        return object.__new__(cls)


    def first(self, default=''):
        """
        # 获取第一个值
        :param default: 如果获取失败, 返回默认值
        :return:
        """
        if not self.result: return default
        return self.result[0]



class Rule():

    def __new__(cls, pattern, docment):
        """
        # 正则获取
        :param pattern: 正则表达式
        :param docment:
        :return:
        """
        cls.result = re.findall(pattern, docment)
        return object.__new__(cls)


    def first(self, default=''):
        """
        # 返回第一个值
        :param default: 获取失败, 返回默认值
        :return:
        """
        if not self.result: return default
        return self.result[0]
