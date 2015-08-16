# -*- coding: utf-8 -*-

from tornado.web import StaticFileHandler

from apps.frontend.urls import LANGS, PAGE_HANDLER_PAGES

from apps.frontend.views.page import PageHandler
from apps.frontend.views.ping_pong import PingPongHandler
from apps.frontend.views.error import ErrorHandler

from settings import STATIC_PATH

handlers = [
    (r'[\/]?$', PageHandler),
    (r'%s[\/]?$' % LANGS, PageHandler),
    (r'%s/%s[\/]?$' % (LANGS, PAGE_HANDLER_PAGES), PageHandler),
    (r'/ping-pong[\/]?$', PingPongHandler),
    (r'/(.*\.(gif|jpg|jpeg|png|ico|js|css|html|swf|xml|txt))$', StaticFileHandler, {'path': STATIC_PATH}),
    (r'%s/(.*)$' % LANGS, ErrorHandler),
    (r'(.*)$', ErrorHandler),
]