# Install
```shell script
pip install -U namekox-redis
```

# Example
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


import time
import random
import anyjson


from marshmallow import Schema, fields
from namekox_redis.core.entrypoints import rds
from namekox_webserver.core.entrypoints.app import app
from namekox_timer.core.entrypoints.timer import timer
from namekox_redis.core.dependencies.redisdb import RedisDB


class ResultSchema(Schema):
    ip = fields.String(required=True)
    alive = fields.Boolean(required=True)
    created = fields.Float(required=True)


def generate_ip():
    return '.'.join([str(random.randint(1, 255)) for _ in range(4)])


class Ping(object):
    name = 'ping'

    redis = RedisDB('redisdb')

    @staticmethod
    def gen_ping_name(ip):
        return 'ping:{}:result'.format(ip)

    @app.api('/api/ping/<ip>/', methods=['GET'])
    def ping_res(self, request, ip=None):
        name = self.gen_ping_name(ip)
        data = self.redis.zrange(name, 0, -1, desc=True, withscores=True)
        data = [{'ip': ip, 'alive': bool(d[1]), 'created': d[0]} for d in data]
        return ResultSchema(many=True).load(data).data

    @rds.sub('redisdb', channels=['ping'])
    def rds_sub(self, message):
        print('recv ping channel data: ', message)

    @timer(5)
    def ip_ping(self):
        ip = generate_ip()
        name = self.gen_ping_name(ip)
        mapping = {
            int(time.time() * 1000): random.choice([0, 1])
        }
        # write to channel
        self.redis.publish('ping', anyjson.serialize({name: mapping}))
        # write to redisdb
        pipe = self.redis.pipeline()
        pipe.zadd(name, mapping)
        pipe.execute()
```

# Running
> config.yaml
```yaml
REDISDB:
  sentinel:
    - redis://:***@*.*.*.*:6379/0
    - redis://:***@*.*.*.*:6379/0
  redisdb: redis://:***@*.*.*.*:6379/0
```
> namekox run ping
```shell script
2020-11-05 09:42:04,335 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-05 09:42:04,336 DEBUG starting services ['ping']
2020-11-05 09:42:04,336 DEBUG starting service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res]
2020-11-05 09:42:04,337 DEBUG spawn manage thread handle ping:namekox_redis.core.entrypoints.sub.handler:_run(args=(), kwargs={}, tid=_run)
2020-11-05 09:42:04,337 DEBUG spawn manage thread handle ping:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-11-05 09:42:04,340 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-11-05 09:42:04,341 DEBUG service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res] started
2020-11-05 09:42:04,341 DEBUG starting service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 09:42:04,342 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] started
2020-11-05 09:42:04,343 DEBUG services ['ping'] started
2020-11-05 09:42:09,344 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 09:42:09,353 DEBUG spawn worker thread handle ping:rds_sub(args=({u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:159.218.96.180:result": {"1604540529345": 1}}'},), kwargs={}, context=None)
('recv ping channel data: ', {u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:159.218.96.180:result": {"1604540529345": 1}}'})
2020-11-05 09:42:14,344 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 09:42:14,350 DEBUG spawn worker thread handle ping:rds_sub(args=({u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:76.230.7.197:result": {"1604540534344": 0}}'},), kwargs={}, context=None)
('recv ping channel data: ', {u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:76.230.7.197:result": {"1604540534344": 0}}'})
2020-11-05 09:42:19,343 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 09:42:19,348 DEBUG spawn worker thread handle ping:rds_sub(args=({u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:172.254.248.64:result": {"1604540539344": 0}}'},), kwargs={}, context=None)
('recv ping channel data: ', {u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:172.254.248.64:result": {"1604540539344": 0}}'})
2020-11-05 09:42:24,345 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 09:42:24,350 DEBUG spawn worker thread handle ping:rds_sub(args=({u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:243.161.154.40:result": {"1604540544345": 0}}'},), kwargs={}, context=None)
('recv ping channel data: ', {u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:243.161.154.40:result": {"1604540544345": 0}}'})
2020-11-05 09:42:29,345 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 09:42:29,350 DEBUG spawn worker thread handle ping:rds_sub(args=({u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:193.11.202.108:result": {"1604540549346": 1}}'},), kwargs={}, context=None)
('recv ping channel data: ', {u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:193.11.202.108:result": {"1604540549346": 1}}'})
2020-11-05 09:42:34,343 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 09:42:34,356 DEBUG spawn worker thread handle ping:rds_sub(args=({u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:254.104.167.77:result": {"1604540554344": 0}}'},), kwargs={}, context=None)
('recv ping channel data: ', {u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:254.104.167.77:result": {"1604540554344": 0}}'})
2020-11-05 09:42:36,504 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10c1f9f10>, ('127.0.0.1', 53353)), kwargs={}, tid=handle_request)
2020-11-05 09:42:36,516 DEBUG spawn worker thread handle ping:ping_res(args=(<Request 'http://127.0.0.1/api/ping/159.218.96.180/' [GET]>,), kwargs={'ip': u'159.218.96.180'}, context={})
127.0.0.1 - - [05/Nov/2020 09:42:36] "GET /api/ping/159.218.96.180/ HTTP/1.1" 200 302 0.010059
2020-11-05 09:42:39,345 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 09:42:39,349 DEBUG spawn worker thread handle ping:rds_sub(args=({u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:52.232.227.243:result": {"1604540559346": 0}}'},), kwargs={}, context=None)
('recv ping channel data: ', {u'pattern': None, u'type': 'message', u'channel': 'ping', u'data': '{"ping:52.232.227.243:result": {"1604540559346": 0}}'})
^C2020-11-05 09:42:42,908 DEBUG stopping services ['ping']
2020-11-05 09:42:42,909 DEBUG stopping service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res]
2020-11-05 09:42:42,912 DEBUG wait service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res] stop
2020-11-05 09:42:42,913 DEBUG service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res] stopped
2020-11-05 09:42:42,913 DEBUG stopping service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 09:42:42,918 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] stopped
2020-11-05 09:42:42,919 DEBUG services ['ping'] stopped
2020-11-05 09:42:42,919 DEBUG killing services ['ping']
2020-11-05 09:42:42,920 DEBUG service ping already stopped
2020-11-05 09:42:42,920 DEBUG services ['ping'] killed
```
> curl http://127.0.0.1/api/ping/159.218.96.180/
```json
{
    "errs": "",
    "code": "Request:Success",
    "data": [
        {
          "ip": "159.218.96.180",
          "alive": true,
          "created": 1604540529345
        }
    ],
    "call_id": "24d9bea6-862e-403c-8078-63e2ea1a9258"
}
```

# Lock<sup>distributed</sup>
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


import time
import random


from logging import getLogger
from namekox_redis.core.dlock import distributed_lock
from namekox_timer.core.entrypoints.timer import timer
from namekox_redis.core.dependencies.redisdb import RedisDB


logger = getLogger(__name__)


class Phone(object):
    name = 'phone'

    redis = RedisDB('redisdb')

    @staticmethod
    def number_assign():
        time.sleep(random.randint(1, 5))

    @timer(0.1)
    def assign_number(self):
        lock_name = 'phone:assign_number:lock'
        distributed_lock(self.redis, self.number_assign, lock_name, timeout=20, blocking_timeout=5)
```
> namekox run ping
```shell script
2020-11-05 11:28:05,309 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-05 11:28:05,309 DEBUG starting services ['ping']
2020-11-05 11:28:05,310 DEBUG starting service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 11:28:05,310 DEBUG spawn manage thread handle ping:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-11-05 11:28:05,311 DEBUG service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number] started
2020-11-05 11:28:05,311 DEBUG starting service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 11:28:05,311 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] started
2020-11-05 11:28:05,311 DEBUG services ['ping'] started
2020-11-05 11:28:05,412 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:05,431 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:06,437 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:06,437 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:06,441 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:10,452 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:10,452 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:10,456 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:15,460 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:15,461 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:15,464 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:16,471 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:16,472 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:16,474 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:17,480 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:17,480 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:17,483 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:20,488 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:20,488 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:20,492 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:21,499 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:21,500 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:21,504 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:23,510 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:23,510 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:23,513 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:24,522 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:24,522 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:29,507 DEBUG number_assign waiting `phone:assign_number:lock` lock released
^C2020-11-05 11:28:31,894 DEBUG stopping services ['ping']
2020-11-05 11:28:31,895 DEBUG stopping service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 11:28:34,421 DEBUG number_assign waiting `phone:assign_number:lock` lock released
2020-11-05 11:28:35,601 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:40,609 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:40,610 DEBUG wait service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number] stop
2020-11-05 11:28:40,610 DEBUG service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number] stopped
2020-11-05 11:28:40,610 DEBUG stopping service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 11:28:40,611 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] stopped
2020-11-05 11:28:40,611 DEBUG services ['ping'] stopped
2020-11-05 11:28:40,612 DEBUG killing services ['ping']
2020-11-05 11:28:40,612 DEBUG service ping already stopped
2020-11-05 11:28:40,612 DEBUG services ['ping'] killed
```
> namekox run ping
```shell script
2020-11-05 11:28:09,387 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-05 11:28:09,387 DEBUG starting services ['ping']
2020-11-05 11:28:09,388 DEBUG starting service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 11:28:09,388 DEBUG spawn manage thread handle ping:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-11-05 11:28:09,388 DEBUG service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number] started
2020-11-05 11:28:09,388 DEBUG starting service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 11:28:09,389 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] started
2020-11-05 11:28:09,389 DEBUG services ['ping'] started
2020-11-05 11:28:09,492 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:14,425 DEBUG number_assign waiting `phone:assign_number:lock` lock released
2020-11-05 11:28:19,421 DEBUG number_assign waiting `phone:assign_number:lock` lock released
2020-11-05 11:28:24,415 DEBUG number_assign waiting `phone:assign_number:lock` lock released
2020-11-05 11:28:24,525 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:28,533 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:28,533 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:28,538 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:29,546 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:29,547 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:29,550 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:32,560 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:32,561 DEBUG spawn worker thread handle ping:assign_number(args=(), kwargs={}, context=None)
2020-11-05 11:28:32,563 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
^C2020-11-05 11:28:34,493 DEBUG stopping services ['ping']
2020-11-05 11:28:34,494 DEBUG stopping service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 11:28:35,572 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 11:28:35,572 DEBUG wait service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number] stop
2020-11-05 11:28:35,572 DEBUG service ping entrypoints [ping:namekox_timer.core.entrypoints.timer.Timer:assign_number] stopped
2020-11-05 11:28:35,572 DEBUG stopping service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 11:28:35,573 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] stopped
2020-11-05 11:28:35,573 DEBUG services ['ping'] stopped
2020-11-05 11:28:35,573 DEBUG killing services ['ping']
2020-11-05 11:28:35,574 DEBUG service ping already stopped
2020-11-05 11:28:35,574 DEBUG services ['ping'] killed
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_redis.cli.subctx.redisdb:RedisDB
  - namekox_redis.cli.subctx.sentinel:SentinelDB
REDISDB:
  sentinel:
    - redis://:***@*.*.*.*:6379/0
    - redis://:***@*.*.*.*:6379/0
  redisdb: redis://:***@*.*.*.*:6379/0
```
> namekox shell
```shell script
Namekox Python 2.7.16 (default, Dec 13 2019, 18:00:32)
[GCC 4.2.1 Compatible Apple LLVM 11.0.0 (clang-1100.0.32.4) (-macos10.15-objc-s shell on darwin
In [1]: nx.redisdb.proxy('redisdb').zrange('ping:159.218.96.180:result', 0, -1, desc=True, withscores=True)
Out[1]: [('1604540529345', 1.0)]
```
