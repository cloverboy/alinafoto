# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-06'

from apps.frontend.urls import LANGS, PAGE_HANDLER_PAGES

from apps.frontend.views.page import PageHandler
from apps.frontend.views.ping_pong import PingPongHandler
from apps.frontend.views.news import NewsHandler
from apps.frontend.views.error import ErrorHandler

handlers = [
    (r'[\/]?$', PageHandler),
    (r'%s[\/]?$' % LANGS, PageHandler),
    (r'%s/%s[\/]?$' % (LANGS, PAGE_HANDLER_PAGES), PageHandler),
    (r'%s/(news)[\/]?(\d+)?[\/]?$' % LANGS, NewsHandler),
    (r'/ping-pong[\/]?$', PingPongHandler),
    (r'%s/(.*)$' % LANGS, ErrorHandler),
    (r'(.*)$', ErrorHandler),
]