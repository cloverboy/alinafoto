# -*- coding: utf-8 -*-

from apps.frontend.views.base import BaseHandler

from settings import DEFAULT_LANG


class ErrorHandler(BaseHandler):

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)

    def get(self, lang=DEFAULT_LANG, *args, **kwargs):
        self.render_error_404(lang)