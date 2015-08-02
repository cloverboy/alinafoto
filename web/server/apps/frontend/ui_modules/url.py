# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-09'

from tornado.web import UIModule

from apps.frontend.urls import reverse_page


class URL(UIModule):

    def render(self, page_name, *args, **kwargs):
        return reverse_page(page_name, *args, **kwargs)