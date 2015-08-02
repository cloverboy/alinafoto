# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2013-11-21'

import logging
import traceback

from tornado.web import RequestHandler
from tornado.locale import set_default_locale

from apps.frontend.data_provider import get_data_provider

from utils.locale import get_locale_code_by_lang
from utils.compress import gzip_string

from settings import (
    BASE_DOMAIN, MEDIA_DOMAIN, BASE_DOMAIN_PROTOCOL,
    MEDIA_DOMAIN_PROTOCOL, DEFAULT_LANG, DEBUG,
    GOOGLE_ANALYTICS_ENABLED, GOOGLE_ANALYTICS_CODE,
    LOCALE_LANG_SHORT_ONLY)

logger = logging.getLogger('mail_error')


class BaseHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def finish(self, chunk=None):
        if chunk is not None:

            replace_dict = {
                '\t': '',
                '\n': '',
                '\r\n': '',
                '    \r\n': '',
                '  \r\n': ' ',
                '    ': '',
                '  ': ' ',
                '> <': '><',
                '; ': ';',
            }

            for a, b in replace_dict.iteritems():
                chunk = chunk.replace(a, b)

            chunk = gzip_string(chunk)
            self.set_header('Content-Encoding', 'gzip')
            self.set_header('Content-Length', str(len(chunk)))

        super(BaseHandler, self).finish(chunk)

    def render(self, tpl_name, lang=DEFAULT_LANG, page=None, tpl_kwargs={}, page_title_key=None, status_code=None):

        if lang not in LOCALE_LANG_SHORT_ONLY:
            lang = DEFAULT_LANG

        underscored_page = page.replace('-', '_')
        if page_title_key is None:
            page_title_key = '%s_page_title' % underscored_page

        page_short_url = self.request.uri
        page_full_url = '%s://%s%s' % (BASE_DOMAIN_PROTOCOL, self.request.host, page_short_url)

        dp = get_data_provider(self.application.settings)

        render_tpl_kwargs = {
            'page_description': dp.get('locale_string', '%s_page_description' % underscored_page, lang),
            'page_keywords': dp.get('locale_string', '%s_page_keywords' % underscored_page, lang),
            'page_title': dp.get('locale_string', page_title_key, lang),
            'google_analytics_enabled': GOOGLE_ANALYTICS_ENABLED,
            'google_analytics_code': GOOGLE_ANALYTICS_CODE,
            'base_domain': BASE_DOMAIN,
            'base_domain_protocol': BASE_DOMAIN_PROTOCOL,
            'media_domain': MEDIA_DOMAIN,
            'media_domain_protocol': MEDIA_DOMAIN_PROTOCOL,
            'page_short_url': page_short_url,
            'page_full_url': page_full_url,
            'page': page,
            'lang': lang,
        }
        render_tpl_kwargs.update(tpl_kwargs)

        set_default_locale(get_locale_code_by_lang(lang))

        if status_code is not None:
            self.set_status(status_code=status_code)
            self._log()

        try:
            super(BaseHandler, self).render('frontend/page/%s' % tpl_name, **render_tpl_kwargs)
        except Exception, e:

            formatted_lines = traceback.format_exc().splitlines()
            content = ', '.join(formatted_lines)

            if DEBUG:
                #self.finish(content)
                raise
            else:
                self.render_error_404(lang)
                logger.error(content)

    def render_error_404(self, lang=DEFAULT_LANG):
        self.render('error.html', lang, page='error', status_code=404)