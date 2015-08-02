# -*- coding: utf-8 -*-

from tornado.web import UIModule

from apps.frontend.urls import reverse_page


class UrlUIModule(UIModule):

    def render(self, page_name, *args, **kwargs):
        return reverse_page(page_name, *args, **kwargs)