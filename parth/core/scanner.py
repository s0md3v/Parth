import json
import sys

from .utils import extract_params
from .param_map import param_rules

def scanner(requests, save_params, dupes):
    """
    scans a request object
    returns dict
    """
    result = []
    all_params = set()
    for url, other_data in requests.items():
        data = other_data[0] if other_data else ''
        params = set(extract_params(url, data))
        for param in params:
            if dupes and param in all_params:
                continue
            if param in param_rules:
                result.append({
                    'url': url,
                    'data': data,
                    'location': param,
                    'issues': param_rules[param],
                    'type': 'parameter'
                })
        if save_params or dupes:
            all_params.update(params)
    return result, list(all_params)
