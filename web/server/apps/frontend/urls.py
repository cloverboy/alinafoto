# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-06'

import urlparse, urllib

from settings import LOCALE_LANG_SHORT

PAGE_HANDLER_PAGES = ['index', 'about', 'services', 'partners', 'contacts', ]

# highlight 'services' top navigation button
# if 'mobile-promotion' page is selected
PAGE_HANDLER_PAGE_ALIASES = {
    'mobile-promotion': 'services',
    'application-development': 'services',
    'search-engine-optimisation': 'services',
    'social-media-marketing': 'services',
}

PAGE_HANDLER_PAGES.extend(PAGE_HANDLER_PAGE_ALIASES.keys())

LANGS = '^/(%s)' % ('|'.join([v for k, v in LOCALE_LANG_SHORT]))
PAGE_HANDLER_PAGES = '(%s)' % '|'.join(PAGE_HANDLER_PAGES)

URL_PATTERNS = {
    'index_page': '/{}/',
    'about_page': '/{}/about/',
    'news_page': '/{}/news/',
    'news_item_page': '/{}/news/{}/',
    'services_page': '/{}/services/',
    'partners_page': '/{}/partners/',
    'contacts_page': '/{}/contacts/',
    'mobile_promotion_page': '/{}/mobile-promotion/',
    'application_development_page': '/{}/application-development/',
    'search_engine_optimisation_page': '/{}/search-engine-optimisation/',
    'social_media_marketing_page': '/{}/social-media-marketing/',
    'ping_pong_page': '/ping-pong/',
}

def reverse_page(page_name, *args, **kwargs):
    pattern = URL_PATTERNS.get(page_name)
    path = pattern.format(*args)

    get_params = kwargs.get('get_params')
    if get_params:
        path = '%s%s%s' % (path, (urlparse.urlparse(path)[4] and '&' or '?'), urllib.urlencode(get_params))

    return path