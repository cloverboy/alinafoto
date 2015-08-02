# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2014-01-09'

from tornado.web import UIModule

from utils.file import get_static_file_relative_path

from settings import BASE_DOMAIN, MEDIA_DOMAIN, MEDIA_DOMAIN_PROTOCOL, DEBUG


class StaticFile(UIModule):

    _cache = {}

    def render(self, *args, **kwargs):
        return self.get_static_file(*args, **kwargs)

    def get_static_file(self, path, *args, **kwargs):

        if not DEBUG:
            try:
                return self._cache[path]
            except KeyError:
                pass

        relative_path = get_static_file_relative_path(path)
        full_url = kwargs.get('full_url', BASE_DOMAIN != MEDIA_DOMAIN)

        if full_url:
            result = '%s://%s/%s' % (MEDIA_DOMAIN_PROTOCOL, MEDIA_DOMAIN, relative_path)
        else:
            result = '/%s' % relative_path

        if not DEBUG:
            self._cache[path] = result

        return result