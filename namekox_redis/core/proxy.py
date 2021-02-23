#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from redis import StrictRedis
from namekox_redis.constants import REDIS_CONFIG_KEY
from namekox_core.core.friendly import AsLazyProperty


from .sentinel import Sentinel


class RedisDBProxy(object):
    def __init__(self, config, **options):
        self.config = config
        self.options = options
        self.connection = None

    @AsLazyProperty
    def uris(self):
        return self.config.get(REDIS_CONFIG_KEY, {})

    def __call__(self, dbname, **options):
        self.options.update(**options)
        duri = self.uris[dbname]
        self.connection = StrictRedis.from_url(duri, **self.options)
        return self.connection


class SentinelDBProxy(object):
    def __init__(self, config, **options):
        self.config = config
        self.options = options
        self.sentinel = None

    @AsLazyProperty
    def uris(self):
        return self.config.get(REDIS_CONFIG_KEY, {})

    def __call__(self, dbname, **options):
        self.options.update(options)
        uris = self.uris[dbname]
        self.sentinel = Sentinel(uris, **self.options)
