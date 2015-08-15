# -*- coding: utf-8 -*-

import urlparse, urllib

from settings import LOCALE_LANG_SHORT, BASE_DOMAIN_PROTOCOL, BASE_DOMAIN

URL_PATTERNS = {
    'index_page': '/{}/',
    'guestbook_page': '/{}/guestbook/',
    'ping_pong_page': '/ping-pong/',
}

PAGE_HANDLER_PAGES = ['weddings', 'children', 'parties', 'others', ]

for slug in PAGE_HANDLER_PAGES:
    URL_PATTERNS['%s_page' % slug] = '/{}/%s/' % slug

LANGS = '^/(%s)' % ('|'.join([v for k, v in LOCALE_LANG_SHORT]))
PAGE_HANDLER_PAGES = '(%s)' % '|'.join(PAGE_HANDLER_PAGES)


def reverse_page(page_name, *args, **kwargs):
    pattern = URL_PATTERNS.get(page_name)
    path = pattern.format(*args)

    query_arguments = kwargs.get('query_arguments')
    if query_arguments:
        path = '%s%s%s' % (path, (urlparse.urlparse(path)[4] and '&' or '?'), urllib.urlencode(query_arguments))

    full_url = kwargs.get('full_url', False)
    if full_url:
        path = '%s://%s%s' % (BASE_DOMAIN_PROTOCOL, BASE_DOMAIN, path)

    return path