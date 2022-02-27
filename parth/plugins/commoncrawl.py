import requests

def commoncrawl(host, page=0):
	response = requests.get('http://index.commoncrawl.org/CC-MAIN-2020-29-index?url=*.%s&fl=url&page=%s&limit=10000' % (host, page)).text
	if response.startswith('<!DOCTYPE html>'):
		return ([], False, 'commoncrawl')
	return (response.split('\n'), True, 'commoncrawl')
