#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from .sub.handler import RedisSubHandler


rds = type(__name__, (object,), {'sub': RedisSubHandler.decorator})
