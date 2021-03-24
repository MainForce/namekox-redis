#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from redis import StrictRedis
from redis._compat import iteritems
from redis.sentinel import Sentinel as BaseSentinel


class Sentinel(BaseSentinel):
    def __init__(self, sentinels, min_other_sentinels=0, sentinel_kwargs=None, **connection_kwargs):
        # if sentinel_kwargs isn't defined, use the socket_* options from
        # connection_kwargs
        self.connection_kwargs = connection_kwargs
        self.min_other_sentinels = min_other_sentinels
        self.sentinel_kwargs = sentinel_kwargs or {
            k: v for k, v in iteritems(connection_kwargs) if k.startswith('socket_')
        }
        self.sentinels = [StrictRedis.from_url(url, **self.sentinel_kwargs) for url in sentinels]
