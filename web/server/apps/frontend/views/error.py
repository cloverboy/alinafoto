# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-06'

from apps.frontend.views.base import BaseHandler

from settings import DEFAULT_LANG


class ErrorHandler(BaseHandler):

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)

    def get(self, lang=DEFAULT_LANG, *args, **kwargs):
        self.render_error_404(lang)