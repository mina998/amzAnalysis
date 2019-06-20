import sqlite3
from redis import Redis
from conn import SQLITE_DB_URI

client = Redis()
cf = 'stop-writes-on-bgsave-error'
if client.config_get(cf).get(cf) == 'yes': client.config_set(cf, 'no')


class RedisClient():


    def table(self, table):
        """
        # 切换表
        :param table:
        :return:
        """

        self.__table = table
        return self


    def pop(self, left=False):
        """
        从指定方向弹出一条
        :param left:
        :return:
        """
        if left: row = client.lpop(self.__table)
        else: row = client.rpop(self.__table)
        if row: return row.decode('utf-8')
        return None


    def put(self, row, left=True):
        """
        从指定方向添加一条数据
        :param proxy:
        :param left:
        :return:
        """
        if left: return client.lpush(self.__table, row)
        return client.rpush(self.__table, row)


    def count(self):
        """
        统计长度
        :return:
        """
        return client.llen(self.__table)


redis = RedisClient()





class Db(object):
    __instance = None
    sqlite_uri = SQLITE_DB_URI

    def execute(self, sql):
        """
        执行SQL语句
        :param sql:
        :return:
        """
        try:
            return self.__cur.execute(sql)
        except Exception as e:
            print(e)

    def commit(self):
        self.__con.commit()

    def close(self):
        self.__con.close()

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        :param args:
        :param kwargs:
        :return:
        """
        if cls.__instance == None:
            cls.__con = sqlite3.connect(cls.sqlite_uri, timeout=60)
            cls.__cur = cls.__con.cursor()
            cls.__instance = object.__new__(cls)
        return cls.__instance

sqlite = Db()
