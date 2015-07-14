# coding:utf-8
'''
    Tags Analysis
    ~~~~~~~~~~~~~
'''

from functools import partial
import requests
import json
import re

X_CLIENT_ID = 'c017577997806d905149'
X_ACCESS_TOKEN = '101c5050ba558bdea41f08aa26923b9fb74adb72ee831aa43c216e80f357'

_cached = {}


def cached(func):
    def _ccached(*args, **kwargs):
        global _cached
        if _cached:
            return _cached
        else:
            r = func(*args, **kwargs)
            _cached = r
            return r
    return _ccached


def sum_datas_by_tags(datas, tags):
    stream = '####'.join([d['title'] for d in datas if tags in d['title']])
    nums = re.findall(r'(?<= )\d+(?= ?)', stream)
    nums = map(lambda x: int(x), nums)
    print nums
    return sum(nums)


def fetch_datas(completed=None):
    headers = {'x-access-token': X_ACCESS_TOKEN, 'x-client-id': X_CLIENT_ID}
    params = {'list_id': 106275541}
    if completed:
        params.update({'completed': 'true'})
    url = 'http://a.wunderlist.com/api/v1/tasks'
    resp = requests.get(url, params=params, headers=headers)
    assert resp.status_code, 200
    datas = json.loads(resp.content)
    return datas

fetch_complete_datas = partial(fetch_datas, True)
sum_by_tags = partial(
    sum_datas_by_tags, fetch_datas())  # use this

# analysis


if __name__ == '__main__':
    print '=' * 5
    print sum_by_tags(u'#t-新思路')
    print '=' * 5
