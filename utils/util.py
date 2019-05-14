#!/usr/bin/env python
# -*- coding:utf-8 -*-


def u_response(status=False, message=None, data=None):
    return {
        'status': status,
        'message': message,
        'data': data,
        'errorCode': ''
    }
