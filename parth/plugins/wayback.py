import re
import requests


def wayback(host, page):
	payload = {
		'url': host,
		'matchType': 'host',
		'collapse': 'urlkey',
		'fl': 'original',
		'page': page,
		'limit': 10000
	}
	headers = {
		'User-Agent': 'Mozilla'
	}
	try:
		response = requests.get(
			'http://web.archive.org/cdx/search?filter=mimetype:text/html&filter=statuscode:200',
			params=payload,
			headers=headers
		).text
		if not response:
			return ([], False, 'wayback')
		urls = filter(None, response.split('\n'))
		return (list(set(urls)), True, 'wayback')
	except requests.exceptions.ConnectionError:
		return([], False, 'wayback')
