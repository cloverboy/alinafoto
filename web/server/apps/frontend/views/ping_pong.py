# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-07-29'

from utils.date import current_server_time

from apps.frontend.views.base import BaseHandler


class PingPongHandler(BaseHandler):

    def get(self, *args, **kwargs):
        super(PingPongHandler, self).finish(unicode(current_server_time()))