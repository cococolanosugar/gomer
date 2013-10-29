#!/usr/bin/env python
# encoding: utf-8
"""
rkcurl.py

Copyright (c) 2010 Rekoo Media. All rights reserved.

A lightweight wrapper around PycURL.

useage:
    rkcurl.get('http://www.example.com/1/')
    rkcurl.delete('http://www.example.com/1/')
"""

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import pycurl

def _call(resource, method, data=None, headers=None, timeout=None, debug=None):
    """A lightweight wrapper around PycURL

    Args:
        resource: resource to call, i. e. /a or /a/123/c
        method: one of: get, post, put, delete
        data: data to encode and send on post and put requests
        headers: http headers
        timeout: http connection timeout, second
        debug: pycurl debug info

    Returns:
        code: http status code
        response: response data
    """
    method = method.upper()
    handle = pycurl.Curl()
    output = StringIO()

    handle.setopt(pycurl.URL, resource)

    if isinstance(headers, dict):
        handle.setopt(pycurl.HTTPHEADER,
                      ['%s: %s' % (header, str(value)) for header, value in headers.iteritems()])

    if isinstance(timeout, int):
        handle.setopt(pycurl.TIMEOUT, timeout)

    if debug:
        handle.setopt(pycurl.VERBOSE, True)

    if method == 'POST':
        handle.setopt(pycurl.POST, True)
        handle.setopt(pycurl.POSTFIELDS, data)
    elif method == 'PUT':
        input = StringIO(data)
        handle.setopt(pycurl.PUT, True)
        handle.setopt(pycurl.READFUNCTION, input.read)
    elif method == 'DELETE':
        handle.setopt(pycurl.CUSTOMREQUEST, 'DELETE')

    handle.setopt(pycurl.WRITEFUNCTION, output.write)
    handle.perform()

    code = handle.getinfo(pycurl.RESPONSE_CODE)
    response = output.getvalue()

    return code, response

def get(resource, headers=None, timeout=None, debug=None):
    """HTTP GET using pycurl"""
    return _call(resource, 'GET', headers=headers, timeout=timeout, debug=debug)

def post(resource, data=None, headers=None, timeout=None, debug=None):
    """HTTP POST using pycurl"""
    return _call(resource, 'POST', data=data, headers=headers, timeout=timeout, debug=debug)

def put(resource, data=None, headers=None, timeout=None, debug=None):
    """HTTP PUT using pycurl"""
    return _call(resource, 'PUT', data=data, headers=headers, timeout=timeout, debug=debug)

def delete(resource, headers=None, timeout=None, debug=None):
    """HTTP DELETE using pycurl"""
    return _call(resource, 'DELETE', headers=headers, timeout=timeout, debug=debug)

