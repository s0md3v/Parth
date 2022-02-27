import json
import re


def save_result(result, savefile, save_format):
    if save_format == 'json':
        with open(savefile, 'w+') as f:
            json.dump(result, f, indent=4)


def extract_params(url, data):
    params = []
    query_part = ''
    if '?' in url:
        query_part = url.split('?')[1].split('#')[0]
    elif data and '=' in data:
        query_part = url.split('?')[1]
    if query_part:
        params.extend(pair.split('=')[0] for pair in query_part.split('&'))
    elif data and data.startswith('{'):
        try:
            return json.loads(data).keys()
        except:
            pass
    return params


def parse_headers(string):
    """
    parses headers
    return dict
    """
    result = {}
    for line in string.split('\n'):
        if len(line) > 1:
            splitted = line.split(':')
            result[splitted[0]] = ':'.join(splitted[1:]).strip()
    return result


def parse_request(string):
    """
    parses http request
    returns dict
    """
    result = {}
    match = re.search(r'(?:([a-zA-Z0-9]+) ([^ ]+) [^ ]+\n)?([\s\S]+\n)\n?([\s\S]+)?', string)
    result['url'] =  re.search(r'[Hh]ost:\s*([a-zA-Z0-9.-]+)').group(1) + match.group(2)
    result['data'] = match.group(4)
    return result


def reader(path, mode='string'):
    """
    reads a file
    returns a string/array containing the content of the file
    """
    with open(path, 'r', encoding='utf-8') as file:
        if mode == 'lines':
            return [line.rstrip('\n') for line in file]
        else:
            return ''.join([line for line in file])
