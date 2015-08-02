# -*- coding: utf-8 -*-

from lib.db import DataProvider

_data_provider = None


def get_data_provider(settings, *args, **kwargs):
    global _data_provider

    if _data_provider is None:
        server_port = settings.get('server_port')

        if server_port:
            logger_name = 'data-provider-%s' % server_port
        else:
            logger_name = None

        _data_provider = DataProvider(logger_name)
    return _data_provider