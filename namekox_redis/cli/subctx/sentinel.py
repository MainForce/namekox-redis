#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from namekox_redis.core.proxy import SentinelDBProxy


class SentinelDB(object):
    def __init__(self, config):
        self.config = config
        self.proxy = SentinelDBProxy(config)

    @classmethod
    def name(cls):
        return 'sentinel'
