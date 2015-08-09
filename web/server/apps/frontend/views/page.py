# -*- coding: utf-8 -*-

from apps.frontend.views.base import BaseHandler

from settings import DEFAULT_LANG


class PageHandler(BaseHandler):

    def get(self, lang=DEFAULT_LANG, page='index', *args, **kwargs):
        super(PageHandler, self).render(lang=lang, page=page)