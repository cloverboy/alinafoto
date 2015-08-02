# -*- coding: utf-8 -*-

from apps.frontend.ui_modules.translation import TranslationUIModule
from apps.frontend.ui_modules.url import UrlUIModule


def get_ui_modules():
    return {
        '_': TranslationUIModule,
        'url': UrlUIModule,
    }