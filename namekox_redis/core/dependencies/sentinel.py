#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from namekox_redis.core.sentinel import Sentinel
from namekox_core.core.friendly import AsLazyProperty
from namekox_redis.constants import REDISDB_CONFIG_KEY
from namekox_core.core.service.dependency import Dependency


class SentinelDB(Dependency):
    def __init__(self, dbname, **options):
        self.sentinel = None
        self.dbname = dbname
        self.options = options
        super(SentinelDB, self).__init__(dbname, **options)

    @AsLazyProperty
    def uris(self):
        return self.container.config.get(REDISDB_CONFIG_KEY, {})

    def setup(self):
        uris = self.uris[self.dbname]
        self.sentinel = Sentinel(uris, **self.options)

    def stop(self):
        if not self.sentinel.sentinels:
            return
        for c in self.sentinel.sentinels:
            c.close()
            c.connection_pool and c.connection_pool.disconnect()

    def get_instance(self, context):
        return self.sentinel
