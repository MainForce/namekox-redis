#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import json


from redis.client import StrictRedis as BaseStrictRedis


class StrictRedis(BaseStrictRedis):
    def publish(self, channel, message):
        message = json.dumps(message)
        return super(StrictRedis, self).publish(channel, message)
