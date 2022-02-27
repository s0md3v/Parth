#!/usr/bin/env python3

import argparse
import concurrent.futures
import json
import sys

from .core.colors import green, white, end, info, bad, good, run
from .core.importer import importer
from .core.scanner import scanner
from .core.utils import save_result

from .plugins.commoncrawl import commoncrawl
from .plugins.otx import otx
from .plugins.wayback import wayback

parser = argparse.ArgumentParser() # defines the parser
# Arguments that can be supplied
parser.add_argument('-t', help='target host', dest='host')
parser.add_argument('-i', help='import from file', dest='input_file')
parser.add_argument('-o', help='output file', dest='output_file')
parser.add_argument('-u', help='uniq parameters', dest='dupes', action='store_true')
parser.add_argument('-f', help='output format', dest='output_format', default='json')
parser.add_argument('-p', help='save parameters', dest='save_params', action='store_true')
parser.add_argument('--pipe', help='only display these issues', dest='pipe')
args = parser.parse_args() # arguments to be parsed

if args.input_file or args.host:
	print('''%s      __
     /_/ _   _ _/_ /_
    /   (_\\ /  /  / / {%s%s%s}%s
	''' % (green, white, __import__('parth').__version__, green, end))

def fetch_urls(host):
    available_plugins = {'commoncrawl': commoncrawl, 'otx': otx, 'wayback': wayback}
    page = 0
    progress = 0
    requests = {}
    while len(available_plugins) > 0 and page <= 10:
        threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=len(available_plugins))
        futures = (threadpool.submit(func, host, page) for func in available_plugins.values())
        for each in concurrent.futures.as_completed(futures):
            if progress < 98:
                progress += 3
            this_result = each.result()
            if not this_result[1]:
                progress += ((10 - page) * 10 / 3)
                del available_plugins[this_result[2]]
            for url in this_result[0]:
                requests[url] = []
            print('%s Progress: %i%%' % (info, progress), end='\r')
        page += 1
    print('%s Progress: %i%%' % (info, 100), end='\r')
    return requests

def main():
    result = []
    all_params = []

    requests = None
    if args.host:
        requests = fetch_urls(args.host)
    elif args.input_file:
        requests = importer(args.input_file)
    elif not sys.stdin.isatty():
        requests = 1
        for line in sys.stdin:
            this_result, all_params = scanner(
                {line.rstrip('\r\n'):[]},
                args.save_params,
                args.dupes
            )
            if args.pipe and this_result:
                if args.pipe in this_result[0]['issues']:
                    print(this_result[0]['url'])
            else:
                result.extend(this_result)
        if args.pipe:
            quit()
    else:
        print('%s No targets specified.' % bad)

    if requests:
        if requests != 1:
            result, all_params = scanner(requests, args.save_params, args.dupes)
        if args.output_file:
            save_result(result, args.output_file, args.output_format)
            print('%s Result saved to %s' % (info, args.output_file))
        else:
            for each in result:
                print('%s+%s %s' % (green, end, each['url']))
                print('    %s- issues:%s   %s' % (green, end, ', '.join(each['issues'])))
                print('    %s- location:%s %s' % (green, end, each['location']))
                if each['data']:
                    print('%s- data:%s %s' % (green, end, each['data']))

    if args.save_params:
        suffix = args.input_file or args.host
        with open('params-' + suffix.strip('.history').strip('.txt') + '.txt', 'w+') as f:
            f.write('\n'.join(all_params))
