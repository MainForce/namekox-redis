#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from namekox_redis.core.proxy import RedisDBProxy


class RedisDB(object):
    def __init__(self, config):
        self.config = config
        self.proxy = RedisDBProxy(config)

    @classmethod
    def name(cls):
        return 'redisdb'
