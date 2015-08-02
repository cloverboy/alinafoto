# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-09'

from tornado.web import UIModule

from apps.frontend.data_provider import get_data_provider

from utils.locale import get_lang_by_locale_code


class Translation(UIModule):

    def render(self, item, **kwargs):
        result = self._get_translation(item, self.locale.code)
        if kwargs.get('obfuscate'):
            result = self.obfuscate(result)
        return result

    def _get_translation(self, item, locale_code):
        return get_data_provider(self.handler.settings).get('locale_string', item, get_lang_by_locale_code(locale_code))

    def obfuscate(self, item):
        return ''.join(['&#%s;' % str(ord(char)) for char in item])