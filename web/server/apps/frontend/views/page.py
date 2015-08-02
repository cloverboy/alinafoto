# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2013-11-21'

from apps.frontend.views.base import BaseHandler
from apps.frontend.urls import PAGE_HANDLER_PAGE_ALIASES

from settings import DEFAULT_LANG


class PageHandler(BaseHandler):

    def get(self, lang=DEFAULT_LANG, page='index', *args, **kwargs):
        underscored_page = page.replace('-', '_')
        page_title_key = '%s_page_title' % underscored_page
        page = PAGE_HANDLER_PAGE_ALIASES.get(page, page)
        tpl_name = '%s.html' % underscored_page
        super(PageHandler, self).render(tpl_name, lang, page, page_title_key=page_title_key)