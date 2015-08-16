# -*- coding: utf-8 -*-

import os
import sys
import logging
from argparse import ArgumentParser

parser = ArgumentParser(prog='Frontend server', description='Server for handling web requests')
parser.add_argument('-p', '--server-port', default=5000, help='Port number')
parser.add_argument('-e', '--server-environ', default='local', help='Server environment (local|production)')
args = parser.parse_args()

server_port = args.server_port
server_environ = args.server_environ

os.environ.update({
    'SERVER_PORT': server_port,
    'SERVER_ENVIRON': server_environ,
})

SERVER_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.normpath(os.path.join(SERVER_PATH, '../../'))
sys.path.insert(0, BASE_PATH)

from settings import DEBUG, TEMPLATES_PATH

from tornado.web import Application
from tornado.httpserver import  HTTPServer
from zmq.eventloop.ioloop import install, IOLoop
install()

from apps.frontend.url_handlers import handlers
from apps.frontend.ui_modules import get_ui_modules


if __name__ == '__main__':
    logger = logging.getLogger('frontend-server-%s' % server_port)

    app = Application(
        handlers=handlers,
        ui_modules=get_ui_modules(),
        template_path=TEMPLATES_PATH,
        server_port=server_port,
        logger=logger,
        debug=DEBUG,
    )

    http_server = HTTPServer(app, xheaders=(not DEBUG))
    http_server.listen(server_port)

    logger = app.settings.get('logger')
    logger.info('launched in {} environment'.format(server_environ))
    logger.info('ready')

    IOLoop.instance().start()