# -*- coding: utf-8 -*-
from urlparse import urlsplit, urlunsplit, parse_qsl, SplitResult
from urllib import urlencode


def initialize_item(item_fields, item):
    for field in item_fields:
        item[field] = u''
    return item


def get_next_page_url(url, page_param_name, first_page_num):
    splitted_url = urlsplit(url)
    query_dict = dict(parse_qsl(splitted_url.query))
    next_page_number = int(query_dict.get(page_param_name, '%d' % first_page_num)) + 1
    query_dict.update({page_param_name: next_page_number})
    next_split_result = SplitResult(splitted_url.scheme, splitted_url.netloc, splitted_url.path, urlencode(query_dict),
                                    splitted_url.fragment)
    return urlunsplit(next_split_result)


def get_item_from_list(data_list):
    if data_list:
        return data_list[0]
    else:
        return None