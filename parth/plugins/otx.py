import re
import requests


def otx(host, page):
    data = requests.get('https://otx.alienvault.com/api/v1/indicators/hostname/%s/url_list?limit=50&page=%d' % (host, page)).json()
    if 'url_list' not in data:
    	return (set([]), False, 'otx')
    urls = [obj['url'] for obj in data['url_list']]
    return (set(urls), data['has_next'], 'otx')
