import re
from lxml import html

class tool():
    @staticmethod

    def findall(pattern, string):
        """
        正则查找IP
        :param pattern:
        :param string:
        :return:
        """
        res = []
        try:
            res = re.findall(pattern, string, re.S)
        except Exception as e: print(e)
        return res

    @staticmethod
    def compile(pattern, string):
        """
        替换字符串
        :param pattern:
        :param string:
        :return:
        """
        string = string.strip()
        return re.compile(pattern, re.S).sub('', string)

    @staticmethod
    def xpath(docment, path):
        """
        Xpath 查找
        :param docment:
        :param path:
        :return:
        """
        eobj = html.etree.HTML(docment)
        if eobj is None: return []
        data = eobj.xpath(path)
        return data

    @staticmethod
    def rot13(message):
        """
        字符串解密
        :return:
        """
        res = ''
        for item in message:
            if (item >= 'A' and item <= 'M') or (item >= 'a' and item <= 'm'):
                res += chr(ord(item) + 13)
            elif (item >= 'N' and item <= 'Z') or (item >= 'n' and item <= 'z'):
                res += chr(ord(item) - 13)
            else: res += item
        return res