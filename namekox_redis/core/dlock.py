#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from logging import getLogger
from redis.exceptions import LockError


logger = getLogger(__name__)


def distributed_lock(conn, func, name, **kwargs):
    while True:
        try:
            with conn.lock(name, **kwargs):
                msg = '{} acquire `{}` lock({}) succ'.format(func.__name__, name, kwargs)
                logger.debug(msg)
                func()
            msg = '{} release `{}` lock({}) succ'.format(func.__name__, name, kwargs)
            logger.debug(msg)
            break
        except LockError:
            msg = '{} waiting `{}` lock released'.format(func.__name__, name)
            logger.debug(msg)
