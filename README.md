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
        self.redis.publish('ping', {name: mapping})
        # write to redisdb
        pipe = self.redis.pipeline()
        pipe.zadd(name, mapping)
        pipe.execute()
```

# Running
> config.yaml
```yaml
REDIS:
  sentinel:
    - redis://:***@*.*.*.*:6379/0
    - redis://:***@*.*.*.*:6379/0
  redisdb: redis://:***@*.*.*.*:6379/0
```
> namekox run ping
```shell script
2020-11-05 18:04:55,207 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-05 18:04:55,209 DEBUG starting services ['ping']
2020-11-05 18:04:55,209 DEBUG starting service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res]
2020-11-05 18:04:55,211 DEBUG spawn manage thread handle ping:namekox_redis.core.entrypoints.sub.handler:_run(args=(), kwargs={}, tid=_run)
2020-11-05 18:04:55,211 DEBUG spawn manage thread handle ping:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-11-05 18:04:55,213 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-11-05 18:04:55,214 DEBUG service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res] started
2020-11-05 18:04:55,215 DEBUG starting service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 18:04:55,216 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] started
2020-11-05 18:04:55,217 DEBUG services ['ping'] started
2020-11-05 18:05:00,219 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 18:05:00,226 DEBUG spawn worker thread handle ping:rds_sub(args=({u'ping:42.194.112.46:result': {u'1604570700219': 0}},), kwargs={}, context={})
('recv ping channel data: ', {u'ping:42.194.112.46:result': {u'1604570700219': 0}})
2020-11-05 18:05:05,219 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 18:05:05,222 DEBUG spawn worker thread handle ping:rds_sub(args=({u'ping:164.102.231.171:result': {u'1604570705219': 1}},), kwargs={}, context={})
('recv ping channel data: ', {u'ping:164.102.231.171:result': {u'1604570705219': 1}})
2020-11-05 18:05:10,219 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 18:05:10,222 DEBUG spawn worker thread handle ping:rds_sub(args=({u'ping:188.106.56.55:result': {u'1604570710219': 1}},), kwargs={}, context={})
('recv ping channel data: ', {u'ping:188.106.56.55:result': {u'1604570710219': 1}})
2020-11-05 18:05:12,931 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x104d44d50>, ('127.0.0.1', 57316)), kwargs={}, tid=handle_request)
2020-11-05 18:05:15,219 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 18:05:15,222 DEBUG spawn worker thread handle ping:rds_sub(args=({u'ping:148.208.79.87:result': {u'1604570715219': 1}},), kwargs={}, context={})
('recv ping channel data: ', {u'ping:148.208.79.87:result': {u'1604570715219': 1}})
2020-11-05 18:05:17,882 DEBUG spawn worker thread handle ping:ping_res(args=(<Request 'http://127.0.0.1/api/ping/42.194.112.46/' [GET]>,), kwargs={'ip': u'42.194.112.46'}, context={})
127.0.0.1 - - [05/Nov/2020 18:05:17] "GET /api/ping/42.194.112.46/ HTTP/1.1" 200 302 0.009732
2020-11-05 18:05:20,219 DEBUG spawn worker thread handle ping:ip_ping(args=(), kwargs={}, context=None)
2020-11-05 18:05:20,223 DEBUG spawn worker thread handle ping:rds_sub(args=({u'ping:115.179.48.157:result': {u'1604570720220': 0}},), kwargs={}, context={})
('recv ping channel data: ', {u'ping:115.179.48.157:result': {u'1604570720220': 0}})
^C2020-11-05 18:05:21,867 DEBUG stopping services ['ping']
2020-11-05 18:05:21,868 DEBUG stopping service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res]
2020-11-05 18:05:21,873 DEBUG wait service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res] stop
2020-11-05 18:05:21,874 DEBUG service ping entrypoints [ping:namekox_redis.core.entrypoints.sub.handler.RedisSubHandler:rds_sub, ping:namekox_timer.core.entrypoints.timer.Timer:ip_ping, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server, ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:ping_res] stopped
2020-11-05 18:05:21,876 DEBUG stopping service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 18:05:21,878 DEBUG service ping dependencies [ping:namekox_redis.core.dependencies.redisdb.RedisDB:redis] stopped
2020-11-05 18:05:21,879 DEBUG services ['ping'] stopped
2020-11-05 18:05:21,879 DEBUG killing services ['ping']
2020-11-05 18:05:21,879 DEBUG service ping already stopped
2020-11-05 18:05:21,880 DEBUG services ['ping'] killed
```
> curl http://127.0.0.1/api/ping/42.194.112.46/
```json
{
    "errs": "",
    "code": "Request:Success",
    "data": [
        {
          "ip": "42.194.112.46",
          "alive": false,
          "created": 1604570700219
        }
    ],
    "call_id": "bb3a562d-44ed-4b7f-ad77-7978403fd4b9"
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
2020-11-05 17:23:46,480 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-05 17:23:46,481 DEBUG starting services ['phone']
2020-11-05 17:23:46,481 DEBUG starting service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 17:23:46,481 DEBUG spawn manage thread handle phone:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-11-05 17:23:46,482 DEBUG service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number] started
2020-11-05 17:23:46,482 DEBUG starting service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 17:23:46,483 DEBUG service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis] started
2020-11-05 17:23:46,483 DEBUG services ['phone'] started
2020-11-05 17:23:46,584 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:23:46,613 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:50,629 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:50,629 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:23:50,634 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:51,641 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:51,642 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:23:51,646 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:54,651 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:54,651 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:23:54,655 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:59,659 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:23:59,660 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:23:59,662 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:03,670 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:03,670 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:03,673 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:07,683 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:07,684 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:07,688 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:12,694 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:12,695 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:12,697 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:15,705 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:15,705 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:15,708 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
^C2020-11-05 17:24:18,082 DEBUG stopping services ['phone']
2020-11-05 17:24:18,083 DEBUG stopping service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 17:24:20,716 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:20,716 DEBUG wait service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number] stop
2020-11-05 17:24:20,716 DEBUG service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number] stopped
2020-11-05 17:24:20,717 DEBUG stopping service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 17:24:20,717 DEBUG service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis] stopped
2020-11-05 17:24:20,718 DEBUG services ['phone'] stopped
2020-11-05 17:24:20,718 DEBUG killing services ['phone']
2020-11-05 17:24:20,719 DEBUG service phone already stopped
2020-11-05 17:24:20,719 DEBUG services ['phone'] killed
```
> namekox run ping
```shell script
2020-11-05 17:24:06,141 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-05 17:24:06,142 DEBUG starting services ['phone']
2020-11-05 17:24:06,142 DEBUG starting service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 17:24:06,142 DEBUG spawn manage thread handle phone:namekox_timer.core.entrypoints.timer:_run(args=(), kwargs={}, tid=_run)
2020-11-05 17:24:06,143 DEBUG service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number] started
2020-11-05 17:24:06,143 DEBUG starting service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 17:24:06,143 DEBUG service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis] started
2020-11-05 17:24:06,143 DEBUG services ['phone'] started
2020-11-05 17:24:06,246 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:11,163 DEBUG number_assign waiting `phone:assign_number:lock` lock released
2020-11-05 17:24:16,088 DEBUG number_assign waiting `phone:assign_number:lock` lock released
2020-11-05 17:24:20,737 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:21,742 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:21,742 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:21,745 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:26,750 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:26,750 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:26,753 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:31,760 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:31,761 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:31,765 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:35,772 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:35,772 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:35,775 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:39,781 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:39,781 DEBUG spawn worker thread handle phone:assign_number(args=(), kwargs={}, context=None)
2020-11-05 17:24:39,786 DEBUG number_assign acquire `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
^C2020-11-05 17:24:44,484 DEBUG stopping services ['phone']
2020-11-05 17:24:44,485 DEBUG stopping service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number]
2020-11-05 17:24:44,790 DEBUG number_assign release `phone:assign_number:lock` lock({'blocking_timeout': 5, 'timeout': 20}) succ
2020-11-05 17:24:44,790 DEBUG wait service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number] stop
2020-11-05 17:24:44,791 DEBUG service phone entrypoints [phone:namekox_timer.core.entrypoints.timer.Timer:assign_number] stopped
2020-11-05 17:24:44,791 DEBUG stopping service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis]
2020-11-05 17:24:44,791 DEBUG service phone dependencies [phone:namekox_redis.core.dependencies.redisdb.RedisDB:redis] stopped
2020-11-05 17:24:44,791 DEBUG services ['phone'] stopped
2020-11-05 17:24:44,792 DEBUG killing services ['phone']
2020-11-05 17:24:44,792 DEBUG service phone already stopped
2020-11-05 17:24:44,793 DEBUG services ['phone'] killed
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_redis.cli.subctx.redisdb:RedisDB
  - namekox_redis.cli.subctx.sentinel:SentinelDB
REDIS:
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
