# -*- coding: utf-8 -*-

from lib.utils.date import current_server_time

from apps.frontend.views.base import BaseHandler


class PingPongHandler(BaseHandler):

    def get(self, *args, **kwargs):
        super(PingPongHandler, self).finish(unicode(current_server_time()))