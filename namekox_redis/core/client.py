#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import json


from redis import StrictRedis
from namekox_redis.core.messaging import gen_message_headers


class RedisClient(StrictRedis):
    def __init__(self, *args, **kwargs):
        self.context = None
        super(RedisClient, self).__init__(*args, **kwargs)

    def publish(self, channel, message):
        headers = gen_message_headers(self.context.data) if self.context else {}
        resdata = {'headers': headers, 'message': message}
        return super(RedisClient, self).publish(channel, json.dumps(resdata))

    def __call__(self, context=None):
        self.context = context
        return self
