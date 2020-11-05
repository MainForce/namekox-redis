#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from redis import StrictRedis
from redis.sentinel import Sentinel as BaseSentinel


class Sentinel(BaseSentinel):
    def __init__(self, sentinels, min_other_sentinels=0, sentinel_kwargs=None, **connection_kwargs):
        super(Sentinel, self).__init__(
            sentinels, min_other_sentinels=min_other_sentinels,
            sentinel_kwargs=sentinel_kwargs, **connection_kwargs)
        self.sentinels = [StrictRedis.from_url(url, **self.sentinel_kwargs) for url in sentinels]
