# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-09'

from apps.frontend.ui_modules.translation import Translation
from apps.frontend.ui_modules.url import URL
from apps.frontend.ui_modules.static_file import StaticFile


def get_ui_modules():
    return {
        '_': Translation,
        'url': URL,
        'static': StaticFile,
    }