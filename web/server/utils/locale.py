# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2013-11-21'

from settings import DEFAULT_LANG, LOCALE_CODE, DEFAULT_LOCALE_CODE


def get_locale_code_by_lang(locale_lang=None):
    for lang, code in LOCALE_CODE:
        if lang == locale_lang:
            return code
    return DEFAULT_LOCALE_CODE


def get_lang_by_locale_code(locale_code):
    for lang, code in LOCALE_CODE:
        if code == locale_code:
            return lang
    return DEFAULT_LANG
