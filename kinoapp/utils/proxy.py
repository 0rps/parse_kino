from requests import request as reqreq


def request(method, url, params=None):
    return reqreq(method, url, params=params)
