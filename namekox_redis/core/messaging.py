#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import six


from namekox_redis.constants import DEFAULT_REDIS_H_PREFIX


def gen_message_headers(context):
    headers = {}
    for k, v in six.iteritems(context):
        k = '{}-'.format(DEFAULT_REDIS_H_PREFIX) + k
        headers.update({k: v})
    return headers


def get_message_headers(message):
    message_headers = message.get('headers', {}) if isinstance(message, dict) else {}
    headers = {}
    for k, v in six.iteritems(message_headers):
        p = '{}-'.format(DEFAULT_REDIS_H_PREFIX)
        k.startswith(p) and headers.update({k[len(p):]: v})
    return headers
