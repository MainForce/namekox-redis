#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import time


from redis import StrictRedis
from logging import getLogger
from namekox_redis.constants import REDIS_CONFIG_KEY
from namekox_core.core.friendly import AsLazyProperty
from namekox_core.core.service.entrypoint import Entrypoint


logger = getLogger(__name__)


class RedisSubHandler(Entrypoint):
    def __init__(self, dbname, channels=None, pattern_mode=False, **options):
        self.gt = None
        self.connection = None
        self.dbname = dbname
        self.options = options
        self.channels = channels or []
        self.pattern_mode = pattern_mode
        super(RedisSubHandler, self).__init__(dbname, channels=channels, pattern_mode=pattern_mode, **options)

    @AsLazyProperty
    def uris(self):
        return self.container.config.get(REDIS_CONFIG_KEY, {})

    def setup(self):
        duri = self.uris[self.dbname]
        self.connection = StrictRedis.from_url(duri, **self.options)

    def start(self):
        self.gt = self.container.spawn_manage_thread(self._run)

    def stop(self):
        self.gt.kill()

    def _run(self):
        p = self.connection.pubsub(ignore_subscribe_messages=True)
        s = p.psubscribe if self.pattern_mode is True else p.subscribe
        s(*self.channels)
        # TODO: extract context data from channel message
        ctx_data = None
        for m in p.listen():
            args, kwargs = (m,), {}
            self.container.spawn_worker_thread(self, args, kwargs, ctx_data=ctx_data)
            time.sleep(0.001)
        u = p.punsubscribe if self.pattern_mode is True else p.unsubscribe
        u(*self.channels)
