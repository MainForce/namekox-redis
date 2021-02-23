#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from redis.sentinel import Sentinel as BaseSentinel


from .client import RedisClient


class Sentinel(BaseSentinel):
    def __init__(self, sentinels, min_other_sentinels=0, sentinel_kwargs=None, **connection_kwargs):
        self.context = None
        super(Sentinel, self).__init__(
            sentinels, min_other_sentinels=min_other_sentinels,
            sentinel_kwargs=sentinel_kwargs, **connection_kwargs)
        self.sentinels = [RedisClient.from_url(url, **self.sentinel_kwargs)(self.context) for url in sentinels]

    def __call__(self, context=None):
        self.context = context
        return self
