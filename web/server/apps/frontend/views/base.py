# -*- coding: utf-8 -*-

import os
import logging

from tornado.web import RequestHandler
from tornado.locale import set_default_locale

from lib.utils.file import file_exists
from lib.utils.locale import get_locale_code_by_lang
from lib.utils.compress import gzip_string, minify_string
from lib.utils.collector import TracebackCollector
from lib.translation import Translation

from settings import (
    BASE_DOMAIN, MEDIA_DOMAIN, BASE_DOMAIN_PROTOCOL, MEDIA_DOMAIN_PROTOCOL,
    DEFAULT_LANG, DEBUG, GOOGLE_ANALYTICS_ENABLED, GOOGLE_ANALYTICS_TRACK_ID,
    LOCALE_LANG_SHORT_ONLY, FACEBOOK_APP_ID, FACEBOOK_APP_PAGE, DISQUS_APP_ID,
    TEMPLATES_PATH)

logger = logging.getLogger('default')


class BaseHandler(RequestHandler):

    SUPPORTED_METHODS = ('GET',)

    def finish(self, chunk=None, minify=True, gzip=True, is_json=False, status_code=None, log_request=True):
        if chunk is not None:

            if minify:
                chunk = minify_string(chunk)

            if gzip:
                chunk = gzip_string(chunk)
                self.set_header('Content-Encoding', 'gzip')
                self.set_header('Content-Length', str(len(chunk)))

            if is_json:
                self.set_header('Content-Type', 'application/json')

            if status_code is not None:
                self.set_status(status_code=status_code)
                if log_request:
                    self._log()

            if DEBUG:
                self.set_header('X-Response-Time', '%.2fms' % (1000.0 * self.request.request_time()))

        super(BaseHandler, self).finish(chunk)

    def render(self, tpl_name=None, lang=DEFAULT_LANG, page=None, tpl_kwargs=None, page_title=None,
               page_title_key=None, page_description=None, page_description_key=None,
               page_keywords=None, page_keywords_key=None, og_image=None,
               status_code=None, *args, **kwargs):

        if tpl_name is None:
            tpl_name = 'base.html'

            if page is not None:
                page_tpl_name = '%s.html' % page
                if file_exists(os.path.join(TEMPLATES_PATH, page_tpl_name)):
                    tpl_name = page_tpl_name

        if lang not in LOCALE_LANG_SHORT_ONLY:
            lang = DEFAULT_LANG

        locale_code = get_locale_code_by_lang(lang)
        trans = Translation()

        if tpl_kwargs is None:
            tpl_kwargs = {}

        if page_title is None:
            if page_title_key is None:
                underscored_page = page.replace('-', '_')
                page_title_key = '%s_page_title' % underscored_page
            page_title = trans.find(page_title_key, lang)

        if page_description is None:
            if page_description_key is None:
                page_description_key = 'page_description'
            page_description = trans.find(page_description_key, lang)

        if page_keywords is None:
            if page_keywords_key is None:
                page_keywords_key = 'page_keywords'
            page_keywords = trans.find(page_keywords_key, lang, [])

        page_short_url = self.request.uri
        page_full_url = '%s://%s%s' % (BASE_DOMAIN_PROTOCOL, self.request.host, page_short_url)

        render_tpl_kwargs = {
            'page_title': page_title,
            'page_description': page_description,
            'page_keywords': page_keywords,
            'google_analytics_enabled': GOOGLE_ANALYTICS_ENABLED,
            'google_analytics_track_id': GOOGLE_ANALYTICS_TRACK_ID,
            'facebook_app_id': FACEBOOK_APP_ID,
            'facebook_app_page': FACEBOOK_APP_PAGE,
            'disqus_app_id': DISQUS_APP_ID,
            'base_domain': BASE_DOMAIN,
            'media_domain': MEDIA_DOMAIN,
            'base_domain_protocol': BASE_DOMAIN_PROTOCOL,
            'media_domain_protocol': MEDIA_DOMAIN_PROTOCOL,
            'base_path': '%s://%s' % (BASE_DOMAIN_PROTOCOL, BASE_DOMAIN),
            'media_path': '%s://%s' % (BASE_DOMAIN_PROTOCOL, MEDIA_DOMAIN),
            'langs': LOCALE_LANG_SHORT_ONLY,
            'page_short_url': page_short_url,
            'page_full_url': page_full_url,
            'locale_code': locale_code,
            'debug': DEBUG,
            'page': page,
            'lang': lang,
        }
        render_tpl_kwargs.update(tpl_kwargs)

        set_default_locale(locale_code)

        if status_code is not None:
            self.set_status(status_code=status_code)
            self._log()

        try:
            super(BaseHandler, self).render(tpl_name, **render_tpl_kwargs)
        except Exception as e:
            ip = self.request.remote_ip
            collected = TracebackCollector().collect(e)

            if DEBUG:
                raise

            else:
                self.render_error_404(lang)
                logger.error('ip: <%s>, collected: <%s>' %
                             (ip, collected))

    def render_error_404(self, lang=DEFAULT_LANG):
        self.render('error.html', lang, page='error', status_code=404)

    def _log_form_error(self, field_errors, cleaned_data, descr='', user_id=None, **kwargs):
        msg = [
            descr,
            'field_errors: <%s>' % field_errors,
            'cleaned_data: <%s>' % cleaned_data,
            'user_id: <%s>' % user_id,
            'ip: <%s>' % self.request.remote_ip,
            'uri: <%s>' % self.request.uri,
            'method: <%s>' % self.request.method,
        ]
        for k, v in kwargs.items():
            msg.append('%s: <%s>' % (k, v))
        logger.error(', '.join(msg))