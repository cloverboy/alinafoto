# -*- coding: utf-8 -*-

from tornado.web import UIModule

from lib.utils.locale import get_lang_by_locale_code
from lib.utils.encoding import html_char_entities
from lib.translation import Translation


class TranslationUIModule(UIModule):

    def render(self, key, **kwargs):
        lang = get_lang_by_locale_code(self.locale.code)
        result = Translation().find(key, lang)

        if kwargs.get('html_char_entities'):
            result = html_char_entities(result)

        return result