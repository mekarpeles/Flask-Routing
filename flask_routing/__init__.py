#!/usr/bin/env python3.4
#-*-coding: utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~

    Configuration for flask application

    :copyright: (c) 2015 Hackerlist
    :license: BSD, see LICENSE for more details.
"""

import os
import string
import random
import json
from flask import Response
from flask.views import MethodView
from werkzeug import wrappers

def router(app, urls, base_url='', names=False, **kwargs):
    """Build web.py style url routing table and register subapps

    urls = ('/url', ClassHandler[, "name"],
            ...
           )

    params:
        base_url - used for recursive calls, do not pass in arg
        names - if names, urls become 3-tuples of route regex, 
                view Class, class name/str-id. Otherwise,
                2-tuple of route, view
    """
    chunk_size = 3 if names else 2
    for rule in chunk(urls, chunk_size):
        route, view, name = rule if names else rule + (None,)
        url = base_url + route
        
        if hasattr(view, 'urls'):
            router(app, getattr(view, 'urls'), base_url=url, names=names)

        elif MethodView in view.mro():
            try:
                name = name or "%s_%s" % (view.__name__, uid())
                app.add_url_rule(url, view_func=view.as_view(name))
            except Exception as e:
                raise e
        else:
            raise ValueError('Invalid view object for url %s %s.' \
                                 % ((base_url + route), view.mro()))
    return app

def uid(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def chunk(lst, n):
    """
    Yield successive n-sized chunks from l. 

        >>> chunk([1,2,3,4], 2)
        [[1, 2], [3, 4]]
        >>> chunk([1,2,3,4,5], 2)
        [[1, 2], [3, 4], [5]]
    """
    if len(lst) < n:
        return [lst]
    chunks = []
    for i in range(0, len(lst), n):
        chunks.append(lst[i:i+n])
    return chunks

def rest_api(f):
    """Decorator to allow routes to return json"""
    def inner(*args, **kwargs):
        try:
            try:
                res = f(*args, **kwargs)
                if isinstance(res, wrappers.Response):
                    return res
                response = Response(json.dumps(res))
            except Exception as e:
                response = Response(json.dumps(e.__dict__), e.http_error_code)

            response.headers.add('Content-Type', 'application/json')
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
        finally:
            #DB Rollbacks to protect against inconsistent states
            pass
    return inner
