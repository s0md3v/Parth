import re

from .utils import reader, parse_request, extract_params

burp_regex = re.compile(r'''(?m)^    <url><!\[CDATA\[(.+?)\]\]></url>
    <host ip="[^"]*">[^<]+</host>
    <port>[^<]*</port>
    <protocol>[^<]*</protocol>
    <method><!\[CDATA\[(.+?)\]\]></method>
    <path>.*</path>
    <extension>(.*)</extension>
    <request base64="(?:false|true)"><!\[CDATA\[([\s\S]+?)]]></request>
    <status>([^<]*)</status>
    <responselength>([^<]*)</responselength>
    <mimetype>([^<]*)</mimetype>''')


def burp_import(path):
	requests = {}
	content = reader(path)
	matches = re.finditer(burp_regex, content)
	for match in matches:
		request = parse_request(match.group(4))
		url = match.group(1)
		requests[url] = request['data']
	return requests


def urls_import(path):
	return {url:[] for url in reader(path, mode='lines')}


def request_import(path):
	parsed = parse_request(reader(path))
	return {parsed['url']:[parsed['data']]}


def importer(path):
    with open(path, 'r', encoding='utf-8') as file:
    	for line in file:
	        if line.startswith('<?xml'):
	            return burp_import(path)
	        elif line.startswith(('http://', 'https://')):
	            return urls_import(path)
	        elif line.startswith(('GET', 'POST')):
	            return request_import(path)
	        return {}
