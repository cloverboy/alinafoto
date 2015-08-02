# -*- coding: utf-8 -*-
import os

#----------COMMON----------
SERVER_ENVIRON = os.environ.get('SERVER_ENVIRON', 'production')
PYTHON_EXECUTABLE = 'python'
DEBUG = False

#----------PATHS----------
BASE_DOMAIN = 'www.alinafoto.lv'
MEDIA_DOMAIN = BASE_DOMAIN
BASE_DOMAIN_PROTOCOL = 'http'
MEDIA_DOMAIN_PROTOCOL = BASE_DOMAIN_PROTOCOL
LAUNCHER_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.normpath(os.path.join(LAUNCHER_PATH, '../../'))
STATIC_PATH = os.path.normpath(os.path.join(BASE_PATH, '../static'))
TEMPLATES_PATH = os.path.join(BASE_PATH, 'templates')
LOG_PATH = os.path.join(BASE_PATH, '../logs')
TMP_PATH = os.path.join(BASE_PATH, '../tmp')

#----------LANGUAGES----------
DEFAULT_LANG = 'lv'
DEFAULT_LANG_ID = 1
DEFAULT_LOCALE_CODE = 'lv_LV'

LOCALE_LANG_FULL = (
    (1, 'Latvian'),
    (2, 'Russian'),
    (3, 'English'),
)

LOCALE_LANG_SHORT = (
    (1, 'lv'),
    (2, 'ru'),
    (3, 'en'),
)

LOCALE_LANG_SHORT_ONLY = ['lv', 'ru', 'en',]

LOCALE_CODE = (
    ('lv', 'lv_LV'),
    ('ru', 'ru_RU'),
    ('en', 'en_US'),
)

#----------FRONTEND----------
FRONTEND_SERVER_PORTS = [50220, ]

#----------MANAGER----------
MANAGER_PUB_ADDRESS = '127.0.0.1'
MANAGER_PUB_PORT = 50240
MANAGER_PROCESSES_CONFIG = []

MANAGER_PROCESSES_CONFIG.extend([
    {
        'title': 'frontend server on port %s' % port,
        'launcher': os.path.join(BASE_PATH, 'apps', 'frontend', 'server.py',),
        'args': {
            '--server-port': str(port),
            '--server-environ': SERVER_ENVIRON,
        },
        'enabled': True,
    }
    for port in FRONTEND_SERVER_PORTS
])

#----------TIME-ZONE----------
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = None # 'Europe/Riga'
TIME_ZONE_OFFSET = 10800 # used to generate server timestamps
TIME_ZONE_GMT_OFFSET = 0 # used to generate gmt string for setting a session cookie

#----------MAIL----------
LOGGER_EMAIL_HOST = 'localhost'
LOGGER_EMAIL = 'wysemediaerrors@gmail.com'

#----------LOGGING----------
LOGGING = {
    'version': 1,
    'formatters': {
        'brief': {
            'format': r'%(asctime)s -- %(levelname)s -- %(name)s -- %(message)s',
            'datefmt': r'%H:%M:%S',
        },
        'precise': {
            'format': r'%(asctime)s -- %(levelname)-5s -- %(name)-30s -- %(message)s',
            'datefmt': r'%Y-%m-%d %H:%M:%S',
        },
        'verbose': {
            'format': r'%(asctime)s -- %(levelname)-5s -- %(pathname)s -- %(funcName)s -- %(lineno)-3d -- %(name)s -- %(message)s',
            'datefmt': r'%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'precise',
            'filename': os.path.join(LOG_PATH, 'server.log'),
            'encoding': 'utf-8',
        },
        'tornado.general': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'brief',
            'filename': os.path.join(LOG_PATH, 'tornado.general.log'),
            'encoding': 'utf-8',
        },
        'tornado.application': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'brief',
            'filename': os.path.join(LOG_PATH, 'tornado.application.log'),
            'encoding': 'utf-8',
        },
        'tornado.access': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'brief',
            'filename': os.path.join(LOG_PATH, 'tornado.access.log'),
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'precise',
        },
        'mail_error': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': LOGGER_EMAIL_HOST,
            'fromaddr': LOGGER_EMAIL,
            'toaddrs': LOGGER_EMAIL,
            'subject': 'DEBUG %s ERROR' % BASE_DOMAIN,
        },
    },
    'loggers': {
        'tornado.general': {
            'handlers': ['tornado.general', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tornado.application': {
            'handlers': ['tornado.application', 'mail_error', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tornado.access': {
            'handlers': ['tornado.access', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'mail_error': {
            'handlers': ['mail_error', ],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

DEFAULT_LOGGER_CONFIG = {
    'handlers': ['default', ],
    'level': 'DEBUG',
    'propagate': False,
}

LOGGER_LIST = []
LOGGER_LIST.extend(['default', 'manager-server', ])
LOGGER_LIST.extend(['frontend-server-%s' % port for port in FRONTEND_SERVER_PORTS])
LOGGER_LIST.extend(['data-provider-%s' % port for port in FRONTEND_SERVER_PORTS])

for item in LOGGER_LIST:
    LOGGING['loggers'][item] = DEFAULT_LOGGER_CONFIG

from logging import config
config.dictConfig(LOGGING)

#----------GOOGLE-ANALYTICS----------
GOOGLE_ANALYTICS_ENABLED = True
GOOGLE_ANALYTICS_CODE = 'UA-46207976-1'