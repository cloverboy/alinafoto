# -*- coding: utf-8 -*-

__author__ = 'Roman Ruskov'
__date__ = '2013-11-25'

import os
import sys
import logging
from argparse import ArgumentParser

# setup environment
parser = ArgumentParser(prog='Manager server', description='Starts and stops all servers required')
parser.add_argument('-e', '--server-environ', default='local', help='Server environment (local|development|production)')
args = parser.parse_args()

server_environ = args.server_environ

os.environ.update({
    'SERVER_ENVIRON': server_environ,
})

SERVER_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.normpath(os.path.join(SERVER_PATH, '../../'))
sys.path.insert(0, BASE_PATH)

# load libraries according to current system environment
from lib.manager import ManagerServer


# start server
if __name__ == '__main__':

    logger = logging.getLogger('manager-server')
    logger.info('------------------------------------------------')
    logger.info('started in {} environment'.format(server_environ))

    manager_server = ManagerServer.getInstance()
    manager_server.start()