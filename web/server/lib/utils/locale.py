# -*- coding: utf-8 -*-

from settings import (
    DEFAULT_LANG, LOCALE_CODE, DEFAULT_LOCALE_CODE,
    LOCALE_LANG_SHORT, DEFAULT_LANG_ID)


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


def get_lang_id_by_lang(lang):
    for lang_id, lang_short in LOCALE_LANG_SHORT:
        if lang_short == lang:
            return lang_id
    return DEFAULT_LANG_ID


def get_lang_by_id(lng_id):
    for lang_id, lang_short in LOCALE_LANG_SHORT:
        if lang_id == lng_id:
            return lang_short
    return DEFAULT_LANG


def get_lang_id_by_locale_code(locale_code):
    return get_lang_id_by_lang(get_lang_by_locale_code(locale_code))