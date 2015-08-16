# -*- coding: utf-8 -*-

import os
import sys
import logging
from argparse import ArgumentParser

parser = ArgumentParser(prog='Manager server', description='Starts and stops all servers required')
parser.add_argument('-e', '--server-environ', default='local', help='Server environment (local|production)')
args = parser.parse_args()

server_environ = args.server_environ

os.environ.update({
    'SERVER_ENVIRON': server_environ,
})

SERVER_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.normpath(os.path.join(SERVER_PATH, '../../'))
sys.path.insert(0, BASE_PATH)

print '++++++ sys.path = <%s> +++++' % sys.path

from lib.manager import ManagerServer

if __name__ == '__main__':

    logger = logging.getLogger('manager-server')
    logger.info('------------------------------------------------')
    logger.info('started in {} environment'.format(server_environ))

    manager_server = ManagerServer()
    manager_server.start()