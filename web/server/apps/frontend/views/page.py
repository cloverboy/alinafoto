# -*- coding: utf-8 -*-

from apps.frontend.views.base import BaseHandler

from settings import DEFAULT_LANG


class PageHandler(BaseHandler):

    def get(self, lang=DEFAULT_LANG, page='index', *args, **kwargs):
        underscored_page = page.replace('-', '_')
        super(PageHandler, self).render('%s.html' % underscored_page, lang, page)