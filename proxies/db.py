from random import randint

from redis import Redis

redis = Redis()
cf = 'stop-writes-on-bgsave-error'
if redis.config_get(cf).get(cf) == 'yes': redis.config_set(cf, 'no')


table = 'proxies'


class RedisClient():


    def pop(self, left=False):
        """
        从指定方向弹出一条
        :param left:
        :return:
        """
        if left: row = redis.lpop(table)
        else: row = redis.rpop(table)
        if row: return row.decode('utf-8')
        return None


    def put(self, row, left=True):
        """
        从指定方向添加一条数据
        :param proxy:
        :param left:
        :return:
        """
        if left: return redis.lpush(table, row)
        return redis.rpush(table, row)


    def get(self, cut=0):
        """
        :param cut: 截取删除条数 int
        :return: 随机从右侧15条中返回一条, 如果cut参数大于0 从左侧截取cut条数据并返回
        """
        #从左侧截取cut条数据并返回
        if cut > 0:
            data = redis.lrange(table, 0, cut)
            redis.ltrim(table, cut, -1)
            return data
        #随机从右侧15条中返回一条,
        num = randint(-15, -1)
        row = redis.lindex(table, num)
        row = row.decode() if row else row
        return row


    def count(self):
        """
        统计长度
        :return:
        """
        return redis.llen(table)


    def views(self):
        """
        查看所有数据
        :return:
        """
        return redis.lrange(table, 0, -1)


    def delete(self, value):
        """
        删除表中指定数据
        :param value:
        :return:
        """
        return redis.lrem(table, 0, value)



if __name__ == '__main__':
    db = RedisClient()
    aa = db.count()
    print(aa)

