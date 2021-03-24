#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from redis import StrictRedis
from namekox_redis.constants import REDIS_CONFIG_KEY
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.dependency import Dependency


class RedisDB(Dependency):
    def __init__(self, dbname, **options):
        self.client = None
        self.dbname = dbname
        self.options = options
        super(RedisDB, self).__init__(dbname, *options)

    @AsLazyProperty
    def uris(self):
        return self.container.config.get(REDIS_CONFIG_KEY, {})

    def setup(self):
        duri = self.uris[self.dbname]
        self.client = StrictRedis.from_url(duri, *self.options)

    def stop(self):
        self.client and self.client.connection_pool and self.client.connection_pool.disconnect()

    def get_instance(self, context):
        return self.client
