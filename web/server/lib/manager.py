# -*- coding: utf-8 -*-

import time
import signal
import logging
import psutil
from tornado.gen import coroutine, Task
from zmq import Context
from zmq.sugar.constants import PUB, SUB, SUBSCRIBE, LINGER
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop.ioloop import IOLoop, install
install()

from settings import (
    MANAGER_PROCESSES_CONFIG, MANAGER_PUB_ADDRESS,
    MANAGER_PUB_PORT, PYTHON_EXECUTABLE)

NOTIFICATION_PROCESS_STOP = 'process_stop'


class ManagerControlled(object):

    def __init__(self, *args, **kwargs):
        self.context = Context.instance()
        self.loop = IOLoop.instance()
        self.control_socket = self.context.socket(SUB)
        self.control_socket.setsockopt(LINGER, 0)  # discard unsent messages on close
        self.control_socket.setsockopt(SUBSCRIBE, '')
        self.control_socket.connect('tcp://{}:{}'.format(MANAGER_PUB_ADDRESS, MANAGER_PUB_PORT))
        self.control_stream = ZMQStream(self.control_socket, self.loop)
        self.control_stream.on_recv_stream(self.control_handler)

    def control_handler(self, stream, message_list):
        for message in message_list:
            try:
                notification, data = message.split()
            except ValueError:
                notification = message

            if notification == NOTIFICATION_PROCESS_STOP:
                self.stop()

    def stop(self):
        self.control_stream.stop_on_recv()
        self.control_stream.close()
        self.control_socket.close()


class ManagerServer(object):

    _processes = []
    _stopping = False

    def __init__(self):
        self.logger = logging.getLogger('manager-server')
        self.context = Context.instance()
        self.loop = IOLoop.instance()

        self.control_socket = self.context.socket(PUB)
        self.control_socket.setsockopt(LINGER, 0)  # discard unsent messages on close
        self.control_socket.bind('tcp://{}:{}'.format(MANAGER_PUB_ADDRESS, MANAGER_PUB_PORT))

        self.register_signals()

    def register_signals(self):
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGQUIT, self.stop)
        signal.signal(signal.SIGINT, self.stop)

    def start(self):
        self.loop.add_timeout(time.time() + 1, self.spawn_processes)
        self.loop.start()

    @coroutine
    def stop(self, *args, **kwargs):
        if self._stopping:
            self.logger.info('signal is ignored. stopping server')
        else:
            self._stopping = True

            self.logger.info('sent graceful server stop notification')
            self.control_socket.send(NOTIFICATION_PROCESS_STOP)

            self.logger.info('waiting 10 sec')
            yield Task(self.loop.add_timeout, time.time() + 10)

            for item in self._processes:
                self.stop_process(item)

            self.loop.stop()
            self.logger.info('server is stopped')

    @coroutine
    def spawn_processes(self):
        for item in MANAGER_PROCESSES_CONFIG:
            yield self.run_process(item)
        self.logger.info('server is ready')

    @coroutine
    def run_process(self, config):
        title = config.get('title')
        launcher = config.get('launcher')
        args_dict = config.get('args', {})
        enabled = config.get('enabled', False)

        if enabled:
            args = [PYTHON_EXECUTABLE, launcher]
            for k, v in args_dict.items():
                args.extend([k, v])

            p = psutil.Popen(args)
            pid = p.pid

            self._processes.append((title, pid))
            self.logger.info('spawned %s with pid %s' % (title, pid))

            yield Task(self.loop.add_timeout, time.time() + 2)

    def stop_process(self, config):
        title, pid = config
        try:
            self.logger.info('stopping %s with pid %s' % (title, pid))
            p = psutil.Process(pid)
        except psutil.NoSuchProcess:
            pass
        else:
            p.terminate()
            p.wait(timeout=2)